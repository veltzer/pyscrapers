from lxml import etree
import lxml.html  # for fromstring
import requests  # for post
import logging  # for basicConfig, getLogger
import shutil  # for copyfileobj
import urllib.parse  # for urljoin
import http.client  # for HTTPConnection

logger = logging.getLogger(__name__)


def print_cookies(cookies, domain):
    print(domain)
    for cookie in cookies:
        print(cookie)


def get_real_content(r):
    assert r.status_code == 200
    '''
    if r.status_code!=200:
        print('got error')
        print(r.content.decode())
        sys.exit(1)
    '''
    str_content = r.content.decode()
    root = lxml.html.fromstring(str_content)
    return root


def download_urls(urls, start=0):
    cnt = start
    logger.info('got [%d] real urls', len(urls))
    for url in urls:
        logger.debug(url)
        r = requests.get(url, stream=True)
        assert r.status_code == 200
        filename = 'image{0:04}.jpg'.format(cnt)
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        logger.info('written [%s]...', filename)
        cnt += 1


def debug_requests():
    http.client.HTTPConnection.debuglevel = 1
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def add_http(url, main_url):
    return urllib.parse.urljoin(main_url, url)


def print_element(e):
    print(etree.tostring(e, pretty_print=True))
