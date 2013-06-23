import json
from pprint import pprint


def similarity(article, other):
    total = 0
    for gram, score in article.items():
        total += abs(score - other.get(gram, 0))
    return total / len(article)


def similar_articles(articles):
    for article in articles:
        scores, seen = [], []
        for other in articles:
            if other.get('og:title') == article.get('og:title') or other.get('og:title') in seen:
                continue
            seen.append(other.get('og:title'))
            scores.append((other, similarity(article.get('freqs'),
                           other.get('freqs'))))
        scores = sorted(scores, key=lambda (a, b): b)[:3]
        print "\n\nARTICLE:", [article.get('og:title')]
        print "> Best matches:"
        for other, score in scores:
            print "  * %s: %s" % ([other.get('og:title')], score)


if __name__ == '__main__':
    with open('articles.json', 'rb') as fh:
        articles = json.load(fh)
        similar_articles(articles)
        #print len(articles)
