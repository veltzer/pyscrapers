""" python deps for this project """

scripts: dict[str,str] = {
    "pyscrapers": "pyscrapers.main:main",
}

config_requires: list[str] = [
    "pyclassifiers",
]
install_requires: list[str] = [
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
    "pydantic",
]
build_requires: list[str] = [
    "hatch",
    "pydmt",
    "pymakehelper",
    "pycmdtools",
]
test_requires: list[str] = [
    "pylint",
    "pytest",
    "mypy",
    "ruff",
    # types
    "types-requests",
    "types-beautifulsoup4",
    "types-tqdm",
    "lxml-stubs",
]
requires = config_requires + install_requires + build_requires + test_requires
