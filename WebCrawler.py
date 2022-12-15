import logging
import sys
from collections import OrderedDict
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


class WebCrawler:

    def __init__(self, content_handler, save_file="CNN_Articles.csv", urls=None, stop_depth=sys.maxsize):
        self.logger = logging.getLogger(__name__)
        self.content_handler = content_handler
        self.save_file = save_file
        self.stop_depth = stop_depth
        self.visited_urls = set()
        self.urls_to_visit = OrderedDict([(x, 0) for x in urls])

    def download_url_text(self, url):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36",
            "Upgrade-Insecure-Requests": "1", "DNT": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
        source_code = requests.get(url, headers=headers)
        source_code.raise_for_status()
        return source_code.text

    def get_urls_links(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if not path:
                continue
            if path.startswith('/'):
                path = urljoin(url, path)
            if not path.startswith('https://edition.cnn.com/'):
                continue
            yield path

    def add_url_to_visit(self, url):
        if url[1] <= self.stop_depth:
            if url[0] not in self.visited_urls:
                self.urls_to_visit[url[0]] = url[1]

    def crawl(self, url):
        html = self.download_url_text(url[0])
        self.content_handler.process_page(html)
        for curr_url in self.get_urls_links(url[0], html):
            self.add_url_to_visit((curr_url, url[1] + 1))

    def run(self):
        try:
            while self.urls_to_visit:
                curr_url = self.urls_to_visit.popitem(last=False)
                self.logger.info(f'Crawling: {curr_url[0]}, Depth: {curr_url[1]}, Remaining urls: {len(self.urls_to_visit)}')
                try:
                    self.crawl(curr_url)
                except Exception as err:
                    self.logger.exception(f'Exception crawl: {curr_url[0]},  Depth: {curr_url[1]}, Error: {err}')
                finally:
                    self.visited_urls.add(curr_url[0])
        except KeyboardInterrupt:
            user_input = input(f"\n\nKeyboard interrupt, do you want to save content in {self.save_file}? (Y/n): ")
            if user_input.lower() in ["no", "n"]:
                return
            pass
        self.content_handler.save_content(self.save_file)
