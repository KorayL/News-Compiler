import re

from src.site import Site


def get_links(site_html):
    links = []
    stories = site_html.findAll('div', class_=re.compile("FeedCard"), limit=5)
    for story in stories:
        links.append(f"https://apnews.com{story.find('a')['href']}")
    return links


def get_titles(html):
    title = html.find('h1').getText()
    return title


def get_dates(html):
    date = html.find(class_=re.compile("Timestamp Component")).getText()
    return date


def get_image_urls(html):
    try:
        image_url = html.find(class_=re.compile("LeadFeature")).find('img')['src']
    except TypeError:
        image_url = None
    except AttributeError:
        image_url = None
    return image_url


def get_bodies(html):
    body = ""
    paragraph_tags = html.findAll('p', class_=re.compile("Component-root"))
    for tag in paragraph_tags:
        body += tag.getText() + "\n"
    return body


address = "https://apnews.com/hub/us-news"
Site(address, "us-news", "Associated Press (AP)", get_links, get_titles, get_dates, get_image_urls,
     get_bodies)
