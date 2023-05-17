"""
Download books from audible
"""
from typing import List
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


def add_book_ids(soup, book_ids) -> bool:
    divs = soup.find_all("div", {"class": "adbl-library-content-row"})
    more_titles = False
    for div in divs:
        book_id = div["id"].split("-")[-1]
        if book_id not in book_ids:
            book_ids.append(book_id)
            more_titles = True
    return more_titles


def add_links(soup, book_ids) -> bool:
    divs = soup.find_all("div", {"class": "adbl-library-content-row"})
    more_titles = False
    for div in divs:
        contents = div.contents
        assert len(contents) >= 1
        div = contents[1]
        contents = div.contents
        assert len(contents) >= 1
        div = contents[1]
        contents = div.contents
        assert len(contents) >= 1
        div = contents[1]
        contents = div.contents
        assert len(contents) >= 1
        a = contents[1]
        elem_href = a["href"]
        if elem_href not in book_ids:
            print(f"appending {elem_href}...")
            book_ids.append(elem_href)
            more_titles = True
    print(len(book_ids))
    return more_titles


def audible(_logger: Logger):
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
    session = ExtSession(base="https://www.audible.com")
    page = 1
    book_ids: List[str] = []
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
        # if not add_book_ids(soup, book_ids):
        if not add_links(soup, book_ids):
            break
        page += 1
    print(book_ids)
    # print(len(book_ids))
    # books = []
    # for book_id in book_ids:
    #     books.append(get_book_data(session, book_id))
