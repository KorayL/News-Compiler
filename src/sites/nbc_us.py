import re
import time
import traceback
from datetime import datetime

import bs4
from bs4 import BeautifulSoup

from src.Site import Site


class nbc_us(Site):
    """
    Implementation of Site class. This class provides methods for reading through the
    NBC New's United States news.
    """

    def set_url(self) -> None:
        self.url = "https://www.nbcnews.com/us-news"

    def set_source(self) -> None:
        self.source = "NBC News"

    def set_category(self) -> None:
        self.category = "US News"

    def get_article_urls(self, html: BeautifulSoup) -> list[str]:
        urls: list[str] = []

        tags: list[bs4.element] = html.find_all(lambda thing: thing.name == "a" and thing.has_attr("href") and
                                                thing["href"].startswith("https://www.nbcnews.com/news/us-news"))

        # First one is always wrong, it is an affiliates link: remote it
        tags.pop(0)

        # Remove duplicates
        tags = list(dict.fromkeys(tags))

        for tag in tags:
            urls.append(tag["href"])

        return urls

    def get_title(self, html: BeautifulSoup) -> str:
        return html.find("h1", class_=re.compile("hero-headline")).getText()

    def get_date(self, html: BeautifulSoup) -> int | None:
        try:
            date: str = html.find(class_=re.compile("mb[0-9]")).find("time")["datetime"]
            date = date.split(".")[0] + date[-1]

            # https://docs.python.org/3/library/time.html#time.strptime
            # December 28, 2023, 7:27 AM
            epoch: int = int(time.mktime(datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").timetuple()))

            return epoch
        except (AttributeError, ValueError):
            return None

    def get_image_url(self, html: BeautifulSoup) -> str | None:
        try:
            # Try to get from main header
            image_url = html.find(class_=re.compile("hero.*container", flags=re.IGNORECASE)).find("img")["src"]
        except (AttributeError, TypeError):
            # Try to get image from article body
            try:
                image_url = html.find(class_=re.compile("inline.*image", flags=re.IGNORECASE)).find("img")["src"]
            except (AttributeError, TypeError):
                return None

        return image_url

    def get_body(self, html: BeautifulSoup) -> list[str]:
        paragraphs: list[str] = []

        body_div: bs4.element = html.find(class_=re.compile("article-body"))
        paragraph_tags: list[bs4.PageElement] = body_div.find_all("p")

        for tag in paragraph_tags:
            paragraphs.append(tag.getText())

        return paragraphs


if __name__ == "__main__":
    """ Use this for testing. It will not run when imported. """
    t = nbc_us()
    t.create_articles(stacktrace=True)
