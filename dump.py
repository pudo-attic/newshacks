import dataset
from common import get_engine

engine = get_engine()
table = engine['articles']

if __name__ == '__main__':
    q = engine.query("SELECT url, news_org, summary, content, title FROM articles")
    dataset.freeze(q, filename='articles.csv')
