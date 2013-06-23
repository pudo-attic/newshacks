from gensim import corpora, models, similarities

NUM_TOPICS = 50

id2word = corpora.Dictionary.load('dictionary.dict')
mm = corpora.MmCorpus('tfidf.mm')
lsi = models.lsimodel.LsiModel(corpus=mm, id2word=id2word, num_topics=NUM_TOPICS)
print lsi.print_topics(NUM_TOPICS)
