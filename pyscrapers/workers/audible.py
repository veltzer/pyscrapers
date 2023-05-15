"""
Download books from audible
"""
from logging import Logger
from bs4 import BeautifulSoup
from pyscrapers.core.ext_requests import ExtSession


def audible(_logger: Logger):
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
    session = ExtSession(base="https://www.audible.com")
    response = session.get_timeout("https://www.audible.com/library/titles")
    soup = BeautifulSoup(
        markup=response.res.text,
        features="lxml",
    )
    pretty = soup.prettify()
    with open("/tmp/temp", "wt") as handle:
        handle.write(pretty)
    # response.save_text()
