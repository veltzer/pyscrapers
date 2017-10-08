import logging
from typing import List

import requests
from lxml import etree

import pyscrapers.core.utils


def scrape_facebook(user_id: str, cookies) -> List[str]:
    logger = logging.getLogger(__name__)
    s = requests.Session()
    s.cookies = cookies

    url = 'https://www.facebook.com/{user_id}/photos'.format(user_id=user_id)
    logger.debug('url is [%s]', url)
    r = s.get(url)
    root = pyscrapers.core.utils.get_html_dom_content(r)
    # print(etree.tostring(root, pretty_print=True))
    # sys.exit(1)

    urls = []
    e_a = root.xpath('//img')
    for x in e_a:
        print(etree.tostring(x, pretty_print=True))
    return urls
