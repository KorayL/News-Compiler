import re
import time
from datetime import datetime

import bs4
from bs4 import BeautifulSoup

from src.Site import Site


class abc_us(Site):
    """
    Implementation of Site class. This class provides methods for reading through the
    ABC New's United States news.
    """

    def set_url(self) -> None:
        self.url = "https://abcnews.go.com/US"

    def set_source(self) -> None:
        self.source = "ABC News"

    def set_category(self) -> None:
        self.category = "US News"

    def get_article_urls(self, html: BeautifulSoup) -> list[str]:
        links: list[str] = []

        stories: list[bs4.element] = html.findAll(class_="ContentRoll__Item", limit=20)

        for story in stories:
            links.append(story.find("a", class_="AnchorLink")["href"])
        return links

    def get_title(self, html: BeautifulSoup) -> str:
        return html.find("h1").getText()

    def get_date(self, html: BeautifulSoup) -> int | None:
        try:
            date: str = html.find("div", class_="xAPp Zdbe jTKb pCRh").get_text()

            # https://docs.python.org/3/library/time.html#time.strptime
            # December 28, 2023, 7:27 AM
            epoch: int = int(time.mktime(datetime.strptime(date, "%B %d, %Y, %I:%M %p")
                                         .timetuple()))

            return epoch
        except AttributeError or ValueError:
            return None

    def get_image_url(self, html: BeautifulSoup) -> str | None:
        try:
            body = html.find(lambda tag: tag.has_attr("data-testid") and tag["data-testid"] == "prism-article-body")
            image_tag = body.find(class_=re.compile("InlineImage"))
            image_url = image_tag.find("img")["src"]
            return image_url

        except TypeError:
            return None
        except AttributeError:
            return None

    def get_body(self, html: BeautifulSoup) -> list[str]:
        paragraphs: list[str] = []

        body_div: bs4.element = html.find(
            lambda tag: tag.has_attr("data-testid") and tag["data-testid"] == "prism-article-body")
        paragraph_tags: list[bs4.PageElement] = html.findAll("p")

        for tag in paragraph_tags:
            paragraphs.append(tag.getText())

        return paragraphs


if __name__ == "__main__":
    site = abc_us()
    urls = site.get_article_urls(site.html)
    for url in urls:
        # do not print the entire html
        print(url)
        html = site.get_html(url)
        print(site.get_title(html))
        print(site.get_date(html))
        print(site.get_image_url(html))
        print(site.get_body(html))

