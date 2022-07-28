
import http.client
import logging

import requests

from pyscrapers.configs import ConfigRequests
from pyscrapers.utils import get_cookies


def get_session():
    # doesnt work
    # requests.adapters.TimeoutSauce = MyTimeout
    if ConfigRequests.debug:
        debug_requests()
    session = requests.Session()
    # doesnt work
    # session.adapters.TimeoutSauce = MyTimeout
    cookies = get_cookies()
    if cookies is not None:
        session.cookies = cookies
    return session


def session_get(session, url):
    return session.get(url, timeout=(ConfigRequests.connect_timeout, ConfigRequests.read_timeout))


def debug_requests():
    """
    Activate the debugging features of the requests module
    :return:
    """
    http.client.HTTPConnection.debuglevel = 1
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.propagate = True
