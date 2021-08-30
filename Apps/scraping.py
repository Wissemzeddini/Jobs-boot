import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Jobs"
)
def splitAndSave(ch):
    list=[]
    for i in ch:
        i = re.sub(r'(\s+|\n)', ' ', i)
        if(len(i)>3):
            list.append(i.strip())
    return list[2]

def saveJob(logo,titre,link,date,local):
    try:
        mycursor = mydb.cursor()
        now = datetime.now()
        sql = "INSERT INTO keejob (logo, titre, link, date, local, date_scraping) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (logo, titre, link, date, local, now)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Job successfully saved")
    except:
        print("Job failed to save")

def searchByKeyword(keyword):
    url='https://www.keejob.com/offres-emploi/?keywords=data+science'
    url = url.replace('data+science', keyword)
    print(keyword,"...")
    web = requests.get(url).content
    parse = BeautifulSoup(web, 'html.parser')
    head= parse.find_all('div', class_='block_white_a')
    for h in head:
        try:
            logo ="https://www.keejob.com"+h.a.figure.img['src']
            titre = h.find('div', class_="span8").text.strip()
            link = h.find('div', class_="span8").h6.a['href']
            link = "https://www.keejob.com"+link
            date = h.find('div', class_="meta_a").text.strip()
            info = h.find('div', class_="span12 no-margin-left").text
            info = re.split(r'(\n)', info)
            local = splitAndSave(info)
            saveJob(logo,titre,link,date,local)
        except:
            pass
        
def scraping_core():
	keyword=['data+science', 'python', 'informatique', 'big+data', 'data+analysist', 'BI', 'AI', 'machine+learning']
	for key in keyword:
		searchByKeyword(key)