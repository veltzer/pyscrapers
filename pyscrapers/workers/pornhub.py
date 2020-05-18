"""
Module to handle scraping of pornhub.

References:
- https://pypi.org/project/pornhub-api/
"""

from itertools import islice

import pornhub_api
from pornhub_api import PornhubApi

from pyscrapers.configs import ConfigPornhubSearch


def print_stars_all(api: pornhub_api.api.PornhubApi):
    stars_results = api.stars.all()
    for star in islice(stars_results.stars, 0, 10):
        print(star.star.star_name)


def print_categories(api: pornhub_api.api.PornhubApi):
    categories = api.video.categories()
    for category in categories.categories:
        print("id [{}], name [{}]".format(category.id, category.category))


def print_tags(api: pornhub_api.api.PornhubApi):
    tags = api.video.tags(ConfigPornhubSearch.literal)
    for tag in tags:
        print("tag [{}]".format(tag))


def download():
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
            for video in data.videos:
                print(counter)
                print(video.video_id)
                print(video.title)
                print(video.url)
                counter += 1
                if counter == limit:
                    break
            page += 1
            if counter == limit:
                break
        except ValueError as e:
            code = e.args[0]["code"]
            if code == "2001":  # no videos found (end of results)
                over = True
            else:
                raise e
