"""
How does this work?
When you fetch the page of a user on instagram you get an html with a javascript embedded
in it with a json object embedded in that. This json object describes the user, his id,
his profile photo and the first 12 images for that user.
If you want to more photos you have to do a follow-up AJAX request to the server.
"""
import json
import logging
from typing import List

import requests
from lxml import etree

import pyscrapers.core.utils


def scrape_instagram(user_id: str, cookies) -> List[str]:
    logger = logging.getLogger(__name__)
    # constants
    domain = 'www.instagram.com'
    base = 'https://{domain}'.format(domain=domain)

    url = '{base}/{user_id}/'.format(base=base, user_id=user_id)
    logger.debug('url is [%s]', url)

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
    c = my_list[0]["user"]
    if 'profile_pic_url_hd' in c:
        urls.append(c['profile_pic_url_hd'])
    elif 'profile_pic_url' in c:
        urls.append(c['profile_pic_url'])
    user_id = c['id']
    # json.dump(c, sys.stdout, indent=4)
    # list_node = c['media']['nodes']
    # for x in list_node:
    #    urls.append(x['display_src'])

    # now we need to do the follow up query
    # url2 = '{base}/query/'.format(base=base)

    """ g_user(278094193)+{+media.after(732083027810814056,+12)+{++count,++nodes+{++++caption,++++code,
    ++++comments+{++++++count++++},++++comments_disabled,++++date,++++dimensions+{++++++height,++++++width++++},
    ++++display_src,++++id,++++is_video,++++likes+{++++++count++++},++++owner+{++++++id++++},++++thumbnail_src,
    ++++video_views++},++page_info}+}" """
    """
    data = {
        # the 5000 is the number of images you want (big number to get all)
        # the 0 in media.after is after what. 0 seems to return everything I think
        # 'q':'ig_user({0})'.format(user_id)+'{ media.after(0, 5000) { count, nodes { display_src } } }',
        'q': 'ig_user({0})'.format(user_id)+'{ media.after(0, 5000) { nodes { display_src } } }',
        # 'q':'ig_user({0})'.format(user_id)+' { media.after(0, 5000) { count, nodes { caption, code, comments
        # { count }, comments_disabled, date, dimensions { height, width }, display_src, id, is_video, likes { count },
        # owner { id }, thumbnail_src, video_views }, page_info } }',
        'ref': 'users::show',
        # this is constant as far as I can tell
        'query_id': '17842962958175392',
    }
    cookie_to_search = 'csrftoken'
    cookie_value = r.cookies[cookie_to_search]
    headers = {
        # these two are necessary or you wont get response from instagram
        'X-CSRFToken': r.cookies[cookie_to_search],
        'Referer': url,
    }
    # you must send cookies and headers to get the data...
    r2 = s.post(url2, data=data, headers=headers)
    for node in res['media']['nodes']:
        urls.append(node['display_src'])
    """

    url2 = '{base}/graphql/query/'.format(base=base)
    params = {
        'query_id': 17888483320059182,
        'variables': json.dumps({
            'id': user_id,
            'first': 5000,
        })
    }
    r2 = s.get(url2, params=params, cookies=r.cookies)
    root = pyscrapers.core.utils.get_html_dom_content(r2)
    res = json.loads(root.text)
    for node in res['data']['user']['edge_owner_to_timeline_media']['edges']:
        urls.append(node['node']['display_url'])
    return urls
