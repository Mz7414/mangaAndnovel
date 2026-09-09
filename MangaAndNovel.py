import requests
from bs4 import BeautifulSoup
import datetime
import re
import time
import os

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

#全域變數
Token = os.environ.get("TOKEN")
User_id = os.environ.get("USER_ID")
user = {
    "Token" : Token,
    "User_id" : User_id,
    "Prefix" : '【作品更新通知】\n'
}
y = datetime.datetime.now().strftime("%Y-%m-%d")    #今天日期
y2 = datetime.date.today() + datetime.timedelta(-1)  #昨天日期(避免漏偵測)
y2 = str(y2)
m1 = re.compile(r'[0-9-]{10}$') #正則表達式 10個字元、由數字0-9及dash組成(日期格式)

header = {
    "Origin":"https://codebeautify.org",
    "Referer":"https://codebeautify.org/"
}

def discord(e) :
    Discord_Webhook_URL = os.environ.get("DISCORD_WEBHOOK_URL")
    data = {
        "content": e
    }
    response = requests.post(Discord_Webhook_URL, json=data)
    
try :
    from linebot.v3.messaging import MessagingApi, ApiClient, Configuration
    from linebot.v3.messaging.models import TextMessage, PushMessageRequest
except ImportError as e :
    discord(str(e))
    raise

def line(msg) :
    config = Configuration(access_token=user['Token'])
    user_id = user['User_id']      
    msg = user['Prefix'] + msg    
    with ApiClient(configuration=config) as api_client :
        messaging_api = MessagingApi(api_client)    
        try :
            message = TextMessage(text=msg)
            push_request = PushMessageRequest(
                to=user_id,
                messages=[message]
            )    
            messaging_api.push_message(push_message_request=push_request)           
        except Exception as e :
            discord(str(e), msg)
            return
            
#執行錯誤時傳送錯誤通知
def line_error(name,e):
    line("<MangaAndNovel>運行出錯\n"+f"{name}錯誤:{e}")

#------------------------------------------------------

#以下函式都是爬蟲
def manga(*args):
    for arg in args :
        url = f"https://www.manhuagui.com/comic/{arg}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        resp = requests.get(url,headers=headers)
        soup = BeautifulSoup(resp.text,"html.parser")
        title = soup.select("div.book-title > h1")[0].text
        update_time = soup.select("span > span:nth-child(3)")[0].text #更新時間
        x = soup.select("li.status > span > a")[0].text  #最新話數
        if re.match(m1,update_time):
            if update_time == y or update_time == y2:
                line(f"看漫畫:《{title}》已更新至{x}")
            time.sleep(3)
        else :
            line(f"{title} 日期格式錯誤")
            
def novel(*args):
    for arg in args : 
        try:
            orurl = "https://www.codebeautify.com/URLService"
            url = f"https://tw.linovelib.com/novel/{arg}.html"
            payload = {
                 "path": url
            }
            
            resp = requests.post(orurl, headers=header, data=payload, timeout=15) 
    
            soup = BeautifulSoup(resp.text,"html.parser")
            title = soup.find("meta", property="og:novel:book_name")['content']
            update_date = soup.find("meta", property="og:novel:update_time")["content"][:10]
            chapter_name = soup.find("meta", property="og:novel:latest_chapter_name")["content"]
            if re.match(m1,update_date):
                if update_date == y or update_date == y2:
                    line(f"小說:《{title}》已更新"+"\n"+f"{chapter_name}")
            else:
                line(f"{title} 日期格式錯誤") 
        except Exception as e:
            line_error(f"小說代碼 {arg}", e)
            continue
        time.sleep(10)
        

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
            line(f"漫畫人:《{title}》已更新至{new}")
        time.sleep(1)
        
try:
    mangaren("47686","jiabailideduola","wozenmekenengchengweinidelianren-buxingbuxing-bushibukeneng")
    mangaren("yiquanchaoren","54233","wailengneiredeqingmeiduiwodeanlianbaoluwuyi","48094","45283","59383")       #漫畫人
    mangaren("wodantuidenvhai")
except Exception as e:
    line_error("漫畫人",e)
    
try:
    manga(34439,7580,6414,5173,36152,1676,28356,17473,42459,42508,31239,31589,36998,32503,30609,35634,32156,39903,43847)        #看漫畫
except Exception as e:
    line_error("看漫畫",e)
    
#novel(1861,2778,2139,6,3181,9,2727,3286,8,3095,2356,3768,2979,4774) #逼哩輕小說 
