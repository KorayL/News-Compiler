from bs4 import BeautifulSoup

import bs4
from bs4 import BeautifulSoup

from src.Site import Site


class template(Site):
    """
    Creating your own site class is very easy. You must inherit from the Site super class,
    implementing all abstract methods. After that, follow the documentation for each method,
    reading over other implementations to supplement, and you should be good to go.

    The only thing that matters for the abstract methods is that the return type is what is asked
    for. Your implementation can be as creative as it needs to be as long as the return types are
    met.
    """

    def set_url(self) -> None:
        pass

    def set_source(self) -> None:
        pass

    def set_category(self) -> None:
        pass

    def get_article_urls(self, html: BeautifulSoup) -> list[str]:
        pass

    def get_title(self, html: BeautifulSoup) -> str:
        pass

    def get_date(self, html: BeautifulSoup) -> None:
        pass

    def get_image_url(self, html: BeautifulSoup) -> str | None:
        pass

    def get_body(self, html: BeautifulSoup) -> list[str]:
        pass
