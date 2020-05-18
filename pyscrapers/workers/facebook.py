"""
download photos from facebook
"""


import logging
from typing import List

import pyscrapers.core.utils


def scrape_facebook(user_id: str, session) -> List[str]:
    """
    download photos from facebook
    :param user_id:
    :param session:
    :return:
    """
    logger = logging.getLogger(__name__)

    url = 'https://www.facebook.com/{user_id}/workers'.format(user_id=user_id)
    logger.debug('url is [%s]', url)
    result = session.get(url)
    root = pyscrapers.core.utils.get_html_dom_content(result)

    urls = []
    elements_img = root.xpath('//img')
    urls.append(elements_img)
    return urls
