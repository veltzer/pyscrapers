""" python deps for this project """

import config.shared

install_requires: list[str] = [
    "lxml",
    "requests",
    # "hyper",
    "browser-cookie3",
    # this module is needed by browser-cookies3 but is not listed as its dependency
    "dbus-python",
    "pytconf",
    "pylogconf",
    "youtube-dl",
    "pyeventroute",
    "fake-useragent",
    "tqdm",
    "beautifulsoup4",
    "pydantic",
]
build_requires: list[str] = config.shared.PBUILD
test_requires: list[str] = config.shared.PTEST
types_requires: list[str] = [
    "types-requests",
    "types-beautifulsoup4",
    "types-tqdm",
    "lxml-stubs",
]
requires = install_requires + build_requires + test_requires + types_requires

scripts: dict[str,str] = {
    "pyscrapers": "pyscrapers.main:main",
}
