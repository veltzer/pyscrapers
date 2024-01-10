from typing import List


console_scripts: List[str] = [
    "pyscrapers=pyscrapers.main:main",
]
dev_requires: List[str] = [
    "pypitools",
]
config_requires: List[str] = [
    "pyclassifiers",
]
install_requires: List[str] = [
    "lxml",
    "requests",
    # "hyper",
    "browser-cookie3",
    # this module is needed by browser-cookies3 but is not listed as it's dependency
    "dbus-python",
    "pytconf",
    "pylogconf",
    "pornhub-api",
    "youtube-dl",
    "pyeventroute",
    "fake-useragent",
    "tqdm",
    "beautifulsoup4",
    "pydantic==1.10.13",
]
make_requires: List[str] = [
    "pymakehelper",
    "pydmt",
    "types-beautifulsoup4",
    "types-tqdm",
    "lxml-stubs",
]
test_requires: List[str] = [
    "pylint",
    "pytest",
    "pytest-cov",
    "pyflakes",
    "pyre-check",
    "flake8",
    "mypy",
    "types-requests",
]
requires = config_requires + install_requires + make_requires + test_requires
