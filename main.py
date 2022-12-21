import logging
from WebCrawler import WebCrawler
from CNNContentHandler import CNNContentHandler


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

if __name__ == '__main__':
    content_handler = CNNContentHandler()
    WebCrawler(content_handler,
               # urls=['https://edition.cnn.com/sitemap.html'],
               urls=[
                   "https://edition.cnn.com/article/sitemap-2022-01.html",
                   "https://edition.cnn.com/article/sitemap-2022-02.html",
                   "https://edition.cnn.com/article/sitemap-2022-03.html",
                   "https://edition.cnn.com/article/sitemap-2022-04.html",
                   "https://edition.cnn.com/article/sitemap-2022-05.html",
                   "https://edition.cnn.com/article/sitemap-2022-06.html",
                   "https://edition.cnn.com/article/sitemap-2022-07.html",
                   "https://edition.cnn.com/article/sitemap-2022-08.html",
                   "https://edition.cnn.com/article/sitemap-2022-09.html",
                   "https://edition.cnn.com/article/sitemap-2022-10.html",
                   "https://edition.cnn.com/article/sitemap-2022-11.html",
                   "https://edition.cnn.com/article/sitemap-2022-12.html",
               ],
               stop_depth=1,
               save_file="CNN_Articles.csv").run()
