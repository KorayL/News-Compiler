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

        stories: list[bs4.element] = html.findAll(class_="ContentList__Item", limit=20)

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
            return html.find(lambda tag: tag.name == "img" and tag.has_attr("data-testid") and
                             tag["data-testid"] == "prism-image")["src"]
        except TypeError:
            return None

    def get_body(self, html: BeautifulSoup) -> list[str]:
        paragraphs: list[str] = []

        paragraph_tags: list[bs4.PageElement] = html.findAll(class_=re.compile("Ekqk nlgH yuUa"))

        for tag in paragraph_tags:
            paragraphs.append(tag.getText())

        return paragraphs


if __name__ == "__main__":
    site = abc_us()
    urls = site.get_article_urls(site.html)
    # print(urls)
    html = site.get_html(urls[0])
    # print(html.prettify())
    date = site.get_date(html)
    # print(date)

