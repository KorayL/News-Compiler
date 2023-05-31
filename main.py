from src.site import Site
from src.article import Article

from json import dumps
from src.sites import *

def main():
    article_dict = dict()

    # Run all Site methods
    for site in Site.Instances:
        print(f"Getting {site.source} HTMLs")
        site.get_htmls()
        print("Getting Article Information...")
        site.get_titles()
        site.get_dates()
        site.get_image_urls()
        site.get_bodies()
        site.create_articles()

    # Download and save images from articles
    print("Downloading Images...")
    for i, article in zip(range(0, len(Article.instances)+1), Article.instances):
        article_name = f"{article.source}-{i}"
        article.download_image(f"data/{article_name}.png")

    # Create dictionaries from articles
    print("Creating Dictionaries...")
    for i, article in zip(range(0, len(Article.instances)), Article.instances):
        article_name = f"{article.source}-{i}"
        article_dict[article_name] = article.to_dict()

    # Write articles dictionary to file
    print("Writing Dictionaries to file...")
    with open("data/articles.json", "w") as file:
        file.write(dumps(article_dict, indent=4))

if __name__ == '__main__':
    main()
