import requests
from bs4 import BeautifulSoup
import datetime
import re
import time

#全域變數
y = datetime.datetime.now().strftime("%Y-%m-%d")    #今天日期
y2 = datetime.date.today() + datetime.timedelta(-1)  #昨天日期(避免漏偵測)
y2 = str(y2)
m1 = re.compile(r'[0-9-]{10}$') #正則表達式 10個字元、由數字0-9及dash組成(日期格式)
Date_error = {
    'message': 
    "\n"+
    '日期格式錯誤'
}
header = {
          "Origin":"https://codebeautify.org",
          "Referer":"https://codebeautify.org/"
}

#傳送更新通知
def line(data):
    url = 'https://notify-api.line.me/api/notify'
    token = 'OU2zb6Js8uMFlBleG8MXvQEnph55MvZegpUPbCDri0V'
    headers = {
        'Authorization': 'Bearer ' + token    # 設定權杖
    }
    requests.post(url, headers=headers, data=data)

#執行錯誤時傳送錯誤通知
def line_error(name,e):
    url = 'https://notify-api.line.me/api/notify'
    token = 'OU2zb6Js8uMFlBleG8MXvQEnph55MvZegpUPbCDri0V'
    headers = {
        'Authorization': 'Bearer ' + token   
    }
    Excute_error = {
        'message': 
        "\n"+
        "<MangaAndNovel>運行出錯"+
        "\n"+
        f"{name}錯誤:{e}"
    }
    requests.post(url, headers=headers, data=Excute_error)

#以下函式都是爬蟲
def mange(*args):
    for arg in args :
        url = f"https://www.manhuagui.com/comic/{arg}/"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text,"html.parser")
        title = soup.select("div.book-title > h1")[0].text
        update_time = soup.select("span > span:nth-child(3)")[0].text #更新時間
        x = soup.select("li.status > span > a")[0].text  #最新話數
        if re.match(m1,update_time):
            if update_time == y or update_time == y2:
                data = {
                    'message': 
                    "\n"+
                    f"看漫畫:《{title}》已更新至{x}"
                }
                line(data)
            time.sleep(1)
        else :
            line(Date_error)
def novel(*args):
    for arg in args : 
        orurl = "https://www.codebeautify.com/URLService"
        url = f"https://tw.linovelib.com/novel/{arg}.html"
        payload = {
             "path": url
        }
        
        resp = requests.post(orurl, headers=header, data=payload)               
        soup = BeautifulSoup(resp.text,"html.parser")
        title = soup.find("meta", property="og:novel:book_name")['content']
        update_date = soup.find("meta", property="og:novel:update_time")["content"][:10]
        chapter_name = soup.find("meta", property="og:novel:latest_chapter_name")["content"]
        if re.match(m1,update_date):
            if update_date == y or update_date == y2:
                data = {
                    'message': 
                    "\n"+
                    f"小說:《{title}》已更新"+
                    "\n"+
                    f"{chapter_name}"
                   }
                line(data)
            time.sleep(1)
        else:
            line(Date_error)    

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
        time.sleep(1)
        
try:
    mangaren("47686","jiabailideduola","wozenmekenengchengweinidelianren-buxingbuxing-bushibukeneng")
    mangaren("yiquanchaoren","54233","wailengneiredeqingmeiduiwodeanlianbaoluwuyi","48094","45283","59383")       #漫畫人
except Exception as e:
    line_error("漫畫人",e)
    
try:
    mange(34439,7580,6414,5173,36152,1676,28356,17473,42459,42508,31239,31589,36998,32503,30609,35634)        #看漫畫
except Exception as e:
    line_error("看漫畫",e)
    
try:
    novel(1861,2059,2139,6,3181,9,2727,3286,8,2513,3161,3095,2356) #逼哩輕小說 
except Exception as e:    
    line_error("逼哩輕小說",e)
