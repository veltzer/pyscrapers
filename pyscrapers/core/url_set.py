import logging
import os
import shutil
import urllib.parse
from typing import Union, List

from pyscrapers.configs import ConfigDownload


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
        self.counter_mp4 = 0

    def append(self, url: str) -> None:
        """
        add url to the list
        :param url:
        :return:
        """
        logger = logging.getLogger(__name__)
        logger.debug("collecting [{}]".format(url))
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

    def suggest_filename(self, suffix: str) -> Union[str, None]:
        if suffix == ".jpg":
            filename = 'image{0:04}.jpg'.format(self.counter_jpg)
            self.counter_jpg += 1
            return filename
        if suffix == ".mp4":
            filename = 'video{0:04}.mp4'.format(self.counter_mp4)
            self.counter_mp4 += 1
            return filename
        logger = logging.getLogger(__name__)
        logger.error('do not know how to handle suffix [%s]...', suffix)
        return None

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
        logger = logging.getLogger(__name__)
        logger.info('got [%d] urls', len(self.urls_list))
        if ConfigDownload.download:
            for url in self.urls_list:
                parse_result = urllib.parse.urlparse(url)
                path = parse_result.path
                logger.info('downloading [%s]...', url)
                response = session.get(url, stream=True)
                assert response.status_code == 200, response.content

                filename = self.get_filename(os.path.splitext(path)[1])
                if filename is None:
                    continue

                with open(filename, 'wb') as file_handle:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, file_handle)
                logger.info('written [%s]...', filename)
