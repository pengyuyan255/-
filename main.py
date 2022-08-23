from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import http
import json
import urllib

today = datetime.now()
# start_date = os.environ['START_DATE']
# city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']
#
# app_id = os.environ["APP_ID"]
# app_secret = os.environ["APP_SECRET"]
#
# user_ids = os.environ["USER_ID"].split("\n")
# template_id = os.environ["TEMPLATE_ID"]

start_date = "2019-12-08"
city = "武汉"
birthday = "12-08"

app_id = "wx7be3bcab0e38bcf7"
app_secret = "b3fbb0b7af42b1aaa84498cbdb446ef0"

user_ids = ["o0big6oIc60RVddWiYuKEeI5uBPE"]
template_id = "Sii28sRYm1JAsWWp9YSzFXxH6qrW6Kjv3PJ47l2m274"

def get_date():
  day = date.today()
  week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
  week = week_list[datetime.today().weekday()]
  return str(day) + ' ' + week

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_caihongpi():
    conn = http.client.HTTPSConnection('api.tianapi.com')  # 接口域名
    params = urllib.parse.urlencode({'key': '69b5f3f9a6567bbe35da7b53e1f0b79e'})
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn.request('POST', '/caihongpi/index', params, headers)
    res = conn.getresponse()
    json1 = json.loads(res.read().decode('utf-8'))
    # print(type(json1))
    # print(json1['newslist'][0]['content'])
    return json1['newslist'][0]['content']
  
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, highest, lowest = get_weather()
data = {"date": {"value": get_date(), "color": get_random_color()},
        "weather": {"value": wea, "color": get_random_color()},
        "temperature": {"value": temperature, "color": get_random_color()},
        "love_days": {"value": get_count(), "color": get_random_color()},
        "birthday_left": {"value": get_birthday(), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()},
        "highest": {"value": highest, "color": get_random_color()},
        "lowest": {"value": lowest, "color": get_random_color()},
        "caihongpi":{"value":get_caihongpi(), "color": get_random_color()}}
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("发送了" + str(count) + "条消息")
