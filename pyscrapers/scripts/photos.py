import argparse

import browser_cookie3

import pyscrapers.core.utils
from pyscrapers.photos.facebook import scrape_facebook
from pyscrapers.photos.instagram import scrape_instagram
from pyscrapers.photos.mambaru import scrape_mambaru
from pyscrapers.photos.travelgirls import scrape_travelgirls
from pyscrapers.photos.vk import scrape_vk


def main():
    # command line parsing
    parser = argparse.ArgumentParser(
        description='''download photos from various sites'''
    )
    parser.add_argument(
        '-t',
        '--type',
        help="Which site to download from",
        choices=["facebook", "instagram", "travelgirls", "vk", "mamba.ru"],
    )
    parser.add_argument(
        '-u',
        '--user-id',
        help='''id of the user to download the albums of
            https://www.facebook.com/profile.php?id=[user_id]&fref=ts
            https://www.instagram.com/[user_id]
            http://www.travelgirls.com/member/[user_id]
            https://vk.com/id[user_id]?z=albums275458801
            http://www.mamba.ru/mb[user_id]
            '''
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='debug requests',
        default=False,
        action='store_true',
    )
    parser.add_argument(
        '-s',
        '--start',
        help='start number for image names',
        type=int,
        default=0,
    )
    args = parser.parse_args()
    if args.id is None:
        parser.error('-i/--id must be given')
    if args.debug:
        pyscrapers.core.utils.debug_requests()

    # load cookies from browser
    cookies = browser_cookie3.firefox()

    urls = []
    if args.type == "facebook":
        urls = scrape_facebook(args.id, cookies)
    if args.type == "instagram":
        urls = scrape_instagram(args.id, cookies)
    if args.type == "travelgirls":
        urls = scrape_travelgirls(args.id, cookies)
    if args.type == "vk":
        urls = scrape_vk(args.id, cookies)
    if args.type == "mamba.ur":
        urls = scrape_mambaru(args.id, cookies)
    pyscrapers.core.utils.download_urls(urls, start=args.start)


if __name__ == '__main__':
    main()
