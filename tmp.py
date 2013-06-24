from gensim import corpora, models, similarities

NUM_TOPICS = 100

id2word = corpora.Dictionary.load('dictionary.dict')
mm = corpora.MmCorpus('tfidf.mm')
lsi = models.lsimodel.LsiModel(corpus=mm, id2word=id2word, num_topics=NUM_TOPICS)
print dir(lsi)
lsi.save('model.lsi')
print lsi.print_topics(NUM_TOPICS)

index = similarities.MatrixSimilarity(lsi[mm])
index.save('matrix.index')

#index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')
