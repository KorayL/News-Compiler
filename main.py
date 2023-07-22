from json import dumps

from src.sites import *
from src.site import Site
from src.article import Article


def main():
    article_dict = dict()

    for site in Site.instances:
        print(f"Getting {site.source} Data")
        site.create_articles()
        for article in site.articles:
            try:
                article.get_title()
                article.get_date()
                article.get_image_url()
                article.get_body()
            except Exception as e:
                if e is KeyboardInterrupt:
                    raise e
                else:
                    print(f"{article.title}: {e}")
                    new_article_list = getattr(site, 'articles')
                    new_article_list.remove(article)
                    setattr(site, 'articles', new_article_list)

                    new_article_list = getattr(Article, 'instances')
                    new_article_list.remove(article)
                    setattr(Article, 'instances', new_article_list)

    # Download and save images from articles
    print("\nDownloading Images...")
    for site in Site.instances:
        for i, article in enumerate(site.articles):
            article_name = f"{article.source}-{i}"
            article.download_image(f"data/{article_name}.png")

    # Create dictionaries from articles
    print("Creating Dictionaries...")
    for site in Site.instances:
        for i, article in enumerate(site.articles):
            article_name = f"{article.source}-{i}"
            article_dict[article_name] = article.to_dict()

    # Write articles dictionary to file
    print("Writing Dictionaries to file...")
    with open("data/articles.json", "w") as file:
        file.write(dumps(article_dict, indent=4))


if __name__ == '__main__':
    main()
