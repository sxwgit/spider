import re
from product import Product
import requests
from bs4 import BeautifulSoup as bs
import json
from urllib.request import quote
from threading import Lock

def shop_name(shopid_list):
    url = 'https://search.jd.com/shop_new.php?ids='
    for i in range(len(shopid_list)):
        url = url + '{%d}' % i + '%2C'
    url = url.format(*shopid_list)
    headers = {'Connection': 'keep-alive',
               'Referer': 'https://search.jd.com/Search?keyword=iphone6s&enc=utf-8&wq=iphone6s&pvid=70d50704c83d469fbc616e449f09fea4',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest'}
    html = requests.get(url=url, headers=headers)
    shopid_json = json.loads(html.text)
    json_list = []
    for i in shopid_json:
        json_list.append(i['shop_name'])
    return json_list