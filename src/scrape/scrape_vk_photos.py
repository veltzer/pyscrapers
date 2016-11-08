#!/usr/bin/python3

'''
This script downloads the public vk albums of a vk public vk user.
You need to supply the user id. This is something you see in the
url when you surf the users account at vk.com

For instance if you see a url like this:
    https://vk.com/id[user_id]?z=albums275458801
then the id for this script will be:
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
import scrape.utils # for download_urls

# set up the logger
logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

def get_my_content(r):
    '''
    the return from the server in vk is not a standard HTML.
    this is why we must cut it up and cant use the regular
    'get_real_content' helper.
    '''
    assert r.status_code==200
    #strcontent=r.content.decode(errors='ignore')
    strcontent=r.content.decode()
    strcontent=strcontent[strcontent.find('<input'):]
    c=str.encode('<html><body>')+str.encode(strcontent)+str.encode('</body></html>')
    root=lxml.html.fromstring(c)
    return root

def main():
    # command line parsing
    parser = argparse.ArgumentParser(
            description='''download albums of a vk public user'''
    )
    parser.add_argument(
            '-i',
            '--id', 
            help='''id of the user to download the albums of
            For instance if you see a url like this:
                https://vk.com/id[user_id]?z=albums275458801
            then the id for this script will be:
                [user_id]
            '''
    )
    args = parser.parse_args()
    if args.id is None:
        parser.error('-i/--id must be given')

    owner=args.id
    url='https://vk.com/al_photos.php'
    data={
        'act': 'show_albums',
        'al': '1',
        'owner': owner,
    }
    r = requests.post(url, data = data)
    root=get_my_content(r)

    e_albums = root.xpath('//div[@class="photos_album_title_wrap"]')
    albums=dict()
    for x in e_albums:
        name_of_album=x.getparent().getparent().getparent().getparent().attrib['id'].split('?')[0]
        e_len=x.xpath('.//div[@class="photos_album_counter fl_r"]/text()')
        albums[name_of_album]=int(e_len[0])
    logger.debug(albums)
    total_images=0
    for v in albums.values():
        logger.debug('got [%d] partial images', v)
        total_images+=v
    logger.debug('got [%d] potential images', total_images)

    count=0
    urls=set()
    got=1
    while got:
        got=0
        data={
            'act': 'show_albums',
            'al': '2',
            'owner': owner,
            'offset': count,
        }
        logger.debug('doing request %d', count)
        r = requests.post(url, data = data)
        root=get_my_content(r)
        e_a = root.xpath('//a[@onclick]')
        for x in e_a:
            onclick=x.attrib['onclick']
            if onclick.startswith('return showPhoto'):
                json_str=onclick[onclick.find('{'):onclick.rfind('}')+1]
                # bas string, need fix lots of things...
                json_str=json_str.replace('\'','"')
                json_str=json_str.replace('jumpTo','"jumpTo"')
                json_str=json_str.replace('z:','"z":')
                json_obj=json.loads(json_str)
                base=json_obj['temp']['base']
                if base=='':
                    continue
                largest=0
                largest_url=None
                minlen=min(len(v) for k,v in json_obj['temp'].items() if k.endswith('_'))
                if minlen==3:
                    for k,v in json_obj['temp'].items():
                        if k!='base':
                            size=v[1]*v[2]
                            if size>largest:
                                largest=size
                                largest_url=v[0]
                    full_url=base+largest_url+'.jpg'
                    urls.add(full_url)
                    got+=1
                if minlen==1:
                    for k,v in json_obj['temp'].items():
                        if k!='base':
                                add_url=v[0]
                                full_url=base+add_url+'.jpg'
                                urls.add(full_url)
                    got+=1
        count+=got

    scrape.utils.download_urls(urls)

if __name__ == '__main__':
    main()
