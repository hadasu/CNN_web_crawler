from bs4 import BeautifulSoup
import pandas as pd
import logging


class CNNContentHandler:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.CNN_article = None
        self.dataset = pd.DataFrame()

    def create_empty_article(self):
        self.CNN_article = {'author': '',
                            'date_published': '',
                            'part_of': '',
                            'article_section': '',
                            'url': '',
                            'headline': '',
                            'description': '',
                            'keywords': '',
                            'alternative_headline': '',
                            'text': ''}

    def file_article(self, html):
        is_article = True
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        try:
            self.CNN_article['author'] = soup.find(itemprop="author").attrs['content']
            self.CNN_article['date_published'] = soup.find(itemprop="datePublished").attrs['content']
            self.CNN_article['part_of'] = soup.find(itemprop="isPartOf").attrs['content']
            self.CNN_article['article_section'] = soup.find(itemprop="articleSection").attrs['content']
            self.CNN_article['url'] = soup.find(itemprop="url").attrs['content']
            self.CNN_article['headline'] = soup.find(itemprop="headline").attrs['content']
            self.CNN_article['description'] = soup.find(itemprop="description").attrs['content']
            self.CNN_article['keywords'] = soup.find(itemprop="keywords").attrs['content']
            self.CNN_article['alternative_headline'] = soup.find(itemprop="alternativeHeadline").attrs['content']
            self.CNN_article['text'] = soup.find(id="body-text").text
        except Exception:
            is_article = False
            self.logger.info(f'Missing Article data')

        return is_article

    def add_article(self):
        self.dataset = self.dataset.append(self.CNN_article, ignore_index=True)

    def save_content(self):
        self.dataset.to_csv('CNN_Articles.csv')

    def process_page(self, html):
        self.create_empty_article()
        is_article = self.file_article(html)
        if is_article:
            self.add_article()
