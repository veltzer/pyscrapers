import os
import shutil

import http.client
import logging

import requests

from pyscrapers.configs import ConfigRequests
from pyscrapers.utils import get_cookies

import pyscrapers.core.ffprobe


FAIL = True


class ExtSession(requests.Session):
    """
    Inherit from requests.Session and add capabilities
    """
    def __init__(self):
        super().__init__()
        cookies = get_cookies()
        if cookies is not None:
            self.cookies = cookies

    def my_get(self, url: str):
        return self.get(url, timeout=(ConfigRequests.connect_timeout, ConfigRequests.read_timeout))

    def download_url(self, source: str, target: str) -> None:
        """
        Download a single url to a file
        """
        logger = logging.getLogger(__name__)
        logger.info('downloading [%s] to [%s]', source, target)
        if os.path.isfile(target):
            logger.info('skipping [%s]', target)
            return
        try:
            response = self.get(source, stream=True)
            response.raise_for_status()
            with open(target, 'wb') as file_handle:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file_handle)
        except IOError:
            os.unlink(target)
        logger.info('written [%s]...', target)

    def download_video_if_wider(self, source: str, target: str, width: int) -> bool:
        """
        Download a video if it is wider than a certain width
        :param source:
        :param target:
        :param width:
        :param self:
        :return:
        """
        logger = logging.getLogger(__name__)
        logger.info('downloading [%s] to [%s]', source, target)
        if os.path.isfile(target):
            file_width = pyscrapers.core.ffprobe.height(target)
            if file_width >= width:
                logger.info('skipping because video with width exists [%s] %s %s', target, file_width, width)
                return True
            logger.info('continuing with download because of width [%s] %s %s', target, file_width, width)
        try:
            response = self.get(source, stream=True)
            if FAIL:
                response.raise_for_status()
            else:
                if response.status_code != 200:
                    logger.info("got bad error code [%s] and failed to download", response.status_code)
                    return False
            with open(target, 'wb') as file_handle:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, file_handle)
        except IOError as e:
            if os.path.isfile(target):
                os.unlink(target)
            if FAIL:
                raise ValueError("count not download") from e
            logger.info("failed to download file")
            return False
        logger.info('written [%s]...', target)
        return True


def setup():
    """
    Activate the debugging features of the requests module
    :return:
    """
    if ConfigRequests.debug:
        http.client.HTTPConnection.debuglevel = 1
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.propagate = True
