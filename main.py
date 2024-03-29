import tkinter.messagebox as alert
from json import dumps
import os

from src.Site import Site
from src.sites import *
import src.flask_app as gui


def get_sites() -> list[Site]:
    """
    Gets all subclasses of Site and instantiates them.
    :return: The list of instantiated sites.
    """

    print("loading sites...")

    sites: list[Site]
    sites = [site() for site in Site.__subclasses__()]

    return sites


def main():
    # Get a list of instantiated sites
    sites = get_sites()
    # Create dictionary with all articles from all sites
    article_dict: dict = dict()
    for i, site in enumerate(sites):
        print(f"downloading articles from website {i+1} of {len(sites)}")
        site.create_articles()
        article_dict.update(site.to_dict())

    # Write articles dictionary to file
    print("writing articles to file")
    data_path: str = fr"{os.path.realpath(__file__).removesuffix(r"\main.py")}\src\static\articles.json"
    with open(data_path, "w") as file:
        file.write(dumps(article_dict, indent=4))


if __name__ == '__main__':
    print("running main")
    try:
        main()
        gui.run()
    except Exception as e:
        alert.showerror(title="An error has occurred!", message=str(e))
