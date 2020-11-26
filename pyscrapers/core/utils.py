"""
This module is s set of utilities for this entire project
"""


import http.client
import logging
import os
import shutil
import urllib.parse
from typing import List

import requests
import lxml
import lxml.html

import pyscrapers.core.ffprobe


def print_cookies(cookies, domain):
    """
    Print the cookies from a specific domain
    :param cookies:
    :param domain:
    :return:
    """
    print(domain)
    for cookie in cookies:
        print(cookie)


def get_http_status_string(code: int):
    """
    This function returns a description of an HTTP status code (404 - not found etc).
    Unfortunately, the requests module does not provide a clean API for this so
    we must access a protected member (underscore member) of 'requests.status_code'.
    See:
    https://stackoverflow.com/questions/24718557/get-the-description-of-a-status-code-in-python-requests
    :param code:
    :return:
    """
    return "http code [{}], [{}]".format(code, requests.status_codes.codes[code][0])


def get_html_dom_content(response):
    """
    Get the content from a request
    :param response:
    :return:
    """
    assert response.status_code == 200, get_http_status_string(response.status_code)
    str_content = response.content.decode()
    root = lxml.html.fromstring(str_content)
    return root


def download_urls(session, urls: List[str], start=0):
    """
    Download a list of urls
    :param session:
    :param urls:
    :param start:
    :return:
    """
    logger = logging.getLogger(__name__)
    counter = start
    logger.info('got [%d] real urls', len(urls))
    for url in urls:
        parse_result = urllib.parse.urlparse(url)
        path = parse_result.path
        logger.info('downloading [%s]...', url)
        response = session.get(url, stream=True)
        assert response.status_code == 200, response.content

        filename = None
        if path.endswith(".jpg"):
            filename = 'image{0:04}.jpg'.format(counter)
        if path.endswith(".mp4"):
            filename = 'video{0:04}.mp4'.format(counter)
        if filename is None:
            logger.error('do not know how to handle path [%s]...', path)
            continue
        assert not os.path.isfile(filename), "already have filename {}".format(path)
        with open(filename, 'wb') as file_handle:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file_handle)
        logger.info('written [%s]...', filename)
        counter += 1


def debug_requests():
    """
    Activate the debugging features of the requests module
    :return:
    """
    http.client.HTTPConnection.debuglevel = 1
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.propagate = True


def add_http(url, main_url):
    """
    add two urls together
    :param url:
    :param main_url:
    :return:
    """
    return urllib.parse.urljoin(main_url, url)


def print_element(element):
    """
    from xml elements from etree
    :param element:
    :return:
    """
    print(lxml.etree.tostring(element, pretty_print=True).decode())


def download_url(session, source: str, target: str) -> None:
    """
    Download a single url to a file
    """
    logger = logging.getLogger(__name__)
    logger.info('downloading [%s] to [%s]', source, target)
    if os.path.isfile(target):
        logger.info('skipping [%s]', target)
        return
    try:
        response = session.get(source, stream=True)
        assert response.status_code == 200, response.content
        with open(target, 'wb') as file_handle:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file_handle)
    except IOError:
        os.unlink(target)
    logger.info('written [%s]...', target)


FAIL = True


def download_video_if_wider(session, source: str, target: str, width: int) -> bool:
    """
    Download a video if it is wider than a certain width
    :param source:
    :param target:
    :param width:
    :param session:
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
        response = session.get(source, stream=True)
        if FAIL:
            assert response.status_code == 200, response.content
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
