#!/usr/bin/env python
# coding: utf-8

# In[43]:


import requests
from bs4 import BeautifulSoup
import datetime

y = datetime.datetime.now().strftime("%Y-%m-%d")
y2 = datetime.date.today() + datetime.timedelta(-1)
y2 = str(y2)

def line(data):
    url = 'https://notify-api.line.me/api/notify'
    token = 'OU2zb6Js8uMFlBleG8MXvQEnph55MvZegpUPbCDri0V'
    headers = {
        'Authorization': 'Bearer ' + token    # 設定權杖
    }
    requests.post(url, headers=headers, data=data)
    
def mange(*args):
    for arg in args :
        url = f"https://www.manhuagui.com/comic/{arg}/"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text,"html.parser")
        title = soup.select("div.book-title > h1")[0].text
        time = soup.select("span > span:nth-child(3)")[0].text #更新時間
        x = soup.select("li.status > span > a")[0].text  #最新話數
        if time == y or time == y2:
            data = {
                'message': 
                "\n"+
                f"看漫畫:《{title}》已更新至{x}"
            }
            line(data)
            
def novel(*args):
    for arg in args : 
        orurl = "https://www.view-page-source.com/"
        url = f"https://tw.linovelib.com/novel/{arg}.html"
        payload = {
             "reference_id": "1",
             "vps_token": "sEJy.bli+ripRaCL0QIB0",
             "uri": f"{url}"
        }
        resp = requests.post(orurl, data=payload)       
        soup = BeautifulSoup(resp.text,"html.parser")
        try:
            x = soup.select("p.gray")[0].text
            title = soup.select("h2.book-title")[0].text
            a = x[:10]
            b = x[11:]
        
        except:
            token = soup.select("#vps_token")[0]["value"]
            payload = {
             "reference_id": "1",
             "vps_token": token,
             "uri": f"{url}"
            }
            resp = requests.post(orurl, data=payload)
            soup = BeautifulSoup(resp.text,"html.parser")
            title = soup.select("h2.book-title")[0].text
            x = soup.select("p.gray")[0].text
            a = x[:10]
            b = x[11:]
        if a == y or a == y2:
            data = {
                'message': 
                "\n"+
                f"小說:《{title}》已更新"+
                "\n"+
                f"{b}"
               }
            line(data)
         

def mangaren(*args):
    for arg in args:
        if arg.isdigit():
            url = f"https://www.manhuaren.com/chapterlist{arg}/"
        else:
            url = f"https://www.manhuaren.com/manhua-{arg}"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text,"html.parser")
        title = soup.select(".normal-top-title")[0].text.strip()
        new = soup.select(".detail-list-title-2")[0].text.strip()
        date = soup.select(".detail-list-title-3")[0].text.strip()
        if date[:2] == "今天" or date[:2] == "昨天":
            data = {
                'message': 
                "\n"+
                f"漫畫人:《{title}》已更新至{new}"
            }
            line(data)
try:
    mangaren("47686","jiabailideduola","wozenmekenengchengweinidelianren-buxingbuxing-bushibukeneng")
    mangaren("yiquanchaoren","54233")                         #漫畫人
    mange(34439,7580,6414,5173,36152,1676,28356,17473,42459)        #看漫畫
    novel(1861,2356,2059,2139,6,3181,9,2727,3286,8,2513,3161,3095) #逼哩輕小說 
except:
    data = {
                'message': 
                "\n"+
                "<MangaAndNovel>運行出錯"
            }
    line(data)
    quit()
