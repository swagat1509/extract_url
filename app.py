import uvicorn
from newsapi import NewsApiClient
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from pygooglenews import GoogleNews



app = FastAPI()

class NewsArticle(BaseModel):
    
    keywords: str
    sources: str
    


class TextExtraction:
    """
    Class to extract the news articles text from the body of the news article.

    """
    def __init__(self, url):
        self.url = url

    def getdata(self,url):
        r = requests.get(url)
        return r.text

    def extract_news(self):
        htmldata = self.getdata(self.url)
        soup = BeautifulSoup(htmldata, 'html.parser')
        body_list = []
        for data in soup.find_all("p"):
            body_list.append(data.get_text())
        body = ".".join(body_list)
        body=body.replace("\n","")

        return body


"""
The following route will extract the urls from the google news page, after we provide the search kaeywords.
"""
@app.post('/get_news_urls_from_keywords_googlenewspage')
def get_news_urls(getarticles: NewsArticle):
    query1 = getarticles.keywords.replace(","," AND ")
    urls = []
    gn = GoogleNews(lang = 'en', country = 'IN')
    results = gn.search(query1)
    newsitems = results['entries']
    for item in newsitems[0:5]:
        urls.append(item.link)

    return {'urls':urls}




        






# api to extract the title, descritpion and the body of the news: 
@app.post('/get_news_url_from_keywords')
def news_articles(getarticles: NewsArticle):
    query1 = getarticles.keywords.replace(","," AND ")
    if getarticles.sources=="string":
        q2=""
    else:
        #q2 = getarticles.sources.replace(","," AND ")
        l = getarticles.sources.split(",")
        if len(l)==1:
            q2 = getarticles.sources
        else:
            q2 = getarticles.sources.replace(","," AND ")  
    
    print(q2)
    current_date = date.today().isoformat()   
    days_before = (date.today()-timedelta(days=30)).isoformat()
    # News api key
    newsapi = NewsApiClient(api_key='13aba4906bbc4731839a873a2ac8b356')
    all_articles = newsapi.get_everything(q=query1,sources=q2, from_param=days_before,to=current_date,language='en', sort_by='relevancy')
    
    urls = []
    total_urls = len(all_articles['articles'])
    for i in range(total_urls):
        urls.append(all_articles['articles'][i]['url'])
    urls = urls[0:5]

    # returns the title, descritpion and the body of the news
    if len(urls) > 0:
        return {'urls':urls}
    else:
        return ("No news found related to the keywords")
           



"""
Description of the below post method:
After the docker image is created from this the below post method "/keyword_sentiment_post_text" 
calls the "/getsentiment" post method from the other docker image and then takes the result from there
and displayes as the output of the below method. 

class Sentiment(BaseModel):
    
    
    sentimenttext : str


@app.post('/keyword_sentiment_post_text')
def get_keyword_sentiment(keyword_sentiment_post:Sentiment):
    t = {"text":keyword_sentiment_post.sentimenttext}
    response = requests.post('http://second:8080/getsentiment', data = json.dumps(t))
    response = response.text
    return (json.loads(response))


"""



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)

