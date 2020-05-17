import logging
from typing import List

from lxml import etree

import pyscrapers.core.utils


def scrape_facebook(user_id: str, session) -> List[str]:
    logger = logging.getLogger(__name__)

    url = 'https://www.facebook.com/{user_id}/workers'.format(user_id=user_id)
    logger.debug('url is [%s]', url)
    r = session.get(url)
    root = pyscrapers.core.utils.get_html_dom_content(r)
    # print(etree.tostring(root, pretty_print=True))
    # sys.exit(1)

    urls = []
    e_a = root.xpath('//img')
    for x in e_a:
        print(etree.tostring(x, pretty_print=True))
    return urls
