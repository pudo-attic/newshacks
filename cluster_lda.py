from gensim import corpora, models, similarities
from nltk import WordPunctTokenizer
import re

NUM_TOPICS = 40

stopwords = open('stopwords.txt').read().split('\n')
word_re = re.compile('[a-z0-9\s]+')
tokenizer = WordPunctTokenizer()
tokenize = lambda text: [w.lower()
                         for w in tokenizer.tokenize(text)
                         if re.match(word_re, w.lower()) and w.lower() not in stopwords]

id2word = corpora.Dictionary.load('dictionary.dict')
mm = corpora.MmCorpus('tfidf.mm')
lsi = models.lsimodel.LsiModel(corpus=mm, id2word=id2word, num_topics=NUM_TOPICS)
dic = corpora.Dictionary.load('dictionary.dict')

def get_topics(text, num, model=lsi):
    """ get +num+ topics for text +text+ """
    topics = []

    for t in sorted(model[dic.doc2bow(tokenize(text))],
                    key=lambda t: t[1],
                    reverse=True)[:num]:

        topics.append([u[1] for u in lsi.show_topic(t[0])])

    return topics
