"""
download photos from facebook
"""


import logging

import pyscrapers.core.utils
from pyscrapers.core.url_set import UrlSet


def scrape_facebook(user_id: str, session, url_set: UrlSet) -> None:
    """
    download photos from facebook
    :param user_id:
    :param session:
    :param url_set:
    :return:
    """
    logger = logging.getLogger(__name__)

    url = f"https://www.facebook.com/{user_id}/workers"
    logger.debug(f"url is [{url}]")
    result = session.get(url)
    root = pyscrapers.core.ext_lxml.get_html_dom_content(result)

    elements_img = root.xpath('//img')
    url_set.append(elements_img)
