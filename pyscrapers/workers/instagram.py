"""
How does this work?
When you fetch the page of a user on instagram you get an html with a javascript embedded
in it with a json object embedded in that. This json object describes the user, his id,
his profile photo and the first 12 images for that user.
If you want to more workers you have to do a follow-up AJAX request to the server.
"""
import json
import logging

from lxml import etree

import pyscrapers.core.utils
from pyscrapers.core.urlset import UrlSet


def scrape_instagram(user_id: str, session, url_set: UrlSet) -> None:
    domain = 'www.instagram.com'
    base = 'https://{domain}'.format(domain=domain)
    url = '{base}/{user_id}/'.format(base=base, user_id=user_id)

    logger = logging.getLogger(__name__)

    r = session.get(url)
    root = pyscrapers.core.utils.get_html_dom_content(r)
    # scrape.utils.print_element(root)

    # register regular expressions with lxml
    # this means that we can use regular expression functions like 'match'
    # by specifying 're:match' in our xpath expressions
    ns = etree.FunctionNamespace("http://exslt.org/regular-expressions")
    ns.prefix = 're'
    e_a = root.xpath('//script[re:match(text(), "^window._sharedData")]')
    assert len(e_a) == 1
    e_a = e_a[0]
    data = e_a.text
    json_text = data[data.find('{'):data.rfind('}') + 1]
    d = json.loads(json_text)
    my_list = d['entry_data']['ProfilePage']
    assert (len(my_list) == 1)
    c = my_list[0]["graphql"]["user"]
    if 'profile_pic_url_hd' in c:
        url_set.append(c['profile_pic_url_hd'])
    elif 'profile_pic_url' in c:
        url_set.append(c['profile_pic_url'])
    user_id = c['id']
    url2 = '{base}/graphql/query/'.format(base=base)
    count = 50
    query_hashes = [
        'bd0d6d184eefd4d0ce7036c11ae58ed9',  # posts
        'ff260833edf142911047af6024eb634a',  # tagged
    ]
    keys = [
        'edge_owner_to_timeline_media',
        'edge_user_to_photos_of_you',
    ]
    counter = 0
    for query_hash, key in zip(query_hashes, keys):
        logger.debug("size of list is [{}]".format(len(url_set.urls_list)))
        has_next_page = True
        end_cursor = None
        while has_next_page:
            variables = {
                    'id': user_id,
                    'first': count,
            }
            if end_cursor:
                variables['after'] = end_cursor
            params = {
                'query_hash': query_hash,
                'variables': json.dumps(variables)
            }
            response = session.get(url2, params=params).json()
            data_user = response['data']['user'][key]
            has_next_page = data_user['page_info']['has_next_page']
            end_cursor = data_user['page_info']['end_cursor']
            for outer_node in data_user['edges']:
                inner_node = outer_node['node']
                if inner_node['is_video'] and 'video_url' in inner_node:
                    url_set.append(inner_node['video_url'])
                if 'display_url' in inner_node:
                    url_set.append(inner_node['display_url'])
            counter += 1
