"""
How does this work?
When you fetch the page of a user on instagram you get an html with a javascript embedded
in it with a json object embedded in that. This json object describes the user, his id,
his profile photo and the first 12 images for that user.
If you want to more photos you have to do a follow-up AJAX request to the server.
"""
import json
from typing import List

import requests
from lxml import etree

import pyscrapers.core.utils


def scrape_instagram(user_id: str, cookies) -> List[str]:
    domain = 'www.instagram.com'
    base = 'https://{domain}'.format(domain=domain)

    url = '{base}/{user_id}/'.format(base=base, user_id=user_id)

    # start a session
    s = requests.Session()
    s.cookies = cookies

    r = s.get(url)
    root = pyscrapers.core.utils.get_html_dom_content(r)
    # scrape.utils.print_element(root)

    urls = []
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
        urls.append(c['profile_pic_url_hd'])
    elif 'profile_pic_url' in c:
        urls.append(c['profile_pic_url'])
    user_id = c['id']
    url2 = '{base}/graphql/query/'.format(base=base)
    has_next_page = True
    end_cursor = None
    while has_next_page:
        variables = {
                'id': user_id,
                'first': 12,
        }
        if end_cursor:
            variables['after'] = end_cursor
        params = {
            # 'query_id': 17888483320059182,
            'query_hash': 'bd0d6d184eefd4d0ce7036c11ae58ed9',
            'variables': json.dumps(variables)
        }
        r2 = s.get(url2, params=params, cookies=r.cookies)
        # print(r2.json())
        # quit()
        data_user = r2.json()['data']['user']['edge_owner_to_timeline_media']
        has_next_page = data_user['page_info']['has_next_page']
        end_cursor = data_user['page_info']['end_cursor']
        for node in data_user['edges']:
            # if it is a video, then append the video, too
            if node['node']['is_video']:
                urls.append(node['node']['video_url'])
                # print(json.dumps(node['node'], indent=4, sort_keys=True))
            urls.append(node['node']['display_url'])
    return urls
