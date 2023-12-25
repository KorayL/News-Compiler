import re

import bs4
from bs4 import BeautifulSoup

from src.Site import Site


class abc_us(Site):
    def set_url(self) -> None:
        self.url = "https://abcnews.go.com/US"

    def set_source(self) -> None:
        self.source = "US News"

    def set_category(self) -> None:
        self.category = "ABC News"

    def get_article_urls(self, html: BeautifulSoup) -> list[str]:
        links: list[str] = []

        stories: list[bs4.PageElement] = html.findAll(class_="ContentList__Item", limit=20)

        for story in stories:
            links.append(story.find("a", class_="AnchorLink")["href"])
        return links

    def get_title(self, html: BeautifulSoup) -> str:
        return html.find("h1").getText()

    def get_date(self, html: BeautifulSoup) -> None:
        return

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
