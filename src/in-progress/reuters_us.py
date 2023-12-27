import re

import bs4
from bs4 import BeautifulSoup
from selenium import webdriver

from src.Site import Site


class reuters_us(Site):
    # @staticmethod
    # def get_html(url) -> BeautifulSoup:
    #     browser = webdriver.Chrome()
    #     browser.get(url)
    #
    #     html_source = browser.page_source
    #     browser.close()
    #
    #     return BeautifulSoup(html_source, "html.parser")

    def set_url(self) -> None:
        self.url = "https://www.reuters.com/world/us/"

    def set_source(self) -> None:
        self.source = "Reuters"

    def set_category(self) -> None:
        self.category = "US News"

    def get_article_urls(self, html: BeautifulSoup) -> list[str]:
        links: list[str] = []

        stories = html.findAll(lambda tag: tag.name == "div" and tag.has_attr("data-testid")
                                           and tag["data-testid"] == "MediaStoryCard", limit=20)

        for story in stories:
            links.append(f"https://reuters.com{story.find('a')['href']}")

        return links

    def get_title(self, html: BeautifulSoup) -> str:
        title = html.find('h1').getText()
        return title

    def get_date(self, html: BeautifulSoup) -> None:
        return

    def get_image_url(self, html: BeautifulSoup) -> str | None:
        try:
            return html.find(class_=re.compile("image-container")).find('img')['src']
        except TypeError:
            return None

    def get_body(self, html: BeautifulSoup) -> list[str]:
        paragraphs: list[str] = []

        paragraph_tags: list[bs4.PageElement] = html.find(
            class_=re.compile("article-body")).findAll('p')

        for tag in paragraph_tags:
            if re.compile("paragraph-\d*"):
                paragraphs.append(tag.getText())

        return paragraphs


if __name__ == "__main__":
    site = reuters_us()
    site.get_article_urls(site.html)
