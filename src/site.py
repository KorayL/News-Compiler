from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

from src.article import Article


class Site:
    instances = []

    def __init__(self, address: str, category: str, source: str,
                 link_func, title_func, date_func, image_url_func, body_func):
        Site.instances.append(self)

        self.link_func = link_func
        """ Function to pull all articles from news site """
        self.title_func = title_func
        """ Function to pull article titles from news site """
        self.date_func = date_func
        """ Function to pull article dates from news site """
        self.image_url_func = image_url_func
        """ Function to pull image urls from news site """
        self.body_func = body_func
        """ Function to pull article bodys from news site """

        self.source = source
        """ Stores the source where the article was pulled from """
        self.category = category
        """ Category the article falls into (ex: world news, politics, space, etc.) """

        self.articles: list = []
        """ List of all articles associated with this class """

        self.site_html = BeautifulSoup(requests.get(address).text, 'html.parser')

    @staticmethod
    def _get_html(link) -> BeautifulSoup:
        """
        Pulls the html of a website
        :param link: Address to the website to pull html from
        :return: BeautifulSoup object of the html from the website
        """

        article_html = BeautifulSoup(requests.get(link).text, "html.parser")
        return article_html

    def create_articles(self):
        links = self.link_func(self.site_html)

        with Pool() as pool:
            article_htmls = (pool.map(self._get_html, links))

        for html in article_htmls:
            self.articles.append(
                Article(html, self.category, self.source,
                        self.title_func, self.date_func, self.image_url_func, self.body_func)
            )
