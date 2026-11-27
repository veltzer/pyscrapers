""" utils.py """

from typing import TYPE_CHECKING

import browser_cookie3

from pyscrapers.configs import ConfigCookiesSource

if TYPE_CHECKING:
    from http.cookiejar import CookieJar


def get_cookies() -> CookieJar | None:
    if ConfigCookiesSource.browser == "firefox":
        return browser_cookie3.firefox()
    if ConfigCookiesSource.browser == "chrome":
        return browser_cookie3.chrome()
    return None
