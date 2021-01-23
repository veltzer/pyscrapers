"""
Module to handle scraping of pornhub.

References:
- https://pypi.org/project/pornhub-api/
"""
import logging
import tempfile
from itertools import islice
from typing import List

import pornhub_api
import requests
from pornhub_api import PornhubApi

from pyscrapers.configs import ConfigPornhubSearch, ConfigUrl, get_cookies, ConfigDebugUrls
from pyscrapers.core.url_set import UrlSet
from pyscrapers.core.utils import get_html_dom_content, get_element_as_bytes
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
        print(f"id [{category.id}], name [{category.category}]")


def print_tags(api: pornhub_api.api.PornhubApi) -> None:
    tags = api.video.tags(ConfigPornhubSearch.literal)
    for tag in tags:
        print(f"tag [{tag}]")


def get_code(e: ValueError) -> int:
    return int(e.args[0]["code"])


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
            code: int = get_code(e)
            if code == 2001:  # no videos found (end of results)
                break
            raise e
        urls = [video.url for video in data.videos]
        if limit is not None:
            urls = list(islice(urls, 0, limit - counter))
        for url in urls:
            logger.info(f"doing item [{counter}]")
            # pylint: disable=broad-except
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
        logger.info(f"number of errors [{errors}]")
        logger.info(f"except_urls [{except_urls}]")


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
    logger = logging.getLogger(__name__)
    if ConfigDebugUrls.save:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            logger.info(f"writing file [{f.name}]")
            f.write(get_element_as_bytes(root))
    xpath_picks = [
        '//ul[@id=\'uploadedVideosSection\']',
        '//ul[@id=\'moreData\']',
        '//ul[@id=\'mostRecentVideosSection\']',
        '//ul[@id=\'showAllChanelVideos\']',
        '//ul[@id=\'pornstarsVideoSection\']',
        '//ul[@id=\'modelMostRecentVideosSection\']',

        # there are extras which we don't need (they provide extra
        # movies which have nothing to do with the page involved)
        # '//ul[@id=\'hottestMenuSection\']',
        # '//ul[@id=\'recommMenuSection\']',
        # '//ul[@id=\'claimedUploadedVideoSection\']',
        # '//ul[@id=\'claimedRecentVideoSection\']',
        # '//ul[@id=\'"videosUploadedSection\']',
        # '//ul[@id=\'"modelPaidClips\']',
    ]
    video_sections = []
    for xpath_pick in xpath_picks:
        video_sections.extend(root.xpath(xpath_pick))
    urls = []
    for video_section in video_sections:
        elements = video_section.xpath('li[contains(@class,\'pcVideoListItem\')]')
        for element in elements:
            # pyscrapers.core.utils.print_element(element)
            # key = element.attrib['_vkey']
            key = element.attrib['data-video-vkey']
            url = f"https://www.pornhub.com/view_video.php?viewkey={key}"
            urls.append(url)
    return urls


def url_generator(url: str):
    yield url
    page = 2
    while True:
        yield f"{url}?page={page}"
        page += 1


def download_url() -> None:
    session = requests.Session()
    session.cookies = get_cookies()
    logger = logging.getLogger(__name__)
    urls = UrlSet()
    for url in url_generator(url=ConfigUrl.url):
        logger.info(f"getting [{url}]...")
        response = session.get(url)
        if response.status_code != 200:
            logger.info(f"got code [{response.status_code}]...")
            break
        root = get_html_dom_content(response)
        new_urls = get_urls_from_page(root)
        if len(new_urls) == 0:
            break
        logger.info(f"got [{len(new_urls)}] new urls")
        for i, new_url in enumerate(new_urls):
            logger.info(f"url {i} is [{new_url}]")
        urls.extend(new_urls)
    session.close()
    logger.info(f"got total [{len(urls.urls_list)}] urls")
    logger.info(f"got [{urls.appended_twice}] appended twice urls")
    youtube_dl_download_urls(urls.urls_list)
