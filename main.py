import logging
from WebCrawler import WebCrawler
from CNNContentHandler import CNNContentHandler


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

if __name__ == '__main__':
    content_handler = CNNContentHandler()
    WebCrawler(content_handler,
               urls=['https://edition.cnn.com/sitemap.html'],
               stop_depth=3).run()
