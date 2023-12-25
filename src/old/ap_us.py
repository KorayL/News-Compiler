import re

from src.Site import Site


def get_links(site_html):
    links = []
    stories = site_html.findAll('div', class_="PageList-items-item", limit=10)
    for story in stories:
        links.append(f"https://apnews.com/{story.find('a')['href']}")
    return links


def get_titles(html):
    title = html.find('h1').getText()
    return title


def get_dates(html):
    date = html.find(class_=re.compile("Page-datePublished")).find("span").getText()
    return date


def get_image_urls(html):
    try:
        image_url = html.find(class_=re.compile("Page-lead")).find('img')['src']
    except Exception as e:
        if e is KeyboardInterrupt:
            raise e
        image_url = None

    if "https" not in image_url:
        image_url = None
    return image_url


def get_bodies(html):
    body = ""
    paragraph_div = html.find(class_=re.compile("RichTextBody")).findAll('p')
    for tag in paragraph_div:
        body += tag.getText() + "\n"
    return body


address = "https://apnews.com/hub/us-news"
Site(address, "US News", "Associated Press (AP)", get_links, get_titles, get_dates, get_image_urls,
     get_bodies)
