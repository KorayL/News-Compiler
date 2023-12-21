import requests


class Article:
    instances = []

    def __init__(self, html, category: str, source: str, title_func, date_func, image_url_func, body_func) -> None:
        Article.instances.append(self)

        self.title_func = title_func
        """ Function to pull article title """
        self.date_func = date_func
        """ Function to pull article date """
        self.image_url_func = image_url_func
        """ Function to pull image url """
        self.body_func = body_func
        """ Function to pull article body """

        self.html = html
        """ Stores the  """
        self.source = source
        """ Stores the source where the article was pulled from """
        self.category = category
        """ Category the article falls into (ex: world news, politics, space, etc.) """
        self.title = None
        """ Title of the article """
        self.date = None
        """ Date at which the article was published or updated """
        self.image_url = None
        """ URL to the main image representing the article """
        self.image_path = None
        """ Relative path on loca   l machine """
        self.body = None
        """ Long string containing entirety of article contents """

    def get_title(self) -> str:
        self.title = self.title_func(self.html)
        return self.title

    def get_date(self) -> str:
        self.date = self.date_func(self.html)
        return self.date

    def get_image_url(self) -> str:
        self.image_url = self.image_url_func(self.html)
        return self.image_url

    def get_body(self) -> str:
        self.body = self.body_func(self.html)
        return self.body

    def download_image(self, path: str) -> None:
        """
        :param path: location and name to store image
        """

        if self.image_url is not None:
            self.image_path = path
            image = requests.get(self.image_url).content
            with open(path, 'wb') as file:
                file.write(image)

    def to_dict(self) -> dict:
        """
        Stores all article data in a dictionary \n
        :returns dictionary with all article data
        """

        article_as_dict = {
            "source": self.source,
            "category": self.category,
            "title": self.title,
            "date": self.date,
            "image_url": self.image_url,
            "image_path": self.image_path,
            "body": self.body
        }
        return article_as_dict
