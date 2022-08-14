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
    # cookie_domain = '.instagram.com'
    base = f'https://{domain}'
    user_url = f'{base}/{user_id}/'
    # url = f'{base}'
    url = "https://i.instagram.com/api/v1/users/web_profile_info"

    logger = logging.getLogger(__name__)

    response = session.get(user_url)
    response.raise_for_status()
    params = {
        "username": user_id,
    }
    headers = {
        "x-ig-app-id": "936619743392459",
    }
    response = session.get(url, params=params, headers=headers)
    response.raise_for_status()
    obj = response.json()
    user_id_json = obj["data"]["user"]["id"]
    profile_pic_url_hd = obj["data"]["user"]["profile_pic_url_hd"]
    url_set.append(profile_pic_url_hd)
    get_urls(logger, session, base, url_set, user_id_json)


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
        logger.info(f"size of list is [{len(url_set.urls_list)}]")
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
                        logger.info("ratelimit, sleeping...")
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
