import json
from pprint import pprint
from common import load_article_dict
from gensim import corpora, models, similarities


def similarity(article, other):
    total = 0
    for gram, score in article.items():
        total += abs(score - other.get(gram, 0))
    return total / len(article)


def make_corpus(dic, texts):
    corpus = [dic.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('corpus.mm', corpus)
    #print corpus
    return corpus


def similar_articles(articles, dic):
    print dic
    return
    #for article in articles:
    #    article['dict'] = load_article_dict(article['url'])
    for article in articles:
        scores, seen = [], []
        for other in articles:
            if other.get('og:title') == article.get('og:title') or other.get('og:title') in seen:
                continue
            seen.append(other.get('og:title'))
            scores.append((other, similarity(article, other)))
        scores = sorted(scores, key=lambda (a, b): b)[:3]
        print "\n\nARTICLE:", [article.get('og:title')]
        print "> Best matches:"
        for other, score in scores:
            print "  * %s: %s" % ([other.get('og:title')], score)


if __name__ == '__main__':

    with open('articles.json', 'rb') as fh:
        articles = json.load(fh)
        texts = []
        for article in articles:
            text = article.get('bigrams') + [article.get('url')]
            texts.append(text)
        dic = corpora.Dictionary(texts)
        corpus = make_corpus(dic, texts)
        similar_articles(articles, dic)
        #print len(articles)
