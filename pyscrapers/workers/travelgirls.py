import pyscrapers.core.utils
from pyscrapers.core.url_set import UrlSet


def scrape_travelgirls(user_id: str, session, url_set: UrlSet) -> None:
    main_url = 'https://www.travelgirls.com/member/{user_id}'.format(user_id=user_id)
    r = session.get(main_url)
    root = pyscrapers.core.utils.get_html_dom_content(r)

    e_a = root.xpath('//a[contains(@class,\'photo\')]')
    for x in e_a:
        # print(etree.tostring(x, pretty_print=True))
        children = x.getchildren()
        assert len(children) == 1
        img = children[0]
        url = pyscrapers.core.utils.add_http(img.attrib['src'], main_url)
        url = url.replace('mini', '')
        url = url.replace('thumb', '')
        url_set.append(url)
