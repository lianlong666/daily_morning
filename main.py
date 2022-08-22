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
# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][0]
#   return weather['weather'], math.floor(weather['temp'])

def get_weather(city):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    region_url = "https://geoapi.qweather.com/v2/city/lookup?location={}&key={}".format(city, weather_key)
    city_data = get(region_url, headers=headers).json()
    if city_data.code == "404":
        print("推送消息失败，请检查地区名是否有误！")
        os.system("pause")
        sys.exit(1)
    elif city_data.code == "401":
        print("推送消息失败，请检查和风天气key是否正确！")
        os.system("pause")
        sys.exit(1)
    else:
        # 获取地区的location--id
        location_id = city_data.location[0].id
    weather_url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}".format(location_id, weather_key)
    weather_data = get(weather_url, headers=headers).json()
    # 天气
    weather = weather_data.now.text
    # 当前温度
    temp = weather_data.now.temp + u"\N{DEGREE SIGN}" + "C"
    # 风向
    wind_dir = weather_data.now.windDir
    return weather, temp, wind_dir

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
  
# 颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
# 传入地区获取天气信息
weather, temp, wind_dir = get_weather(city)
data = {"city":{"value":city,"color": get_random_color()},"weather":{"value":weather,"color": get_random_color()},"temp":{"value":temp,"color": get_random_color()},"wind_dir":{"value":wind_dir,"color": get_random_color()},"love_days":{"value":get_count(),"color": get_random_color()},"birthday":{"value":get_birthday(),"color": get_random_color()},"words":{"value":get_words(), ,"color": get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)