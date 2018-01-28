import requests
import re
from product import Product
from urllib.request import quote
import json
from threading import Lock
import time


def get_tbcomment(id):
    x = {}
    url = 'https://rate.taobao.com/detailCommon.htm?auctionNumId=%d' % id
    html = requests.get(url).text
    t = html[3:-1]
    content = json.loads(t)
    real_content = content['data']['impress']
    for i in real_content:
        x[i['title']] = i['count']
    return x


lock = Lock()


def run_thread(nid_list):
    x = []
    for i in range(len(nid_list)):
        # 先要获取锁:
        lock.acquire()
        try:
            x.append(get_tbcomment(nid_list[i]))
        finally:
            # 改完了一定要释放锁:
            lock.release()
    return x


def sovl_dict(contents, key):
    list = []
    nid_list = []
    for content in contents[0:15]:
        nid_list.append(int(content['nid']))
        x = Product()
        x.name = key
        if 'nick' in content:
            x.shop = content['nick']
        else:
            x.shop = u" "
        if 'salePrice' in content:
            x.price = float(content['salePrice'])
        elif 'view_price' in content:
            x.price = float(content['view_price'])
        else:
            x.price = u" "
        x.url = 'https://item.taobao.com/item.htm?id=%d' % int(content['nid'])
        list.append(x)
    comment_list = run_thread(nid_list)
    for i in range(len(list)):
        list[i].comment = comment_list[i]
    return list


def search_tb(key):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0',
        'Host': 's.taobao.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.taobao.com/',
        'Connection': 'keep-alive',
    }
    key_word = quote(key)
    url = 'https://s.taobao.com/search?q={}'.format(key_word)
    html = requests.get(url, headers=headers)

    regex = r'g_page_config = (.+)'
    items = re.findall(regex, html.content.decode('utf-8'))
    items = items.pop().strip()
    items = items[0:-1]
    items = json.loads(items)
    items = items['mods']['itemlist']['data']['auctions']
    return sovl_dict(items, key)
