"""
The default group of operations that pyscrapers has
"""
import logging
import shelve

import pylogconf.core
from pornhub_api import PornhubApi
from pytconf import register_endpoint, register_main, config_arg_parse_and_launch

from pyscrapers.configs import ConfigCookiesSource, ConfigSiteId, ConfigPornhubSearch, \
    ConfigYoutubeDl, ConfigDownload, ConfigLogging, ConfigUrl, ConfigDebugUrls, ConfigRequests, \
    ConfigUser
from pyscrapers.core.url_set import UrlSet
from pyscrapers.core.ext_requests import ExtSession
from pyscrapers.static import APP_NAME, VERSION_STR, LOGGER_NAME, DESCRIPTION
from pyscrapers.workers.drumeo import get_number_of_pages, get_courses, get_course_details, get_course_urls, \
    download_course
from pyscrapers.workers.facebook import scrape_facebook
from pyscrapers.workers.getpocket import getpocket_download
from pyscrapers.workers.instagram import scrape_instagram
from pyscrapers.workers.audible import audible
from pyscrapers.workers.mamba_ru import scrape_mambaru
from pyscrapers.workers.pornhub import download_search, print_stars_all_detailed, download_url
from pyscrapers.workers.sxyprn import sxyprn_download
from pyscrapers.workers.netflix import netflix_download
from pyscrapers.workers.instagram_stories import instagram_stories_download
from pyscrapers.workers.travelgirls import scrape_travelgirls
from pyscrapers.workers.vk import scrape_vk
from pyscrapers.workers.youtube_dl_handlers import youtube_dl_handler

import pyscrapers.core.ext_requests


@register_endpoint(
    description="Download photo albums from various sites",
    configs=[
        ConfigSiteId,
        ConfigRequests,
        ConfigCookiesSource,
        ConfigDownload,
        ConfigLogging,
    ],
)
def photos():
    pyscrapers.core.ext_requests.setup()
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(ConfigLogging.loglevel)
    session = ExtSession()
    url_set = UrlSet()
    if ConfigSiteId.site == "facebook":
        scrape_facebook(ConfigSiteId.user_id, session, url_set)
    if ConfigSiteId.site == "instagram":
        scrape_instagram(ConfigSiteId.user_id, session, url_set)
    if ConfigSiteId.site == "travelgirls":
        scrape_travelgirls(ConfigSiteId.user_id, session, url_set)
    if ConfigSiteId.site == "vk":
        scrape_vk(ConfigSiteId.user_id, session, url_set)
    if ConfigSiteId.site == "mamba.ru":
        scrape_mambaru(ConfigSiteId.user_id, session, url_set)
    url_set.download(session)
    session.close()


@register_endpoint(
    description="Download videos from drumeo",
    configs=[
        ConfigRequests,
        ConfigCookiesSource,
    ],
)
def drumeo():
    session = ExtSession()
    logger = logging.getLogger(__name__)
    courses = False
    reload = {}
    with shelve.open("cache.db") as d:
        if "courses" in d:
            list_of_courses = d["courses"]
            print(f"got from cache [{len(list_of_courses)}] courses")
        else:
            pages = get_number_of_pages(courses=courses, session=session)
            print(f"number of pages is [{pages}]")
            list_of_courses = get_courses(pages, courses=courses, session=session)
            print(f"got [{len(list_of_courses)}] courses")
            d["courses"] = list_of_courses
        for i, course in enumerate(list_of_courses):
            logger.info(f"course number [{i}]")
            if course.number in d and course.number not in reload:
                list_of_courses[i] = d[course.number]
                logger.info(f"got from cache [{list_of_courses[i]}]")
            else:
                get_course_details(course, courses=courses, session=session)
                get_course_urls(course, courses=courses, session=session)
                print(course)
                d[course.number] = course
            download_course(list_of_courses[i], session)
    session.close()


@register_endpoint(
    description="print stars all detailed",
)
def pornhub_stars_all_detailed():
    api = PornhubApi()
    print_stars_all_detailed(api)


@register_endpoint(
    description="Download search results from pornhub",
    configs=[
        ConfigPornhubSearch,
        ConfigDownload,
        ConfigYoutubeDl,
    ],
)
def pornhub_download_search():
    download_search()


@register_endpoint(
    description="Download url videos from pornhub",
    configs=[
        ConfigRequests,
        ConfigDebugUrls,
        ConfigCookiesSource,
        ConfigUrl,
        ConfigDownload,
        ConfigYoutubeDl,
    ],
)
def pornhub_download_url():
    session = ExtSession()
    download_url(session)


@register_endpoint(
    description="Download movies using youtuble_dl",
    configs=[
        ConfigUrl,
        ConfigYoutubeDl,
    ],
)
def youtube_dl():
    youtube_dl_handler()


@register_endpoint(
    description="Download list from getpocket",
    configs=[
        ConfigRequests,
        ConfigCookiesSource,
        ConfigDownload,
        ConfigLogging,
    ],
)
def getpocket():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(ConfigLogging.loglevel)
    session = ExtSession()
    getpocket_download(session, logger)


@register_endpoint(
    description="Download movies from sxyprn.com",
    configs=[
        ConfigRequests,
        ConfigUrl,
        ConfigLogging,
        ConfigDebugUrls,
    ],
)
def sxyprn():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(ConfigLogging.loglevel)
    session = ExtSession()
    sxyprn_download(session, logger)


@register_endpoint(
    description="Download your list from netflix",
    configs=[
        ConfigRequests,
        ConfigLogging,
        ConfigDebugUrls,
    ],
)
def netflix_list():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(ConfigLogging.loglevel)
    session = ExtSession()
    netflix_download(session, logger)


@register_endpoint(
    description="Download instagram stroies for a particular user",
    configs=[
        ConfigRequests,
        ConfigLogging,
        ConfigDebugUrls,
        ConfigUser,
        ConfigCookiesSource,
    ],
)
def instagram_stories():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(ConfigLogging.loglevel)
    session = ExtSession()
    instagram_stories_download(session, logger)


@register_endpoint(
    description="Download audible books list",
    configs=[
        ConfigRequests,
        ConfigLogging,
        ConfigDebugUrls,
        ConfigCookiesSource,
    ],
)
def audible_books():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(ConfigLogging.loglevel)
    audible(logger)


@register_main(
    main_description=DESCRIPTION,
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == '__main__':
    main()
