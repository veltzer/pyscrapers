"""
Module to handle scraping of pornhub.

References:
- https://pypi.org/project/pornhub-api/
"""
import os
from itertools import islice

import pornhub_api
from pornhub_api import PornhubApi

from pyscrapers.configs import ConfigPornhubSearch, ConfigPornhubDownload
from pyscrapers.workers.youtube_dl_handlers import youtube_dl_download_urls


def print_stars_all(api: pornhub_api.api.PornhubApi) -> None:
    stars_results = api.stars.all()
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
    api = PornhubApi()

    limit = ConfigPornhubSearch.limit
    over = False
    page = 1
    counter = 0
    while not over:
        try:
            kwargs = dict()
            if ConfigPornhubSearch.use_ordering:
                kwargs["ordering"] = ConfigPornhubSearch.ordering
            if ConfigPornhubSearch.use_period:
                kwargs["period"] = ConfigPornhubSearch.period
            if ConfigPornhubSearch.use_tags:
                kwargs["tags"] = ConfigPornhubSearch.tags
            data = api.search.search(
                ConfigPornhubSearch.query,
                page=page,
                **kwargs,
            )
            urls = [video.url for video in data.videos]
            if limit is not None:
                urls = list(islice(urls, 0, limit-counter))
            youtube_dl_download_urls(
                urls,
                os.path.join(
                    ConfigPornhubDownload.folder,
                    ConfigPornhubSearch.query,
                )
            )
            counter += len(urls)
            page += 1
            if counter == limit:
                break
        except ValueError as e:
            code = e.args[0]["code"]
            if code == "2001":  # no videos found (end of results)
                over = True
            else:
                raise e
