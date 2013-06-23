import os
import hashlib
import requests
from urlparse import urljoin
from pprint import pprint
from lxml import html

URL = 'http://www.guardiannews.com/'
CACHE_DIR = '.cache'
STOPKEYS = ['twitter:', 'msapplication', 'fb:', 'application-name', 'DC.date']


def buffered_get(url):
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    path = os.path.join(CACHE_DIR, hashlib.sha1(url).hexdigest())
    if os.path.isfile(path):
        with open(path, 'rb') as fh:
            return fh.read()
    with open(path, 'wb') as fh:
        res = requests.get(url)
        fh.write(res.content)
        return res.content


def get_article(url):
    art = html.fromstring(buffered_get(url))
    metas = [(m.get('name', m.get('property')), m.get('content')) for m in art.findall('.//meta')]
    for key in STOPKEYS:
        metas = [(k, v) for k, v in metas if k is not None and key not in k]
    data = dict(metas)
    data['url'] = url
    if data.get('og:type') != 'article':
        return
    body = art.find('.//div[@id="article-body-blocks"]')
    if body is None:
        return
    data['text'] = body.xpath('string()')
    #pprint(data)
    return data


def get_articles():
    res = requests.get(URL)
    doc = html.fromstring(res.content)
    urls = set([urljoin(URL, a.get('href')) for a in doc.findall('.//a')])
    seen = []
    for url in urls:
        if url is None:
            continue
        try:
            art = get_article(url)
            if art is not None:
                if art.get('url') is not seen:
                    yield art
                else:
                    seen.append(art.get('url'))
        except Exception, e:
            print e

if __name__ == '__main__':
    get_articles()
