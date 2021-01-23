import tempfile
import urllib.parse
from logging import Logger
from requests.sessions import Session

from pyscrapers.configs import ConfigUrl, ConfigDebugUrls
from pyscrapers.core.url_set import UrlSet
from pyscrapers.core.utils import get_html_dom_content, get_element_as_bytes
from pyscrapers.workers.youtube_dl_handlers import youtube_dl_download_urls


def url_generator(url: str):
    yield url
    page = 30
    while True:
        yield f"{url}?page={page}"
        page += 30


def sxyprn_download(session: Session, logger: Logger):
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
    url_parsed = urllib.parse.urlparse(ConfigUrl.url)
    # noinspection PyProtectedMember
    base_url = url_parsed._replace(path="", params="", query="", fragment="").geturl()

    urls = UrlSet()
    for url in url_generator(url=ConfigUrl.url):
        logger.info(f"loading [{url}]")
        response = session.get(url=url)
        if response.status_code != 200:
            logger.info(f"got code [{response.status_code}]...")
            break
        if response.text == "":
            logger.info(f"got empty response")
            break
        root = get_html_dom_content(response)
        if ConfigDebugUrls.save:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                logger.info(f"writing file [{f.name}]")
                f.write(get_element_as_bytes(root))
        elements = root.xpath("//a[contains(@class,'js-pop')]")
        for element in elements:
            href = element.attrib["href"]
            url = urllib.parse.urljoin(base_url, href)
            no_fluff = urllib.parse.urlparse(url)._replace(params="", query="", fragment="").geturl()
            urls.append(no_fluff)
    session.close()
    logger.info(f"got total [{len(urls.urls_list)}] urls")
    logger.info(f"got [{urls.appended_twice}] appended twice urls")
    youtube_dl_download_urls(urls.urls_list)
