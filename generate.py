import json
from common import get_engine
from tokenize import make_bigrams
from corpora import make_corpora

engine = get_engine()
table = engine['articles']


def generate_texts():
    with open('texts.json', 'wb') as fh:
        texts = []
        for i, article in enumerate(table):
            article['bigrams'] = make_bigrams(article.get('content', ''))
            print [i, len(article['bigrams'])]
            texts.append(article['bigrams'] + [article.get('url')])
        json.dump(texts, fh)
        return texts


def generate_corpora():
    with open('texts.json', 'rb') as fh:
        texts = json.load(fh)
        make_corpora(texts)

if __name__ == '__main__':
    #generate_texts()
    generate_corpora()
