import dataset 

engine = dataset.connect('postgresql://localhost/fl')
table = engine['articles']

if __name__ == '__main__':
    dataset.freeze(engine.query("SELECT url, news_org, summary, content, title FROM articles"), filename='articles.csv')