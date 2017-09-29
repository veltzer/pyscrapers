from typing import List

import requests

import pyscrapers.core.utils


def scrape_travelgirls(user_id: str, cookies) -> List[str]:
    main_url = 'http://www.travelgirls.com/member/{user_id}'.format(user_id=user_id)
    r = requests.get(main_url, cookies=cookies)
    root = pyscrapers.core.utils.get_real_content(r)

    urls = []
    e_a = root.xpath('//a[contains(@class,\'photo\')]')
    for x in e_a:
        # print(etree.tostring(x, pretty_print=True))
        children = x.getchildren()
        assert len(children) == 1
        img = children[0]
        url = pyscrapers.core.utils.add_http(img.attrib['src'], main_url)
        url = url.replace('mini', '')
        urls.append(url)
    return urls
