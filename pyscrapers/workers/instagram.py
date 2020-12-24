"""
How does this work?
When you fetch the page of a user on instagram you get an html with javascript embedded
in it with a json object embedded in that. This json object describes the user, his id,
his profile photo and the first 12 images for that user.
If you want more you have to do a follow-up AJAX request to the server.
"""
import json
import logging
import time

import pyeventroute.route
from lxml import etree

from pyscrapers.core.utils import get_html_dom_content
from pyscrapers.core.url_set import UrlSet


def is_rate_limit(response) -> bool:
    """
    Rate limit messages look like this:
    { "message": "rate limited", "status": "fail" }
    :param response:
    :return:
    """
    return response["status"] == "fail" and response["message"] == "rate limited"


def scrape_instagram(user_id: str, session, url_set: UrlSet) -> None:
    domain = 'www.instagram.com'
    base = f'https://{domain}'
    url = f'{base}/{user_id}/'

    logger = logging.getLogger(__name__)

    response = session.get(url)
    root = get_html_dom_content(response)
    # scrape.utils.print_element(root)

    # register regular expressions with lxml
    # this means that we can use regular expression functions like 'match'
    # by specifying 're:match' in our xpath expressions
    ns = etree.FunctionNamespace("http://exslt.org/regular-expressions")
    ns.prefix = 're'
    e_a = root.xpath('//script[re:match(text(), "^window._sharedData")]')
    assert len(e_a) == 1
    data = e_a[0].text
    d = json.loads(data[data.find('{'):data.rfind('}') + 1])
    my_list = d['entry_data']['ProfilePage']
    assert len(my_list) == 1
    c = my_list[0]["graphql"]["user"]
    if 'profile_pic_url_hd' in c:
        url_set.append(c['profile_pic_url_hd'])
    elif 'profile_pic_url' in c:
        url_set.append(c['profile_pic_url'])
    user_id = c['id']
    get_urls(logger, session, base, url_set, user_id)


def get_urls(logger, session, base, url_set, user_id):
    url = f'{base}/graphql/query/'
    count = 50
    query_hashes = [
        'bd0d6d184eefd4d0ce7036c11ae58ed9',  # posts
        'ff260833edf142911047af6024eb634a',  # tagged
    ]
    keys = [
        'edge_owner_to_timeline_media',
        'edge_user_to_photos_of_you',
    ]
    stats_video = 0
    stats_image = 0
    stats_shortcode_video = 0
    for query_hash, key in zip(query_hashes, keys):
        logger.debug(f"size of list is [{len(url_set.urls_list)}]")
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
            response = session.get(url, params=params).json()
            data_user = response['data']['user'][key]
            has_next_page = data_user['page_info']['has_next_page']
            end_cursor = data_user['page_info']['end_cursor']
            for outer_node in data_user['edges']:
                inner_node = outer_node['node']
                if inner_node['is_video'] and 'video_url' in inner_node:
                    url_set.append(inner_node['video_url'])
                    stats_video += 1
                if inner_node['is_video'] and 'shortcode' in inner_node:
                    params = {
                        'query_hash': '03f541f086ce0a9b31f67688ff9c1e09',
                        'shortcode': inner_node['shortcode'],
                    }
                    response_short = session.get(url, params=params).json()
                    while is_rate_limit(response_short):
                        time.sleep(60)
                        response_short = session.get(url, params=params).json()
                    if 'data' in response_short:
                        url_set.append(response_short['data']['shortcode_media']['video_url'])
                    else:
                        pyeventroute.route.accept(response_short)
                    stats_shortcode_video += 1
                if 'display_url' in inner_node:
                    url_set.append(inner_node['display_url'])
                    stats_image += 1
    logger.info(f"stats_video [{stats_video}]")
    logger.info(f"stats_image [{stats_image}]")
    logger.info(f"stats_shortcode_video [{stats_shortcode_video}]")
