import requests
from pprint import pprint
from lxml import html

URL = 'http://www.nytimes.com/'

def get_articles():
    res = requests.get(URL)
    doc = html.fromstring(res.content)
    urls = set([a.get('href') for a in doc.findall('.//a')])
    for url in urls:
        if url is None:
            continue
        res = requests.get(url)
        art = html.fromstring(res.content)
        metas = [(m.get('name'), m.get('content')) for m in art.findall('.//meta')]
        metas = dict(metas)
        if metas.get('og:type') != 'article':
            continue
        pprint(metas)


if __name__ == '__main__':
    get_articles()
