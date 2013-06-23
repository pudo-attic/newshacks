import json, re
from pprint import pprint
from common import load_article_dict
from gensim import corpora, models, similarities
from nltk.tokenize import WordPunctTokenizer

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

def make_tfidf(mm, d):
    return models.TfidfModel(mm, id2word=d, normalize=True)


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
1


if __name__ == '__main__':

    word_re = re.compile('[a-z0-9\s]+')
    stopwords = open('stopwords.txt').read().split('\n')
    with open('articles.json', 'rb') as fh:
        articles = json.load(fh)
        texts = []
        tokenizer = WordPunctTokenizer()
        for article in articles:
           texts.append([w
                         for w in tokenizer.tokenize(article.get('text'))
                         if re.match(word_re, w) and w not in stopwords])

        dic = corpora.Dictionary(texts)
        dic.save('dictionary.dict')
        corpus = make_corpus(dic, texts)
        tfidf = make_tfidf(corpus, dic)
        corpora.MmCorpus.serialize('tfidf.mm', tfidf[corpus], progress_cnt=100)
