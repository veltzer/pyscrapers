""" travelgirls.py """

from typing import TYPE_CHECKING

import pyscrapers.core.ext_lxml
import pyscrapers.core.utils

if TYPE_CHECKING:
    from pyscrapers.core.ext_requests import ExtSession
    from pyscrapers.core.url_set import UrlSet


def scrape_travelgirls(user_id: str, session: ExtSession, url_set: UrlSet) -> None:
    main_url = f"https://www.travelgirls.com/member/{user_id}"
    r = session.get(main_url)
    root = pyscrapers.core.ext_lxml.get_html_dom_content(r)

    e_a = pyscrapers.core.ext_lxml.xpath_elements(root, "//a[contains(@class,\"photo\")]")
    for x in e_a:
        children = x.getchildren()
        assert len(children) == 1
        img = children[0]
        url = pyscrapers.core.utils.add_http(img.attrib["src"], main_url)
        url = url.replace("mini", "")
        url = url.replace("thumb", "")
        url_set.append(url)
