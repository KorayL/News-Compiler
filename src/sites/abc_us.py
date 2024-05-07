import re

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
            date: str = html.find("div", class_="xAPpq JQYD ZdbeE  jTKbV pCRh ").get_text()
        except (AttributeError, ValueError):
            return None

        return self._date_parser_helper(date)

    def get_image_url(self, html: BeautifulSoup) -> str | None:
        try:
            body = html.find(lambda tag: tag.has_attr("data-testid") and tag["data-testid"] == "prism-article-body")
            image_tag = body.find(class_=re.compile("InlineImage"))
            image_url = image_tag.find("img")["src"]
            return image_url

        except (TypeError, AttributeError):
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
    site.create_articles(stacktrace=True)
