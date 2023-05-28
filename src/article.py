import requests

class Article:
    instances = []

    def __init__(self, source, category, title, date, image_url, body) -> None:
        Article.instances.append(self)

        self.source = source
        self.category = category
        self.title = title
        self.date = date
        self.image_url = image_url
        self.image_path = None
        self.body = body

    def download_image(self, path: str) -> None:
        """
        :param path: location and name to store image
        """

        if self.image_url != "Null":
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
            "image_path": self.image_path,
            "body": self.body
        }
        return article_as_dict
