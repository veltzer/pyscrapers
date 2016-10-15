#!/usr/bin/python3

'''
This script scrapes photos from travelgirls.com

For instance if you see a url like this:
    http://www.travelgirls.com/member/2126319
then the id for this script will be:
    2126319 

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
import urllib.parse # for urljoin
import browser_cookie3

def get_real_content(r):
    assert r.status_code==200
    strcontent=r.content.decode(errors='ignore')
    strcontent=strcontent[strcontent.find('<input'):]
    c=str.encode('<html><body>')+str.encode(strcontent)+str.encode('</body></html>')
    root=lxml.html.fromstring(c)
    return root

def add_http(url, main_url):
    return urllib.parse.urljoin(main_url, url)

# set up the logger
logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

# command line parsing
parser = argparse.ArgumentParser(
        description='''download photos from travelgirls'''
)
parser.add_argument(
        '-i',
        '--id', 
        help='''id of the user to download the albums of
        For instance if you see a url like this:
            http://www.travelgirls.com/member/2126319
        then the id for this script will be:
            2126319 
        '''
)
args = parser.parse_args()
if args.id is None:
    parser.error('-i/--id must be given')

# load cookies from browser
cookies=browser_cookie3.firefox()

main_url='http://www.travelgirls.com/member/{id}'.format(id=args.id)
r = requests.get(main_url, cookies=cookies)
root = get_real_content(r)

urls=[]
e_a = root.xpath('//a[contains(@class,\'photo\')]')
for x in e_a:
    print(lxml.etree.tostring(x, pretty_print=True))
    children=x.getchildren()
    assert len(children)==1
    img=children[0]
    url=add_http(img.attrib['src'], main_url)
    url=url.replace('mini','')
    urls.append(url)

cnt=0
logger.info('got [%d] real urls', len(urls))
for url in urls:
    logger.debug(url)
    r=requests.get(url, stream=True)
    assert r.status_code==200
    filename='image{0:04}.jpg'.format(cnt)
    with open(filename, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
    logger.info('written [%s]...', filename)
    cnt+=1
