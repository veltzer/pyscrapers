"""
Module to handle scraping of pornhub.

References:
- https://pypi.org/project/pornhub-api/
"""
import logging
from itertools import islice
from typing import List

import pornhub_api
import requests
from pornhub_api import PornhubApi

import pyscrapers.core.utils
from pyscrapers.configs import ConfigPornhubSearch, ConfigDebugRequests, ConfigUrl, get_cookies
from pyscrapers.core.url_set import UrlSet
from pyscrapers.workers.youtube_dl_handlers import youtube_dl_download_url, youtube_dl_download_urls


def print_stars_all(api: pornhub_api.api.PornhubApi) -> None:
    stars_results = api.stars.all()
    for star in islice(stars_results.stars, 0, ConfigPornhubSearch.limit):
        print(star.star.star_name)


def print_stars_all_detailed(api: pornhub_api.api.PornhubApi) -> None:
    stars_results = api.stars.all_detailed()
    for star in islice(stars_results.stars, 0, ConfigPornhubSearch.limit):
        print(star.star.star_name)


def print_categories(api: pornhub_api.api.PornhubApi) -> None:
    categories = api.video.categories()
    for category in categories.categories:
        print("id [{}], name [{}]".format(category.id, category.category))


def print_tags(api: pornhub_api.api.PornhubApi) -> None:
    tags = api.video.tags(ConfigPornhubSearch.literal)
    for tag in tags:
        print("tag [{}]".format(tag))


def download_search() -> None:
    """
    Download movies from pornhub
    """
    logger = logging.getLogger(__name__)
    api = PornhubApi()

    limit = ConfigPornhubSearch.limit
    page = 1
    counter = 0
    errors = 0
    exceptions = []
    except_urls = []
    while True:
        kwargs = dict()
        if ConfigPornhubSearch.use_ordering:
            kwargs["ordering"] = ConfigPornhubSearch.ordering
        if ConfigPornhubSearch.use_period:
            kwargs["period"] = ConfigPornhubSearch.period
        if ConfigPornhubSearch.use_tags:
            kwargs["tags"] = ConfigPornhubSearch.tags
        try:
            data = api.search.search(
                ConfigPornhubSearch.query,
                page=page,
                **kwargs,
            )
        except ValueError as e:
            code = e.args[0]["code"]
            if code == "2001":  # no videos found (end of results)
                break
            raise e
        urls = [video.url for video in data.videos]
        if limit is not None:
            urls = list(islice(urls, 0, limit - counter))
        for url in urls:
            logger.info("doing item [{}]".format(counter))
            # noinspection PyBroadException
            try:
                youtube_dl_download_url(url)
            except Exception as e:
                errors += 1
                exceptions.append(e)
                except_urls.append(url)
            counter += 1
        page += 1
        if counter == limit:
            break
    if errors > 0:
        logger.info("number of errors [{}]".format(errors))
        logger.info("except_urls [{}]".format(except_urls))


def get_number_of_pages(root) -> int:
    """
    return number of pages for a pornstar
    :param root:
    :return:
    """
    counters = root.xpath('//div[contains(@class,\'showingInfo\')]')
    assert len(counters) == 1
    counter = counters[0]
    number = int(counter.text.strip().split()[3])
    number_in_page = 36
    number_of_pages = -(-number // number_in_page)
    return number_of_pages


def get_urls_from_page(root) -> List[str]:
    """
    return urls from page
    :param root:
    :return:
    """
    # video_sections = root.xpath('//section[@id=\'videosTab\']')
    # assert len(video_sections) == 1, len(video_sections)
    # video_section = video_sections[0]
    # video_section = video_sections[0]
    # <ul class="dropdownHottestVideos videos" id="hottestMenuSection">
    # <ul class="videos row-5-thumbs" id="mostRecentVideosSection">
    xpath_attempts = [
        '//ul[contains(@class,\'pornstarsVideos\')]',
        '//ul[@id=\'moreData\']',
        '//ul[@id=\'mostRecentVideosSection\']',
    ]
    video_sections = []
    for xpath_attempt in xpath_attempts:
        video_sections = root.xpath(xpath_attempt)
        if len(video_sections) == 1:
            break
    if len(video_sections) == 1:
        video_section = video_sections[0]
        elements = video_section.xpath('li[contains(@class,\'pcVideoListItem\')]')
        urls = []
        for element in elements:
            key = element.attrib['_vkey']
            url = "https://www.pornhub.com/view_video.php?viewkey={key}".format(key=key)
            urls.append(url)
        return urls
    return []


def url_generator(url: str):
    yield url
    page = 2
    while True:
        yield "{url}?page={page}".format(url=url, page=page)
        page += 1


def download_url() -> None:
    if ConfigDebugRequests.debug:
        pyscrapers.core.utils.debug_requests()
    session = requests.Session()
    session.cookies = get_cookies()
    logger = logging.getLogger(__name__)
    urls = UrlSet()
    for url in url_generator(url=ConfigUrl.url):
        logger.info("getting [{}]...".format(url))
        page = session.get(url)
        if page.status_code != 200:
            break
        root = pyscrapers.core.utils.get_html_dom_content(page)
        new_urls = get_urls_from_page(root)
        if len(new_urls) == 0:
            break
        logger.info("got [{}] new urls".format(len(new_urls)))
        for i, new_url in enumerate(new_urls):
            logger.info("url {} is [{}]".format(i, new_url))
        urls.extend(new_urls)
    session.close()
    logger.info("got total [{}] urls".format(len(urls.urls_list)))
    logger.info("got [{}] appended twice urls".format(urls.appended_twice))
    youtube_dl_download_urls(urls.urls_list)
