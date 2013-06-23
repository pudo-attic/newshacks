import json
from guhp import get_articles
from nltk.tokenize import WordPunctTokenizer
from freq import tf_idf
from normalize import normalize

STOPWORDS = open('stopwords.txt').read().split()
#print STOPWORDS


def tokens_to_bigrams(tokens):
    last_token = None
    for token in tokens:
        if last_token is not None:
            yield '%s_%s' % (last_token, token)
        last_token = token


def make_bigrams(text):
    tokens = WordPunctTokenizer().tokenize(text)
    tokens = filter(lambda t: len(t), map(normalize, tokens))
    tokens = [t for t in tokens if t not in STOPWORDS]
    bigrams = list(tokens_to_bigrams(tokens))
    return bigrams


def freqs(article, articles):
    grams = {}
    for gram in set(article):
        grams[gram] = tf_idf(gram, article, articles)
    return grams


if __name__ == '__main__':
    articles = []
    print "Loading and tokenizing articles..."
    for article in get_articles():
        article['bigrams'] = make_bigrams(article.get('text'))
        articles.append(article)
    print "Generating term frequencies..."
    articles_grams = [a.get('bigrams') for a in articles]
    for article in articles:
        article['freqs'] = freqs(article.get('bigrams'), articles_grams)
    with open('articles.json', 'wb') as fh:
        json.dump(articles, fh)
    #print len(articles)
