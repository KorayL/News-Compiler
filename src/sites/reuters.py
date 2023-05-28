from src.site import Site
import re

def get_links(site_html):
    links = []
    divs = site_html.findAll('div')
    for div in divs:
        if "data-testid" in div.attrs and div["data-testid"] == "MediaStoryCard":
            links.append(f"https://reuters.com{div.find('a')['href']}")

    return links

def get_titles(html):
    title = html.find('h1').getText()
    return title

def get_dates(html):
    date_line = html.findAll(class_="date-line__date__23Ge-")
    date = date_line[1].getText() + " | " + date_line[2].getText()
    return date

def get_image_urls(html):
    try:
        image_url = html.find(class_=re.compile("image-container")).find('img')['src']
    except TypeError:
        image_url = "Null"
    return image_url

def get_bodies(html):
    body = ""
    paragraph_tags = html.find(class_=re.compile("article-body")).findAll('p')
    for tag in paragraph_tags:
        if re.compile("paragraph-\d*"):
            body += tag.getText() + "\n"
    return body


address = "https://www.reuters.com/world/us/"
Site(address, "us-news", "reuters", get_links, get_titles, get_dates, get_image_urls, get_bodies)
