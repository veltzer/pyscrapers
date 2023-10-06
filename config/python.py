console_scripts = [
    "pyscrapers=pyscrapers.main:main",
]
dev_requires = [
    "pypitools",
]
make_requires = [
    "pyclassifiers",
    "pymakehelper",
    "pydmt",
    "sphinx",
]
install_requires = [
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
test_requires = [
    "pylint",
    "pytest",
    "pytest-cov",
    "pyflakes",
    "pyre-check",
    "flake8",
    "mypy",
    "types-requests",
]
