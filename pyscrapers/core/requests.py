
import http.client
import logging

import requests
from requests.adapters import TimeoutSauce

from pyscrapers.configs import ConfigRequests, ConfigDebugRequests


class MyTimeout(TimeoutSauce):
    def __init__(self, *args, **kwargs):
        if kwargs['connect'] is None:
            kwargs['connect'] = ConfigRequests.connect_timeout
        if kwargs['read'] is None:
            kwargs['read'] = ConfigRequests.read_timeout
        super().__init__(*args, **kwargs)


def config_requests():
    requests.adapters.TimeoutSauce = MyTimeout
    if ConfigDebugRequests.debug:
        debug_requests()


def debug_requests():
    """
    Activate the debugging features of the requests module
    :return:
    """
    http.client.HTTPConnection.debuglevel = 1
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.propagate = True
