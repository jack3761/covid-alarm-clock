import json
import requests


with open('config.json', 'r') as f:
    x = json.load(f)["news"]
    api_key = x["news_key"]
    base_url = x["news_URL"]
    key_words = x['news_key_words']
country = "gb"
complete_url = base_url + "country=" + country + "&apiKey=" + api_key
# print response object
response = requests.get(complete_url)

def get_news():
    news_dict = response.json()
    articles = news_dict["articles"]
    filtered_articles = []
    if key_words != []:
        for article in articles:
            for word in key_words:
                if article["source"]["name"] and article['content'] and article['title']:
                    if word in article['title'].lower() or word in article['content'].lower():
                        filtered_articles.append(article['title'])
    else:
        for article in articles:
            filtered_articles.append(article['title'])
    return filtered_articles

