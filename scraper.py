import csv
import dataset
from StringIO import StringIO
from lxml import html
import requests
import re
import urllib
import uuid
import json
from readability.readability import Document
from urlparse import urljoin
from datetime import datetime

from threads import threaded

engine = dataset.connect('postgresql://localhost/fl')
table = engine['articles']


def get_sources():
    res = requests.get('https://docs.google.com/spreadsheet/pub?key=0An9Q5Mkz4lG7dGt6ZTNZLU03cnZRMkQtMkdaZ1lhd1E&output=csv')
    time = datetime.now().strftime("%s")
    for row in csv.DictReader(StringIO(res.content)):
        base = {'news_org': row['site_name'], 'time': time}
        url = row['site_url']
        doc = html.fromstring(requests.get(url).content)
        links = [a.get('href') for a in doc.findall('.//a')]
        links = [re.sub(url, "", l) for l in links if l is not None]
        links = [urljoin(url, l) for l in links]
        articles = [l for l in links if re.match(row['site_regex'], l)]
        for a in set(articles):
            art = base.copy()
            art.update({'url': a})
            yield art


def get_article(d):
    url = d['url']
    if table.find_one(url=url):
        return
    print "fetching stuff for %s" % url
    d['html'] = requests.get(url).content
    doc = Document(d['html'])
    d['summary'] = html.fromstring(doc.summary()).xpath('string()')
    d['content'] = html.fromstring(doc.content()).xpath('string()')
    d['title'] = doc.title()
    #print d
    #fname = "data/" + uuid.uuid4().hex + ".json"
    table.upsert(d, ['url'])

if __name__ == '__main__':
    for art in get_sources():
        get_article(art)
  #threaded(data, get_article)
