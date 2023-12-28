class Article:
    """ Represents an article with necessary information scraped from a news website. """

    def __init__(self, url: str, title: str, image_url: str, body: str, source: str, category: str,
                 date: str) -> None:
        """
        Initializes an article.
        :param url:
        :param title: The title of the article.
        :param image_url: URL to the image obtained from the scraped website.
        :param body: Body of the article.
        :param source: Where the article came from.
        :param category: What is this article about? This is how it will be sorted later.
        :param date: The date associated with the article from the scraped site. Can be None if
        no date found.
        """

        self.url: str = url
        """ Link to the article from the original website. """
        self.title: str = title
        """ The title of the article. """
        self.image_url: str = image_url
        """ URL to the image obtained from the scraped website. """
        self.body: str = body
        """ Body of the article. """
        self.source: str = source
        """ Where the article came from. """
        self.category: str = category
        """ What is this article about? This is how it will be sorted later. """
        self.date: str = date
        """ The date associated with the article from the scraped site. 
        Can be None if no date found. """
        self.dict = None
        """ Dictionary containing all article information. To be put in json data file. """

    def to_dict(self) -> dict:
        """
        Stores all article data in a dictionary.
        :return: dictionary with all article data.
        """

        if self.dict is None:
            dictionary = {
                "url": self.url,
                "title": self.title,
                "image_url": self.image_url,
                "body": self.body,
                "source": self.source,
                "epoch": self.date,
                "category": self.category,
            }
            self.dict = dictionary

        return self.dict
