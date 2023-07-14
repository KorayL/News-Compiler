from src.article import Article
import requests
from bs4 import BeautifulSoup

from multiprocessing import Pool


class Site:
    Instances = []

    def __init__(self, address, category, source, link_func, title_func, date_func, image_url_func, body_func):
        Site.Instances.append(self)

        self.link_func = link_func
        self.title_func = title_func
        self.date_func = date_func
        self.image_url_func = image_url_func
        self.body_func = body_func

        self.article_htmls = []
        self.article_titles = []
        self.article_dates = []
        self.article_image_urls = []
        self.article_bodies = []

        self.category = category
        self.source = source

        self.site_html = BeautifulSoup(requests.get(address).text, 'html.parser')

    def _get_html(self, link):
        article_html = BeautifulSoup(requests.get(link).text, "html.parser")
        return article_html

    def get_htmls(self):
        links = self.link_func(self.site_html)

        with Pool() as pool:
            self.article_htmls = (pool.map(self._get_html, links))

    def get_titles(self):
        self.article_titles = self._html_loop_wrapper(self.title_func)

    def get_dates(self):
        self.article_dates = self._html_loop_wrapper(self.date_func)

    def get_image_urls(self):
        self.article_dates = self._html_loop_wrapper(self.date_func)

    def get_bodies(self):
        self.article_bodies = self._html_loop_wrapper(self.body_func)

    def create_articles(self):
        for i in range(len(self.article_htmls)):
            Article(self.source, self.category, self.article_titles[i], self.article_dates[i],
                    self.article_image_urls[i], self.article_bodies[i])

    def _html_loop_wrapper(self, func):
        array = []
        for html in self.article_htmls:
            var = func(html)
            array.append(var)

        return array
