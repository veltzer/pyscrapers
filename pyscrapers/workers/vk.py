import json
import logging

import lxml.etree
import lxml.html

from pyscrapers.core.url_set import UrlSet


def get_my_content(r):
    """
    the return from the server in vk is not a standard HTML.
    this is why we must cut it up and cant use the regular
    'get_real_content' helper.
    """
    r.raise_for_status()
    str_content = r.content.decode(errors='ignore')
    str_content = str_content[str_content.find('<input'):]
    c = str.encode('<html><body>') + str.encode(str_content) + str.encode('</body></html>')
    root = lxml.html.fromstring(c)
    return root


def yield_json_objs_and_base(r):
    for x in get_my_content(r).xpath('//a[@onclick]'):
        onclick = x.attrib['onclick']
        if onclick.startswith('return showPhoto'):
            json_str = onclick[onclick.find('{'):onclick.rfind('}') + 1]
            # bas string, need fix lots of things...
            json_str = json_str.replace('\'', '"').replace('jumpTo', '"jumpTo"').replace('z:', '"z":')
            json_obj = json.loads(json_str)
            base = json_obj['temp']['base']
            if base == '':
                continue
            yield json_obj, base


def scrape_vk(user_id: str, session, url_set: UrlSet) -> None:
    logger = logging.getLogger(__name__)
    url = 'https://vk.com/al_photos.php'

    count = 0
    got = 1
    while got:
        got = 0
        data = {
            'act': 'show_albums',
            'al': '2',
            'owner': user_id,
            'offset': count,
        }
        logger.debug('doing request %d', count)
        r = session.post(url, data=data)
        for base, json_obj in yield_json_objs_and_base(r):
            got = get_urls(base, got, json_obj, url_set)
        count += got


def get_urls(base, got, json_obj, url_set):
    largest = 0
    largest_url = None
    min_len = min(len(v) for k, v in json_obj['temp'].items() if k.endswith('_'))
    if min_len == 3:
        for k, v in json_obj['temp'].items():
            if k != 'base':
                size = v[1] * v[2]
                if size > largest:
                    largest = size
                    largest_url = v[0]
        url_set.append(base + largest_url + '.jpg')
        got += 1
    if min_len == 1:
        for k, v in json_obj['temp'].items():
            if k != 'base':
                url_set.append(base + v[0] + '.jpg')
        got += 1
    return got


def get_total_images(logger, session, url, user_id):
    data = {
        'act': 'show_albums',
        'al': '1',
        'owner': user_id,
    }
    r = session.post(url, data=data)
    root = get_my_content(r)

    e_albums = root.xpath('//div[@class="photos_album_title_wrap"]')
    albums = {}
    for x in e_albums:
        name_of_album = x.getparent().getparent().getparent().getparent().attrib['id'].split('?')[0]
        e_len = x.xpath('.//div[@class="photos_album_counter fl_r"]/text()')
        albums[name_of_album] = int(e_len[0])
    logger.debug(albums)
    total_images = 0
    for v in albums.values():
        logger.debug('got [%d] partial images', v)
        total_images += v
    logger.debug('got [%d] potential images', total_images)
