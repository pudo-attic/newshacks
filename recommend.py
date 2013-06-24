import json
import requests
from urlparse import urlparse
from lxml import html
from readability.readability import Document
from common import get_engine
from tokenize import make_bigrams
from corpora import make_corpora
from gensim import corpora, models, similarities

engine = get_engine()
table = engine['articles']

index = similarities.MatrixSimilarity.load('matrix.index')
dictionary = corpora.Dictionary.load('dictionary.dict')
corpus = corpora.MmCorpus('corpus.mm')
lsi = models.lsimodel.LsiModel.load('model.lsi')

ARTICLES = {}

for i, article in enumerate(table):
        ARTICLES[i] = article

def recommend_by_url(url):
    parsed = urlparse(url)
    doc = Document(requests.get(url).content)
    content = html.fromstring(doc.content()).xpath('string()')
    bigrams = make_bigrams(content)
    vec_bow = dictionary.doc2bow(bigrams)
    vec_lsi = lsi[vec_bow]
    sims = index[vec_lsi]
    #print sims
    docs = sorted(list(enumerate(sims)), key=lambda item: -item[1])
    results, seen = [], []
    for doc, score in docs:
        res = ARTICLES[doc]
        if not 'url' in res or res['url'] in seen:
            continue
        seen.append(res['url'])
        p = urlparse(res['url'])
        if p.hostname.endswith(parsed.hostname):
            continue
        res['score'] = float(score)
        if 'content' in res:
            del res['content']
        if 'html' in res:
            del res['html']
        if res['summary']:
            res['summary'] = res['summary'].strip()
        results.append(res)
        if len(results) > 14:
            break
    return results


if __name__ == '__main__':
    #generate_texts()
    print recommend_by_url('http://www.spiegel.de/politik/ausland/edward-snowden-beantragt-asyl-in-ecuador-a-907424.html')
