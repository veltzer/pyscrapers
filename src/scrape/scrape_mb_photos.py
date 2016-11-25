import requests  # for post
import logging  # for basicConfig, getLogger
import argparse  # for ArgumentParser
import browser_cookie3  # for firefox
import scrape.utils  # for download_urls, get_real_content


# set up the logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)


def main():
    # command line parsing
    parser = argparse.ArgumentParser(
            description='''download photos from mamba.ru'''
    )
    parser.add_argument(
            '-i',
            '--id', 
            help='''id of the user to download the albums of
            For instance if you see a url like this:
                http://www.mamba.ru/mb[number]
            then the id for this script will be:
                mb[number]
            '''
    )
    args = parser.parse_args()
    if args.id is None:
        parser.error('-i/--id must be given')

    # load cookies from browser
    cookies = browser_cookie3.firefox()

    main_url = 'http://www.mamba.ru/{id}'.format(id=args.id)
    r = requests.get(main_url, cookies=cookies)
    root = scrape.utils.get_real_content(r)
    print(root)

if __name__ == '__main__':
    main()
