#!/usr/bin/python3

'''
This script scrapes photos from travelgirls.com

For instance if you see a profile of a user like this:
    https://www.facebook.com/profile.php?id=[user_id]&fref=ts
then the id for this script will be:
    [user_id]
If the url is this way:
    https://www.facebook.com/[user_id]
then the id fro this script will be:
    [user_id]

References:
- http://docs.python-requests.org/en/master
- http://docs.python-guide.org/en/latest/scenarios/scrape
'''

import requests # for post
import lxml.html # for fromstring
import lxml.etree # for tostring
import json # for loads
import shutil # for copyfileobj
import sys # for argv
import logging # for basicConfig, getLogger
import argparse  # for ArgumentParser
import browser_cookie3 # for firefox
import scrape.utils # for download_urls, get_real_content

# set up the logger
logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

# command line parsing
parser = argparse.ArgumentParser(
        description='''download photos from facebook'''
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
cookies=browser_cookie3.firefox()

url='https://www.facebook.com/{id}/photos'.format(id=args.id)
logger.debug('url is [%s]', url)
r = requests.get(url)
root = get_real_content(r)
#print(lxml.etree.tostring(root, pretty_print=True))
#sys.exit(1)

urls=[]
e_a = root.xpath('//img')
for x in e_a:
    print(lxml.etree.tostring(x, pretty_print=True))

scrape.utils.download_urls(urls)
