from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
# 在一起时间
start_date = os.environ['START_DATE']
# 地区
city = os.environ['CITY']
# 生日
birthday = os.environ['BIRTHDAY']
# app_id
app_id = os.environ["APP_ID"]
# app_secret
app_secret = os.environ["APP_SECRET"]
# 用户id
user_id = os.environ["USER_ID"]
# 模板id
template_id = os.environ["TEMPLATE_ID"]
# 和风天气key
weather_key = os.environ["WEATHER_KEY"]

def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)

# 天气
def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

# 在一起时间
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

# 距离生日
def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# 文案
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

# 获取当日日期
def get_date():
  week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
  year = localtime().tm_year
  month = localtime().tm_mon
  day = localtime().tm_mday
  today = datetime.date(datetime(year=year, month=month, day=day))
  week = week_list[today.isoweekday() % 7]
  return "{} {}".format(today, week)
  
# 颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
# 传入地区获取天气信息
weather, temp, wind_dir = get_weather(city)
data = {"date": {"value":get_date(),"color":get_random_color()},"city":{"value":city,"color":get_random_color()},"weather":{"value":weather,"color":get_random_color()},"temp":{"value":temp,"color":get_random_color()},"wind_dir":{"value":wind_dir,"color":get_random_color()},"love_days":{"value":get_count(),"color": get_random_color()},"birthday":{"value":get_birthday(),"color":get_random_color()},"words":{"value":get_words(),"color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
