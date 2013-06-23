#from nltk.tokenize.regexp import WordPunctTokenizer
from normalize import normalize
#from common import save_article_dict

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
