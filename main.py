from json import dumps
from src.reuters_us import reuters_us
from src.ap_us import ap_us

def main():
    articles = dict()

    article_list = reuters_us()
    article_list = ap_us()
    for i, article in zip(range(0, len(article_list)+1), article_list):
        articles[f"reuters-{i}"] = article.to_dict()

    # Write articles dictionary to file
    with open("data/articles.json", "w") as file:
        file.write(dumps(articles, indent=4))

if __name__ == '__main__':
    main()
