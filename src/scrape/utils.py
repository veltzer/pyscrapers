import lxml.html # for fromstring
import lxml.etree # for tostring
import requests # for post
import logging # for basicConfig, getLogger
import shutil # for copyfileobj

logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

def get_real_content(r):
    assert r.status_code==200
    strcontent=r.content.decode()
    root=lxml.html.fromstring(strcontent)
    return root

def download_urls(urls):
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

def debug_requests():
    http.client.HTTPConnection.debuglevel=1
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

def add_http(url, main_url):
    return urllib.parse.urljoin(main_url, url)
