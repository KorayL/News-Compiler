from src.article import Article
import requests
from bs4 import BeautifulSoup
import re

def ap_us():
    # get website html
    address = "https://apnews.com/hub/us-news"
    soup = BeautifulSoup(requests.get(address).text, 'html.parser')

    # create return array
    articles = []

    # get links to all sub-articles
    links = []
    stories = soup.findAll('div', class_=re.compile("FeedCard"))
    for story in stories:
        links.append(f"https://apnews.com{story.find('a')['href']}")

    for num, link in zip(range(0, len(links) + 1), links):
        html = BeautifulSoup(requests.get(link).text, "html.parser")
        category = "us-news"
        title = html.find('h1').getText()

        date = html.find(class_=re.compile("Timestamp Component")).getText()

        try:
            image_url = html.find(class_=re.compile("LeadFeature")).find('img')['src']
            image = requests.get(image_url).content
        except TypeError:
            image_name = "Null"
        except AttributeError:
            image_name = "Null"
        else:
            image_name = f"ap-us-news-{num}.jpg"
            with open(f"data/image_name", 'wb') as file:
                file.write(image)

        body = ""
        print(link)
        paragraph_tags = html.findAll('p', class_=re.compile("Component-root"))
        for tag in paragraph_tags:
            body += tag.getText() + "\n"

        articles.append(Article(category, title, date, image_name, body))

    return articles
