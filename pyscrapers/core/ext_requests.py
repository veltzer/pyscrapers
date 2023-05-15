import os
import shutil
import urllib

import http.client
import logging

import requests
from tqdm import tqdm

from fake_useragent import UserAgent

from pyscrapers.configs import ConfigRequests
from pyscrapers.utils import get_cookies

import pyscrapers.core.ffprobe


FAIL = True


class ExtResponse:

    def __init__(self, res: requests.Response):
        self.res = res

    def raise_for_status(self):
        return self.res.raise_for_status()

    def save_text(self, filename: str = "/tmp/temp"):
        try:
            with open(filename, "wt") as handle:
                handle.write(self.res.content.decode())
        except IOError:
            os.unlink(filename)

    def save_binary(self, filename: str = "/tmp/temp") -> None:
        try:
            with open(filename, 'wb') as handle:
                self.res.raw.decode_content = True
                shutil.copyfileobj(self.res.raw, handle)
        except IOError:
            os.unlink(filename)


class ExtSession(requests.Session):
    """
    Inherit from requests.Session and add capabilities
    """
    def __init__(self, base: str = ""):
        super().__init__()
        cookies = get_cookies()
        if cookies is not None:
            self.cookies = cookies
        self.base = base
        ua = UserAgent()
        self.headers["User-Agent"] = ua.chrome

    def get_timeout(self, url: str):
        return ExtResponse(self.get(url, timeout=(ConfigRequests.connect_timeout, ConfigRequests.read_timeout)))

    def ext_get(self, url: str, *args, **kwargs):
        abs_url = urllib.parse.urljoin(self.base, url)
        ret = super().get(abs_url, *args, **kwargs)
        ret.raise_for_status()
        return ExtResponse(ret)

    def download_url(self, source: str, target: str) -> None:
        """
        Download a single url to a file
        """
        logger = logging.getLogger(__name__)
        logger.info('downloading [%s] to [%s]', source, target)
        if os.path.isfile(target):
            logger.info('skipping [%s]', target)
            return
        response = self.ext_get(source, stream=True)
        response.save_text(target)
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
        response = self.ext_get(source, stream=True)
        response.save_binary(target)
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


CONTENT_LENGTH_HEADER = 'content-length'
BLOCK_SIZE = 1024 * 1024


def download(response, filename: str) -> None:
    if CONTENT_LENGTH_HEADER in response.headers:
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        assert total_size_in_bytes != 0
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, disable=not ConfigRequests.progress)
        have_total = True
    else:
        progress_bar = tqdm(unit='iB', unit_scale=True, disable=not ConfigRequests.progress)
        have_total = False
    # pylint: disable=broad-except
    try:
        with open(filename, "wb") as file_handle:
            for data in response.iter_content(BLOCK_SIZE):
                progress_bar.update(len(data))
                file_handle.write(data)
    except (Exception, KeyboardInterrupt, SystemError) as e:
        os.unlink(filename)
        raise e
    progress_bar.close()
    if have_total and ConfigRequests.progress:
        assert progress_bar.n == total_size_in_bytes, f"something wrong {progress_bar.n} =! {total_size_in_bytes}"
