"""
This module is s set of utilities for this entire project
"""


import urllib.parse
import http.client


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
    # noinspection PyProtectedMember,PyUnresolvedReferences
    # pylint: disable=protected-access
    # return f"http code [{code}], [{requests.status_codes._codes[code][0]}]"
    return f"http code [{code}], [{http.client.responses[code]}]"


def add_http(url, main_url):
    """
    add two urls together
    :param url:
    :param main_url:
    :return:
    """
    return urllib.parse.urljoin(main_url, url)
