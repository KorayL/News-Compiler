from src.article import Article
import requests
from bs4 import BeautifulSoup
import re

def reuters_us():

    # get website html
    address = "https://www.reuters.com/world/us/"
    soup = BeautifulSoup(requests.get(address).text, 'html.parser')

    # create return array
    articles = []

    # get links to all sub-articles
    links = []
    divs = soup.findAll('div')
    for div in divs:
        if "data-testid" in div.attrs and div["data-testid"] == "MediaStoryCard":
            links.append(f"https://reuters.com{div.find('a')['href']}")

    # get data from all sub-article links
    for num, link in zip(range(0, len(links) + 1), links):
        html = BeautifulSoup(requests.get(link).text, "html.parser")
        category = "us-news"
        title = html.find('h1').getText()

        date_line = html.findAll(class_="date-line__date__23Ge-")
        date = date_line[1].getText() + " | " + date_line[2].getText()

        try:
            image_url = html.find(class_=re.compile("image-container")).find('img')['src']
            image = requests.get(image_url).content
        except TypeError:
            image_name = "Null"
        else:
            image_name = f"reuters-us-{num}.jpg"
            with open(f"data/{image_name}", 'wb') as file:
                file.write(image)

        body = ""
        paragraph_tags = html.find(class_=re.compile("article-body")).findAll('p')
        for tag in paragraph_tags:
            if re.compile("paragraph-\d*"):
                body += tag.getText() + "\n"

        articles.append(Article(category, title, date, image_name, body))

    return articles
