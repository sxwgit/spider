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


def get_comment(id_url):
    x = {}
    try:
        id = ''.join(re.findall(r'\d+', id_url))
        url = 'https://club.jd.com/comment/productPageComments.action?' \
              'productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(id)
        html = requests.get(url=url)
        setting = json.loads(html.text)
        hotCommentTagStatistics = setting['hotCommentTagStatistics']
        for item in hotCommentTagStatistics:
            x[item['name']] = item['count']
    except:
        x = {}
    return x


lock = Lock()


def run_thread(nid_list):
    x = []
    for i in range(len(nid_list)):
        # 先要获取锁:
        lock.acquire()
        try:
            x.append(get_comment(nid_list[i]))
        finally:
            # 改完了一定要释放锁:
            lock.release()
    return x


def url(url):
    url = str(url)
    true_url = re.findall(r'//img.+.jpg', url)
    return ''.join(list(true_url))


def search_jd(key):
    key_code = quote(key)
    html = requests.get('https://search.jd.com/Search?keyword={}'
                        '&enc=utf-8&wq={}'.format(key_code, key_code))
    bsobj = bs(html.content, 'lxml')
    pic_list = bsobj.findAll('div', {'class': 'p-img'})
    price_list = bsobj.findAll('div', {'class': 'p-price'})
    name_list = bsobj.findAll('div', {'class': 'p-name p-name-type-2'})
    shop_list = bsobj.findAll('div', {'class': 'p-shop'})
    t1 = pic_list[0].find('img').get('src')
    t2 = pic_list[0].find('img').get('data-lazy-img')
    if t1:
        pic_url = 'http:' + t1
    else:
        pic_url = 'http:' + t2
    shopid_list = []
    item_list = []
    idurl_list = []
    for i in range(15):
        x = Product()
        x.name = key
        x.price = float(price_list[i].find('strong').get_text()[1:])
        if x.price == None:
            pass
        else:
            #shopid_list.append(shop_list[i].get('data-shopid'))
            x.shop=shop_list[i].get_text()
            x.url = 'https:' + name_list[i].find('a')['href']  # 这里得到的是商品id
            idurl_list.append(name_list[i].find('a')['href'])
            item_list.append(x)
    comment_list = run_thread(idurl_list)
    for i in range(len(comment_list)):
        item_list[i].comment = comment_list[i]
    '''
        通过shopid所构建的链接得到店铺名，如果shopid为空，则删除对应的item，证明该店铺不存在或者为广告等
    
    shopname = shop_name(shopid_list)
    for i in range(len(shopid_list) - 1, -1, -1):
        if shopid_list[i] == None:
            del item_list[i]
    for i in range(len(shopname)):
        item_list[i].shop = shopname[i]
    '''
    return item_list, pic_url

