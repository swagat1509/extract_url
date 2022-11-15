import uvicorn
from newsapi import NewsApiClient
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, timedelta
import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

app = FastAPI()

class NewsArticle(BaseModel):
    
    keywords: str
    sources: str
    sentimenttext : str


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




        
        


# News api key
newsapi = NewsApiClient(api_key='13aba4906bbc4731839a873a2ac8b356')


# api to extract the title, descritpion and the body of the news: 
@app.post('/getarticles')
def news_articles(getarticles: NewsArticle):
    query1 = getarticles.keywords.replace(","," AND ")
    if getarticles.sources=="string":
        q2=""
    else:
        q2 = getarticles.sources.replace(","," AND ") 
    
    print(q2)
    current_date = date.today().isoformat()   
    days_before = (date.today()-timedelta(days=30)).isoformat()
    all_articles = newsapi.get_everything(q=query1,sources=q2, from_param=days_before,to=current_date,language='en', sort_by='relevancy')
    
    url = all_articles['articles'][0]['url']
    te = TextExtraction(url)
    news_body = te.extract_news()


    # returns the title, descritpion and the body of the news
    return({'title':all_articles['articles'][0]['title']},
           {'description':all_articles['articles'][0]['description']},
           {'body':news_body})



"""
Description of the below post method:
After the docker image is created from this the below post method "/keyword_sentiment_post_text" 
calls the "/getsentiment" post method from the other docker image and then takes the result from there
and displayes as the output of the below method. 
"""

@app.post('/keyword_sentiment_post_text')
def get_keyword_sentiment(keyword_sentiment_post:NewsArticle):
    t = {"text":keyword_sentiment_post.sentimenttext}
    response = requests.post('http://second:8080/getsentiment', data = json.dumps(t))
    return (response.text)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)

