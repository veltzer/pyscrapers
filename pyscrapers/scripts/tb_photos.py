import argparse

import browser_cookie3
import requests

import pyscrapers.utils


def main():
    # command line parsing
    parser = argparse.ArgumentParser(
            description='''download photos from travelgirls.com'''
    )
    parser.add_argument(
            '-i',
            '--id', 
            help='''id of the user to download the albums of
            For instance if you see a url like this:
                http://www.travelgirls.com/member/[user_id]
            then the id for this script will be:
                [user_id]
            '''
    )
    args = parser.parse_args()
    if args.id is None:
        parser.error('-i/--id must be given')

    # load cookies from browser
    cookies = browser_cookie3.firefox()

    main_url = 'http://www.travelgirls.com/member/{id}'.format(id=args.id)
    r = requests.get(main_url, cookies=cookies)
    root = pyscrapers.utils.get_real_content(r)

    urls = []
    e_a = root.xpath('//a[contains(@class,\'photo\')]')
    for x in e_a:
        # print(etree.tostring(x, pretty_print=True))
        children = x.getchildren()
        assert len(children) == 1
        img = children[0]
        url = pyscrapers.utils.add_http(img.attrib['src'], main_url)
        url = url.replace('mini', '')
        urls.append(url)

    pyscrapers.utils.download_urls(urls)


if __name__ == '__main__':
    main()
