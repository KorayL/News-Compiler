from src.site import Site
from src.article import Article

from json import dumps
from src.sites import *

def main():
    article_dict = dict()

    for site in Site.Instances:
        site.get_htmls()
        site.get_titles()
        site.get_dates()
        site.get_image_urls()
        site.get_bodies()
        site.create_articles()

    for i, article in zip(range(0, len(Article.instances)+1), Article.instances):
        article_name = f"{article.source}-{i}"
        article.download_image(f"data/{article_name}.png")
        article_dict[article_name] = article.to_dict()

    # Write articles dictionary to file
    with open("data/articles.json", "w") as file:
        file.write(dumps(article_dict, indent=4))

if __name__ == '__main__':
    main()
