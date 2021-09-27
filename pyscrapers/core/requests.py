
import http.client
import logging

import requests
from requests.adapters import TimeoutSauce

from pyscrapers.configs import ConfigRequests, get_cookies


class MyTimeout(TimeoutSauce):
    def __init__(self, *args, **kwargs):
        if kwargs['connect'] is None:
            kwargs['connect'] = ConfigRequests.connect_timeout
        if kwargs['read'] is None:
            kwargs['read'] = ConfigRequests.read_timeout
        super().__init__(*args, **kwargs)


def get_session():
    # doesnt work
    # requests.adapters.TimeoutSauce = MyTimeout
    if ConfigRequests.debug:
        debug_requests()
    session = requests.Session()
    # doesnt work
    # session.adapters.TimeoutSauce = MyTimeout
    session.cookies = get_cookies()
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
