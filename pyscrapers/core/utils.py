import http.client
import logging
import os
import shutil
import urllib.parse

import lxml.html
import requests
from lxml import etree

from pyscrapers.core import ffprobe


def print_cookies(cookies, domain):
    print(domain)
    for cookie in cookies:
        print(cookie)


def get_real_content(r):
    assert r.status_code == 200
    '''
    if r.status_code!=200:
        print('got error')
        print(r.content.decode())
        sys.exit(1)
    '''
    str_content = r.content.decode()
    root = lxml.html.fromstring(str_content)
    return root


def download_urls(urls, start=0):
    logger = logging.getLogger(__name__)
    cnt = start
    logger.info('got [%d] real urls', len(urls))
    for url in urls:
        logger.info('downloading [%s]...', url)
        r = requests.get(url, stream=True)
        assert r.status_code == 200
        filename = 'image{0:04}.jpg'.format(cnt)
        assert not os.path.isfile(filename)
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        logger.info('written [%s]...', filename)
        cnt += 1


def debug_requests():
    http.client.HTTPConnection.debuglevel = 1
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.propagate = True


def add_http(url, main_url):
    return urllib.parse.urljoin(main_url, url)


def print_element(e):
    print(etree.tostring(e, pretty_print=True).decode())


def download_url(source: str, target: str) -> None:
    logger = logging.getLogger(__name__)
    logger.info('downloading [%s] to [%s]', source, target)
    if os.path.isfile(target):
        logger.info('skipping [%s]', target)
        return
    try:
        r = requests.get(source, stream=True)
        assert r.status_code == 200
        with open(target, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    except IOError:
        os.unlink(target)
    logger.info('written [%s]...', target)


FAIL = True


def download_video_if_wider(source: str, target: str, width: int) -> bool:
    logger = logging.getLogger(__name__)
    logger.info('downloading [%s] to [%s]', source, target)
    if os.path.isfile(target):
        file_width = ffprobe.height(target)
        if file_width >= width:
            logger.info('skipping because video with width exists [%s] %s %s', target, file_width, width)
            return True
        else:
            logger.info('continuing with download because of width [%s] %s %s', target, file_width, width)
    try:
        r = requests.get(source, stream=True)
        if FAIL:
            assert r.status_code == 200
        else:
            if r.status_code != 200:
                logger.info("got bad error code [%s] and failed to download", r.status_code)
                return False
        with open(target, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    except IOError:
        if os.path.isfile(target):
            os.unlink(target)
        if FAIL:
            raise ValueError("count not download")
        else:
            logger.info("failed to download file")
            return False
    logger.info('written [%s]...', target)
    return True


class Urls:
    """ list of urls to download and to where """
    def __init__(self, download_as_collecting=False):
        self.list = []
        self.download_as_collecting = download_as_collecting

    def add_url(self, source, target):
        self.list.append((source, target))
        if self.download_as_collecting:
            download_url(source=source, target=target)

    def print(self):
        for (source, target) in self.list:
            print(source, target, sep="\t")

    def download(self):
        for (source, target) in self.list:
            download_url(source=source, target=target)
