import logging
import sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class WebCrawler:

    def __init__(self, content_handler, urls=[], stop_depth=sys.maxsize):
        self.logger = logging.getLogger(__name__)
        self.content_handler = content_handler
        self.stop_depth = stop_depth
        self.visited_urls = []
        self.urls_to_visit = [(url, 0) for url in urls]

    def download_url_text(self, url):
        return requests.get(url).text

    def get_urls_links(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url[1] <= self.stop_depth:
            if url[0] not in self.visited_urls and url not in self.urls_to_visit:
                self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url_text(url[0])
        self.content_handler.process_page(html)
        for curr_url in self.get_urls_links(url[0], html):
            self.add_url_to_visit((curr_url, url[1] + 1))

    def run(self):
        while self.urls_to_visit:
            curr_url = self.urls_to_visit.pop(0)
            self.logger.info(f'Crawling: {curr_url[0]}, Depth: {curr_url[1]}')
            try:
                self.crawl(curr_url)
            except Exception:
                self.logger.exception(f'Exception crawl: {curr_url[0]},  Depth: {curr_url[1]}')
            finally:
                self.visited_urls.append(curr_url[0])

        self.content_handler.save_content()
