from bs4 import BeautifulSoup
import pandas as pd
import logging


class CNNContentHandler:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.CNN_article = None
        self.dataset = pd.DataFrame()

    def create_empty_article(self):
        self.CNN_article = {
            'author': '',
            'date_published': '',
            'date_modified': '',
            'article_section': '',
            'url': '',
            'headline': '',
            'description': '',
            'keywords': '',
            'text': ''
        }

    def file_article(self, html):
        is_article = True
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()

        page_type = soup.find("meta", {"name": "type"})
        if not page_type or page_type.attrs['content'] != "article":
            self.logger.info(f'Page is not of type "article". Actual type is: {page_type[:10] if page_type is str else None}')
            return False

        try:
            self.CNN_article['author'] = soup.find("meta", {"name": "author"}).attrs['content'].strip()
            self.CNN_article['date_published'] = soup.find("meta", {"property": "article:published_time"}).attrs['content'].strip()
            self.CNN_article['date_modified'] = soup.find("meta", {"property": "article:modified_time"}).attrs['content'].strip()
            self.CNN_article['article_section'] = soup.find("meta", {"name": "meta-section"}).attrs['content']
            self.CNN_article['url'] = soup.find("meta", {"property": "og:url"}).attrs['content']
            self.CNN_article['headline'] = soup.find("h1", {"data-editable": "headlineText"}).text.strip()
            self.CNN_article['description'] = soup.find("meta", {"name": "description"}).attrs['content'].strip()
            self.CNN_article['keywords'] = soup.find("meta", {"name": "keywords"}).attrs['content'].strip()
            self.CNN_article['text'] = soup.find(itemprop="articleBody").text.strip()
        except Exception as err:
            is_article = False
            self.logger.info(f'Missing Article dataError: {err}')
            for k, v in self.CNN_article.items():
                self.logger.info(f"{k}: {None if not v else v[:10] + '...'}")
            self.logger.info(f'Missing Article dataError: {err}')

        return is_article

    def add_article(self):
        self.dataset = self.dataset.concat(self.CNN_article, ignore_index=True)

    def save_content(self, filename):
        self.dataset.to_csv(filename)

    def process_page(self, html):
        self.create_empty_article()
        is_article = self.file_article(html)
        if is_article:
            self.add_article()
