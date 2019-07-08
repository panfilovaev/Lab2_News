# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 18:14:13 2019

@author: DNS
"""

import requests 
import re
from bs4 import BeautifulSoup
import time
import csv

def get_article_keywords(link):
    article_page = requests.get(link)
    article_soup = BeautifulSoup(article_page.content, 'html.parser')
    if len(article_soup.head('meta', attrs={'name': 'keywords'})) != 0:
        return article_soup.head('meta', attrs={'name': 'keywords'})[0]['content']
    else:
        print(link)
        return None

def get_articles(init = False):
    news = []
    articles = source_soup.find_all('article')
    for article in articles:
        ref = article('a', attrs={'href': re.compile('https://www.cbsnews.com/news/')})
        #print('1:', article)
        if len(ref) != 0:
            link = ref[0]['href']
            if init:
                initialization_refs.add(link)
            elif not link in initialization_refs:
                attributes_news = {}
                attributes_news['url'] = link
                attributes_news['header'] = article(class_ = 'item__hed')[0].text.strip()
                attributes_news['description'] = article(class_ = 'item__dek')[0].text.strip()
                attributes_news['keywords'] = get_article_keywords(link)
                news.append(attributes_news)
                initialization_refs.add(link)
    return news 

def writer_file_news(FILENAME = 'news', news_list = [], init = False):
    with open(FILENAME, "a", newline="", encoding='utf-8') as file:
        columns = ["url", "header", "description", "keywords"]
        writer = csv.DictWriter(file, fieldnames=columns)
        if init: writer.writeheader()
        writer.writerows(news_list)

print('время запуска: ', time.asctime())
init_time = time.clock()
running_time = time.clock() - init_time

source_url = 'https://www.cbsnews.com/politics/'
source_page = requests.get(source_url)
source_soup = BeautifulSoup(source_page.content, 'html.parser')

#заполяем множество новостей, которые были опубликованы до начала программы, их анализировать не будем
initialization_refs = set() 
get_articles(True)

writer_file_news('GOP_news.csv', [], True)
writer_file_news('Democrat_news.csv',[], True)
writer_file_news('Another_news.csv', [], True)
      
while running_time < 86400: #меньше суток
    
    source_page = requests.get(source_url)
    source_soup = BeautifulSoup(source_page.content, 'html.parser')
    news = get_articles()
    
    #расскладывакм новости по спискам. Одна новость может попасть и в список демократов и в список GOP, 
    #если содержит и те и другие ключевые cлова
    GOP_news =[]
    Democrat_news = []
    Another_news = []
    
    for n in news:
        if 'republican party' in n['keywords'] or 'GOP' in n['keywords'] or 'republicans' in n['keywords']:
            GOP_news.append(n)
        if 'democratic party' in n['keywords'] or 'democrats' in n['keywords']:
            Democrat_news.append(n)
        if not 'republican party' in n['keywords'] and not 'GOP' in n['keywords'] and not 'democratic party' in n['keywords'] and not 'democrats' in n['keywords'] and not 'republicans' in n['keywords']:
            Another_news.append(n)
        
    writer_file_news('GOP_news.csv', GOP_news )
    writer_file_news('Democrat_news.csv',Democrat_news)
    writer_file_news('Another_news.csv', Another_news)
    
    print('итеррация завершена')
    #прерываемся на 30 минут
    time.sleep(3600) #засыпаем на один час
    
    running_time = time.clock() - init_time
    print('время работы оработки: ', int(running_time/60), 'минут')
    
    
print('Ороботка завершена в ', time.asctime())

