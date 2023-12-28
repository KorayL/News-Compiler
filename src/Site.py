from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from src.Article import Article


class Site(ABC):
    """
    Abstract class that represents a news website containing several articles. This class
    contains necessary methods to get information from all articles on a specific news website.
    If an exception is thrown from one of the abstract methods when pulling information from an
    article's website, that article will be skipped (not included).
    """

    def __init__(self) -> None:
        """ Initializes the site. Gets all necessary attributes. Some attributes may need to be
         retrieved/set separately. """

        self.articles: list[Article] = []
        """ List of all articles associated with this news website. """

        self.url: str = ""
        """ Stores the URL to the news website from which all articles are extracted from. """
        self.source: str = ""
        """ Stores the source where the article was pulled from. """
        self.category: str = ""
        """ Category the article falls into (ex: world news, politics, space, etc.) """

        self.html: BeautifulSoup = None
        """ The HTML belonging to this site. """

        self.set_url()
        self.set_source()
        self.set_category()

        print("\tdownloading website HTMl")
        self.html = self.get_html(self.url)

    def create_articles(self):
        """ Populates the list of articles for this news website. """

        urls = self.get_article_urls(self.html)

        for url in urls:
            print(f"\textracting information from article: {url}")
            # Use abstract methods to get all necessary information
            html = self.get_html(url)
            title = self.get_title(html)
            image_url = self.get_image_url(html)
            body = self.get_body(html)
            date = self.get_date(html)

            # Create one string from body with special characters between all paragraphs
            # format must be recognized by js code.
            formatted_body: str = "\n\n".join(body)

            # Create article
            article: Article = Article(url, title, image_url, formatted_body, self.source,
                                       self.category, date)

            # Add article to list of articles
            self.articles.append(article)

    def to_dict(self) -> dict:
        """
        Creates a dictionary of articles from the articles created from the source news website.
        :return: Dictionary of articles.
        """
        article_dict: dict = dict()

        for i, article in enumerate(self.articles):
            name = f"{article.source}-{i}"
            article_dict[name] = article.to_dict()

        return article_dict

    @staticmethod
    def get_html(url) -> BeautifulSoup:
        """ Gets the BeautifulSoup HTML of this website. """

        return BeautifulSoup(requests.get(url).text, 'html.parser')

    @abstractmethod
    def set_url(self) -> None:
        """ Sets the URL to the news website. This is the URL from which all articles will be
         obtained from. The URL is what the user would be visiting if this application did not
         exist. \n
         Implementation is simple: self.url=''. """
        pass

    @abstractmethod
    def set_source(self) -> None:
        """ Sets what real website this site object represents. The site it not used for any
        functional purpose-it simply informs the user where the article is coming from. Check
        other Site object implementations or run the application to find examples. \n
        Implementation is simple: self.source=''. """
        pass

    @abstractmethod
    def set_category(self) -> None:
        """ Sets the category of news this website provides. The category may be used to group
        articles together. Check other Site object implementation to see what 'conventions'
        to follow. \n
        Implementation is simple: self.category=''. """
        pass

    @abstractmethod
    def get_article_urls(self, html: BeautifulSoup) -> list[str]:
        """
        Gets links for individual articles from the HTML of the news website.
        :param html: BeautifulSoup object of the HTML of the news website.
        :return: A list of links to articles.
        """
        pass

    @abstractmethod
    def get_title(self, html: BeautifulSoup) -> str:
        """
        Gets title of the article. Needs to work for each article obtained from running
        get_article_urls().
        :param html: BeautifulSoup object of the article HTML of the article.
        :return: The title of the article.
        """
        pass

    @abstractmethod
    def get_date(self, html: BeautifulSoup) -> None:
        """ TODO: update method with datetime object return type. """
        pass

    @abstractmethod
    def get_image_url(self, html: BeautifulSoup) -> str | None:
        """
        Gets the URL of the article's image. each article obtained from running
        get_article_urls(). It is okay if an article has no associated image. \n
        Highly recommend considering try/except statements in this method: some websites will
        have articles without images, have articles with videos, or have articles with carousels.
        In these cases, if an exception is thrown from this method, the entire article will be
        skipped. An except clause that returns "None" will allow the article to be included
        without an image.
        :param html: BeautifulSoup object of the article HTML of the article.
        :return: URL to the image that represents the article or None with the article does not
        have an image.
        """
        pass

    @abstractmethod
    def get_body(self, html: BeautifulSoup) -> list[str]:
        """
        Gets the body of the article. Needs to work for each article obtained from running
        get_article_urls().
        :param html: BeautifulSoup object of the article HTML of the article.
        :return: A list of string. Each element represents one paragraph in the body.
        """
        pass
