"""
Module to handle scraping of pornhub.

References:
- https://pypi.org/project/pornhub-api/
"""
import logging
from itertools import islice

import pornhub_api
from pornhub_api import PornhubApi

from pyscrapers.configs import ConfigPornhubSearch, ConfigPornhubDownload
from pyscrapers.workers.youtube_dl_handlers import youtube_dl_download_url


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


def download() -> None:
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
            else:
                raise e
        urls = [video.url for video in data.videos]
        if limit is not None:
            urls = list(islice(urls, 0, limit - counter))
        for url in urls:
            logger.info("doing item [{}]".format(counter))
            # noinspection PyBroadException
            try:
                youtube_dl_download_url(url, ConfigPornhubDownload.folder)
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
