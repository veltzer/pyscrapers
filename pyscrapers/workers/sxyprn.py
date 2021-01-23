import tempfile
import urllib.parse
from logging import Logger
from requests.sessions import Session

from pyscrapers.configs import ConfigUrl, ConfigDebugUrls
from pyscrapers.core.url_set import UrlSet
from pyscrapers.core.utils import get_html_dom_content, get_element_as_bytes


def sxyprn_download(session: Session, logger: Logger):
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
    response = session.get(url=ConfigUrl.url)
    url_parsed = urllib.parse.urlparse(ConfigUrl.url)
    # noinspection PyProtectedMember
    base_url = url_parsed._replace(path="", params="", query="", fragment="").geturl()

    root = get_html_dom_content(response)
    if ConfigDebugUrls.save:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            logger.info(f"writing file [{f.name}]")
            f.write(get_element_as_bytes(root))
    url_set = UrlSet()
    elements = root.xpath("//a[contains(@class,'js-pop')]")
    for element in elements:
        href = element.attrib["href"]
        url = urllib.parse.urljoin(base_url, href)
        no_fluff = urllib.parse.urlparse(url)._replace(params="", query="", fragment="").geturl()
        url_set.append(no_fluff)
    url_set.print()
