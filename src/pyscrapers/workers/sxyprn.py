""" sxyprn.py """

import tempfile
import urllib.parse
from typing import TYPE_CHECKING

from pyscrapers.configs import ConfigDebugUrls, ConfigUrl
from pyscrapers.core.ext_lxml import get_element_as_bytes, get_html_dom_content, xpath_elements
from pyscrapers.core.url_set import UrlSet
from pyscrapers.workers.youtube_dl_handlers import youtube_dl_download_urls

if TYPE_CHECKING:
    from logging import Logger

    from requests.sessions import Session


def url_generator(url: str):
    yield url
    page = 30
    while True:
        yield f"{url}?page={page}"
        page += 30


def sxyprn_download(session: Session, logger: Logger) -> None:
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
    url_parsed = urllib.parse.urlparse(ConfigUrl.url)
    # noinspection PyProtectedMember
    base_url = url_parsed._replace(path="", params="", query="", fragment="").geturl()

    num_pages = None
    urls = UrlSet()
    for counter, url in enumerate(url_generator(url=ConfigUrl.url), start=1):
        logger.info("loading [%s]", url)
        response = session.get(url)
        response.raise_for_status()
        root = get_html_dom_content(response)
        if num_pages is None:
            num_pages = len(xpath_elements(root, "//div[contains(@class,\"ctrl_el\")]"))
            if num_pages == 0:
                num_pages = 1
        if ConfigDebugUrls.save:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                logger.info("writing file [%s]", f.name)
                f.write(get_element_as_bytes(root))
        elements = xpath_elements(root, "//a[contains(@class,\"js-pop\")]")
        for element in elements:
            href = element.attrib["href"]
            full_url = urllib.parse.urljoin(base_url, href)
            no_fluff = urllib.parse.urlparse(full_url)._replace(params="", query="", fragment="").geturl()
            urls.append(no_fluff)
        if counter == num_pages:
            break
    session.close()
    logger.info("got total [%s] urls", len(urls.urls_list))
    logger.info("got [%s] appended twice urls", urls.appended_twice)
    youtube_dl_download_urls(urls.urls_list)
