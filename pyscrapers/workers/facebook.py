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

    url = 'https://www.facebook.com/{user_id}/workers'.format(user_id=user_id)
    logger.debug('url is [%s]', url)
    result = session.get(url)
    root = pyscrapers.core.utils.get_html_dom_content(result)

    elements_img = root.xpath('//img')
    url_set.append(elements_img)
