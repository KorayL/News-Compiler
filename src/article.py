class Article:
    def __init__(self, category, title, date, image, body):
        self.category = category
        self.title = title
        self.date = date
        self.image = image
        self.body = body

    def to_dict(self):
        article_as_dict = {
            "category": self.category,
            "title": self.title,
            "date": self.date,
            "image_name": self.image,
            "body": self.body
        }
        return article_as_dict
