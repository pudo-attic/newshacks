from common import get_engine

engine = get_engine()
table = engine['articles']


def generate():
    for article in table:
        print article


if __name__ == '__main__':
    generate()
