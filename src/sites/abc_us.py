import re

from src.site import Site


def get_links(site_html):
    links = []
    stories = site_html.findAll(class_="ContentList__Item", limit=10)
    for story in stories:
        links.append(story.find("a", class_="AnchorLink")["href"])
    return links


def get_titles(html):
    title = html.find("h1").getText()
    return title


def get_dates(html):
    date = html.find(class_=re.compile("Zdbe  aiPa"))
    if date is None:
        return "No Date Found"
    return date


def get_image_urls(html):
    try:
        image_url = html.find(lambda tag: tag.name == "img" and tag.has_attr("data-testid") and
                              tag["data-testid"] == "prism-image")["src"]
    except TypeError:
        image_url = None

    return image_url


def get_bodies(html):
    body = ""
    paragraph_tags = html.findAll(class_="Ekqk yuUa lqtk TjIX aGjv")
    for tag in paragraph_tags:
        body += tag.getText() + "\n\n"
    return body


address = "https://abcnews.go.com/US"
Site(address, "US News", "ABC News", get_links, get_titles, get_dates, get_image_urls, get_bodies)
