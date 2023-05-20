from src.article import Article
import requests
from bs4 import BeautifulSoup
import re

def reuters():

    # get website html
    address = "https://www.reuters.com/world/us/"
    response = requests.get(address)
    soup = BeautifulSoup(response.text, 'html.parser')

    # create return array
    articles = []

    # get links to all sub-articles
    links = []
    divs = soup.findAll('div')
    for div in divs:
        if "data-testid" in div.attrs and div["data-testid"] == "MediaStoryCard":
            links.append(f"https://reuters.com{div.find('a')['href']}")

    # get data from all sub-article links
    for i, link in zip(range(0, len(links)+1), links):
        html = BeautifulSoup(requests.get(link).text, "html.parser")
        category = "us-news"
        title = html.find('h1').getText()

        date = ""
        date_line = html.findAll(class_="date-line__date__23Ge-")
        for j in range(2, 3):
            date += date_line[j].getText()

        try:
            image_url = html.find(class_=re.compile("image-container")).find('img')['src']
            image = requests.get(image_url).content
        except TypeError:
            image_name = "Null"
        else:
            with open(f"data/reuters-{i}.png", 'wb') as file:
                file.write(image)
            image_name = f"reuters-{i}.png"

        body = ""
        paragraph_tags = html.find(class_=re.compile("article-body")).findAll('p')
        for tag in paragraph_tags:
            if re.compile("paragraph-\d*"):
                body += tag.getText() + "\n"

        articles.append(Article(category, title, date, image_name, body))

    return articles

if __name__ == "__main__":
    reuters()
