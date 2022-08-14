import logging
import os
import urllib.parse
from collections import Counter
from typing import List

from pyscrapers.configs import ConfigDownload
from pyscrapers.core.ext_requests import download


class UrlSet:
    """ set of urls, with no duplicates. Can be downloaded """
    def __init__(self):
        """
        constructor
        """
        self.urls_set = set()
        self.urls_list = []
        self.appended_twice = 0
        self.counter_jpg = 0
        self.counter_video = 0

    def append(self, url: str) -> None:
        """
        add url to the list
        :param url:
        :return:
        """
        logger = logging.getLogger(__name__)
        logger.debug(f"collecting [{url}]")
        if url in self.urls_set:
            self.appended_twice += 1
        else:
            self.urls_set.add(url)
            self.urls_list.append(url)

    def extend(self, urls: List[str]) -> None:
        for url in urls:
            self.append(url)

    def print(self) -> None:
        """
        print the list
        :return:
        """
        for url in self.urls_list:
            print(url)

    def suggest_filename(self, suffix: str) -> str:
        if suffix == ".jpg":
            filename = f"image{self.counter_jpg:04d}.jpg"
            self.counter_jpg += 1
            return filename
        if suffix in (".mp4", ".webp"):
            filename = f"video{self.counter_video:04d}{suffix}"
            self.counter_video += 1
            return filename
        raise ValueError(f"dont know how to handle suffix [{suffix}]")

    def get_filename(self, suffix: str) -> str:
        filename = self.suggest_filename(suffix)
        while os.path.isfile(filename):
            filename = self.suggest_filename(suffix)
        return filename

    def download(self, session):
        """
        download the list
        :param session:
        :return:
        """
        skipped = 0
        downloads_per_suffix = Counter()
        logger = logging.getLogger(__name__)
        logger.info(f"got [{len(self.urls_list)}] urls")
        if ConfigDownload.download:
            for url in self.urls_list:
                parse_result = urllib.parse.urlparse(url)
                path = parse_result.path
                suffix = os.path.splitext(path)[1]
                filename = self.get_filename(suffix)
                if filename is None:
                    skipped += 1
                    logger.info(f"skipping [{path}]...")
                    continue

                logger.info(f"downloading [{path}] to [{filename}]...")
                response = session.get(url, stream=True)
                response.raise_for_status()
                downloads_per_suffix[suffix] += 1
                download(response, filename)
                logger.info(f"written [{filename}]...")
        logger.info(f"skipped [{skipped}]...")
        logger.info(downloads_per_suffix)
