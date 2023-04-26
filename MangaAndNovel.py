#!/usr/bin/env python
# coding: utf-8

# In[43]:


import requests
from bs4 import BeautifulSoup
import datetime

y = datetime.datetime.now().strftime("%Y-%m-%d")

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
        if time == y :
            data = {
                'message': 
                "\n"+
                f"漫畫:《{title}》已更新至{x}"
            }
            line(data)
            
def novel(*args):
    for arg in args : 
        url = f"https://tw.linovelib.com/novel/{arg}.html"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text,"html.parser")
        x = soup.select("p.gray")[0].text
        title = soup.select("h2.book-title")[0].text
        a = x[:10]
        b = x[11:]
        if a == y :
            data = {
                'message': 
                "\n"+
                f"小說:《{title}》已更新"
            }
            line(data)
         
novel(2356,2059,2139,6,3181,9,2727,3286,8,2513,3161,3095) #逼哩輕小說 
mange(34439,7580,6414,5173,36152,1676,28356,17473)        #看漫畫

