import re

import bs4
from bs4 import BeautifulSoup

from src.Site import Site


class ap_us(Site):
    def set_url(self) -> None:
        self.url = "https://apnews.com/hub/us-news"

    def set_source(self) -> None:
        self.source = "Associated Press (AP)"

    def set_category(self) -> None:
        self.category = "US News"

    def get_article_urls(self, html: BeautifulSoup) -> list[str]:
        urls: list[str] = []

        content: bs4.element = html.find('div', class_="Page-content")
        stories: list[bs4.element] = content.findAll(class_="PageList-items-item", limit=20)
        for story in stories:
            urls.append(story.find('a')['href'])

        return urls

    def get_title(self, html: BeautifulSoup) -> str:
        return html.find('h1').getText()

    def get_date(self, html: BeautifulSoup) -> None:
        return

    def get_image_url(self, html: BeautifulSoup) -> str | None:
        try:
            # Try to get image
            page_lead = html.find("div", class_=re.compile("Page-lead"))
            image_url = page_lead.find("img")["src"]

            # If image not returned
            if "https" not in image_url:
                # Try to get image from carousel
                carousel_media = page_lead.find("div", class_="CarouselSlide-media")
                image_url = carousel_media.find("source")["data-flickity-lazyload-srcset"]

                # Image links may be chained together or have extraneous characters, only take before the first space
                i = image_url.index(" ")
                image_url = image_url[0:i]

            # Return image if image has been retrieved, None otherwise
            return image_url if "http" in image_url else None
        except Exception as e:
            if e is KeyboardInterrupt:
                raise e

            return None

    def get_body(self, html: BeautifulSoup) -> list[str]:
        body: list[str] = []

        paragraph_div = html.find(class_=re.compile("RichTextBody")).findAll('p')

        for tag in paragraph_div:
            body.append(tag.getText())

        return body


if __name__ == "__main__":
    site = ap_us()
    site.create_articles()
    print(site.to_dict())
