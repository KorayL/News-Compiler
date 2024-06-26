from tkinter import messagebox
from tkinter import Tk
from json import dumps
import os

from multiprocessing import Pool

from src.Site import Site
from src.sites import *
import src.flask_app as gui
from src.git_tools import pull as check_for_updates
from src.git_tools import initialize as initialize_project


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
    # Setting up repository structure
    if not os.path.exists(".git"):  # Check if .git folder exists
        print("No git repository found...")
        initialize_project()
    else:
        print("Checking for Updates...")
        check_for_updates()

    print("Running News Compiler...")
    try:
        # Only download articles if user wants to
        root = Tk()
        root.withdraw()
        reload: bool = messagebox.askyesnocancel("Article Download", "Would you like to download the latest articles?")
        root.update()
        if reload:
            main()
        if reload is None:
            exit()

        gui.run()
    except Exception as e:
        root = Tk()
        root.withdraw()
        messagebox.showerror(title="An error has occurred!", message=str(e))
        root.update()
