from gensim import corpora, models, similarities


def make_corpus(dic, texts):
    corpus = [dic.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('corpus.mm', corpus)
    #print corpus
    return corpus


def make_tfidf(mm, d):
    return models.TfidfModel(mm, id2word=d, normalize=True)


def make_corpora(texts):
    dic = corpora.Dictionary(texts)
    dic.save('dictionary.dict')
    corpus = make_corpus(dic, texts)
    tfidf = make_tfidf(corpus, dic)
    corpora.MmCorpus.serialize('tfidf.mm', tfidf[corpus], progress_cnt=100)
