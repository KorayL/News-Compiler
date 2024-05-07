from tkinter import messagebox
from json import dumps
import os

from multiprocessing import Pool

from src.Site import Site
from src.sites import *
import src.flask_app as gui


def instantiate(class_: type) -> object:
    """
    Used when multiprocessing to instantiate a class.
    :param class_: The class to instantiate.
    :return: The instantiated class.
    """
    return class_()

def get_sites() -> list[Site]:
    """
    Gets all subclasses of Site and instantiates them.
    :return: The list of instantiated sites.
    """

    print("loading sites...")

    # Instantiate all sites
    with Pool() as pool:
        sites: list[Site] = pool.map(instantiate, Site.__subclasses__())

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
    data_path = os.path.join(os.path.dirname(__file__), "src/static/articles.json")
    with open(data_path, "w") as file:
        file.write(dumps(article_dict, indent=4))


if __name__ == '__main__':
    print("running main")
    try:
        # Only download articles if user wants to
        reload: bool = messagebox.askyesnocancel("Article Download", "Would you like to download the latest articles?")
        if reload:
            main()
        if reload is None:
            exit()

        gui.run()
    except Exception as e:
        messagebox.showerror(title="An error has occurred!", message=str(e))
