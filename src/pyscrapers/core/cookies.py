"""
There are helpers for cookies
"""

from typing import Any


def print_cookies(cookies: Any, domain: str) -> None:
    """
    Print the cookies from a specific domain
    :param cookies:
    :param domain:
    :return:
    """
    print(domain)
    for cookie in cookies:
        print(cookie)
