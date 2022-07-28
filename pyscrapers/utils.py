import browser_cookie3


from pyscrapers.configs import ConfigCookiesSource


def get_cookies():
    if ConfigCookiesSource.browser == "firefox":
        return browser_cookie3.firefox()
    if ConfigCookiesSource.browser == "chrome":
        return browser_cookie3.chrome()
    return None
    # raise ValueError(f"unsupported browser [{ConfigCookiesSource.browser}")
