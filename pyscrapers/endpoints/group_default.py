"""
The default group of operations that pyscrapers has
"""
import logging
import shelve

import requests
from pornhub_api import PornhubApi
from pytconf.config import register_endpoint, register_function_group

import pyscrapers.core.utils
import pyscrapers.version
from pyscrapers.configs import ConfigDebugRequests, ConfigCookiesSource, ConfigSiteId, ConfigPornhubSearch, \
    ConfigYoutubeDl, ConfigPornhubDownload, ConfigPornhubPornstar, ConfigDownload
from pyscrapers.core.urlset import UrlSet
from pyscrapers.workers.drumeo import get_number_of_pages, get_courses, get_course_details, get_course_urls, \
    download_course
from pyscrapers.workers.facebook import scrape_facebook
from pyscrapers.workers.instagram import scrape_instagram
from pyscrapers.workers.mambaru import scrape_mambaru
from pyscrapers.workers.pornhub import download, print_stars_all_detailed, pornhub_download_pornstar_handler
from pyscrapers.workers.travelgirls import scrape_travelgirls
from pyscrapers.workers.vk import scrape_vk
from pyscrapers.workers.youtube_dl_handlers import youtube_dl_handler

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pyscapers commands"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    configs=[],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pyscrapers.version.VERSION_STR)


@register_endpoint(
    configs=[
        ConfigSiteId,
        ConfigDebugRequests,
        ConfigCookiesSource,
        ConfigDownload,
    ],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def photos():
    """
    Download photo albums from various sites
    """
    if ConfigDebugRequests.debug:
        pyscrapers.core.utils.debug_requests()
    ConfigCookiesSource.config_cookies()
    session = requests.Session()
    session.cookies = ConfigCookiesSource.cookies
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
    configs=[
        ConfigDebugRequests,
        ConfigCookiesSource,
    ],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def drumeo():
    """
    Download videos from drumeo
    """
    if ConfigDebugRequests.debug:
        pyscrapers.core.utils.debug_requests()

    ConfigCookiesSource.config_cookies()

    session = requests.Session()
    session.cookies = ConfigCookiesSource.cookies

    logger = logging.getLogger(__name__)
    courses = False
    reload = {}
    with shelve.open("cache.db") as d:
        if "courses" in d:
            list_of_courses = d["courses"]
            print("got from cache [{}] courses".format(len(list_of_courses)))
        else:
            pages = get_number_of_pages(courses=courses, session=session)
            print("number of pages is [{}]".format(pages))
            list_of_courses = get_courses(pages, courses=courses, session=session)
            print("got [{}] courses".format(len(list_of_courses)))
            d["courses"] = list_of_courses
        for i, course in enumerate(list_of_courses):
            logger.info("course number [%s]", i)
            if course.number in d and course.number not in reload:
                list_of_courses[i] = d[course.number]
                logger.info("got from cache [%s]", list_of_courses[i])
            else:
                get_course_details(course, courses=courses, session=session)
                get_course_urls(course, courses=courses, session=session)
                print(course)
                d[course.number] = course
            download_course(list_of_courses[i], session)
    session.close()


@register_endpoint(
    configs=[
        ConfigPornhubSearch,
        ConfigPornhubDownload,
    ],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def pornhub():
    """
    Download movies from pornhub
    """
    download()


@register_endpoint(
    configs=[],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def pornhub_stars_all_detailed():
    """
    print stars all detailed
    """
    api = PornhubApi()
    print_stars_all_detailed(api)


@register_endpoint(
    configs=[
        ConfigYoutubeDl,
    ],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def youtube_dl():
    """
    Download movies from pornhub
    """
    youtube_dl_handler()


@register_endpoint(
    configs=[
        ConfigDebugRequests,
        ConfigCookiesSource,
        ConfigPornhubPornstar,
        ConfigPornhubDownload,
    ],
    suggest_configs=[],
    group=GROUP_NAME_DEFAULT,
)
def pornhub_download_pornstar():
    """
    Download movies of a pornstar from pornhub
    """
    pornhub_download_pornstar_handler()
