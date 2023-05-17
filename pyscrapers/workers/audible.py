"""
Download books from audible
"""
from collections import OrderedDict
from logging import Logger
from bs4 import BeautifulSoup
from pyscrapers.core.ext_requests import ExtSession
from pyscrapers.configs import ConfigDebugUrls


def get_book_data(session: ExtSession, book_id: str) -> OrderedDict:
    url = f"https://www.audible.com/pb/{book_id}"
    print(f"getting {url}...")
    response = session.get_timeout(url)
    soup = BeautifulSoup(
        markup=response.res.text,
        features="lxml",
    )
    if ConfigDebugUrls.save:
        pretty = soup.prettify()
        with open("/tmp/single.html", "wt") as handle:
            handle.write(pretty)
    d = OrderedDict()
    divs = soup.find_all("h1", {"class": "bc-heading"})
    print(divs)
    assert len(divs) == 1
    d["title"] = divs[0].text
    return d


def audible(_logger: Logger):
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
    session = ExtSession(base="https://www.audible.com")
    page = 1
    more_titles = True
    book_ids = []
    while True:
        url = f"https://www.audible.com/library/titles?page={page}"
        print(f"getting {url}...")
        response = session.get_timeout(url)
        soup = BeautifulSoup(
            markup=response.res.text,
            features="lxml",
        )
        if ConfigDebugUrls.save:
            pretty = soup.prettify()
            with open(f"/tmp/page{page}.html", "wt") as handle:
                handle.write(pretty)

        # collect all books ids from the page
        divs = soup.find_all("div", {"class": "adbl-library-content-row"})
        more_titles = False
        for div in divs:
            book_id = div["id"].split("-")[-1]
            if book_id not in book_ids:
                book_ids.append(book_id)
                more_titles = True
        if not more_titles:
            break
        page += 1
    # print(book_ids)
    # print(len(book_ids))
    books = []
    for book_id in book_ids:
        books.append(get_book_data(session, book_id))
