from json import dumps
from src.reuters_us import reuters

def main():
    articles = dict()

    article_list = reuters()
    for i, article in zip(range(0, len(article_list)+1), article_list):
        articles[f"reuters-{i}"] = article.to_dict()

    # Write articles dictionary to file
    with open("data/articles.json", "w") as file:
        file.write(dumps(articles, indent=4))

if __name__ == '__main__':
    main()
