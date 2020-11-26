"""
The default group of operations that pyscrapers has
"""
import logging
import shelve

import pylogconf.core
import requests
from pornhub_api import PornhubApi
from pytconf import register_endpoint, register_main, config_arg_parse_and_launch

import pyscrapers.core.utils
from pyscrapers.configs import ConfigDebugRequests, ConfigCookiesSource, ConfigSiteId, ConfigPornhubSearch, \
    ConfigYoutubeDl, ConfigDownload, ConfigLogging, ConfigUrl, get_cookies
from pyscrapers.core.url_set import UrlSet
from pyscrapers.static import APP_NAME, VERSION_STR
from pyscrapers.workers.drumeo import get_number_of_pages, get_courses, get_course_details, get_course_urls, \
    download_course
from pyscrapers.workers.facebook import scrape_facebook
from pyscrapers.workers.instagram import scrape_instagram
from pyscrapers.workers.mambaru import scrape_mambaru
from pyscrapers.workers.pornhub import download_search, print_stars_all_detailed, download_url
from pyscrapers.workers.travelgirls import scrape_travelgirls
from pyscrapers.workers.vk import scrape_vk
from pyscrapers.workers.youtube_dl_handlers import youtube_dl_handler


@register_endpoint(
    description="Download photo albums from various sites",
    configs=[
        ConfigSiteId,
        ConfigDebugRequests,
        ConfigCookiesSource,
        ConfigDownload,
        ConfigLogging,
    ],
)
def photos():
    if ConfigDebugRequests.debug:
        pyscrapers.core.utils.debug_requests()
    logger = logging.getLogger('pyscrapers')
    logger.setLevel(ConfigLogging.loglevel)
    session = requests.Session()
    session.cookies = get_cookies()
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
        ConfigDebugRequests,
        ConfigCookiesSource,
    ],
)
def drumeo():
    if ConfigDebugRequests.debug:
        pyscrapers.core.utils.debug_requests()

    session = requests.Session()
    session.cookies = get_cookies()

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
        ConfigDebugRequests,
        ConfigCookiesSource,
        ConfigUrl,
        ConfigDownload,
        ConfigYoutubeDl,
    ],
)
def pornhub_download_url():
    download_url()


@register_endpoint(
    description="Download movies using youtuble_dl",
    configs=[
        ConfigUrl,
        ConfigYoutubeDl,
    ],
)
def youtube_dl():
    youtube_dl_handler()


@register_main(
    main_description="pyscapers will help you download stuff from the web",
    app_name=APP_NAME,
    version=VERSION_STR,
)
def main():
    pylogconf.core.setup()
    config_arg_parse_and_launch()


if __name__ == '__main__':
    main()
