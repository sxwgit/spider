import pymysql
from search import Search
import json
import time
from product import Product


def f(d):
    x = Product()
    x.url = d['url']
    x.name = d['name']
    x.price = d['price']
    x.comment = d['comment']
    x.shop = d['shop']
    return x


def find_key(key):
    conn = pymysql.connect(user='root', password='a765601220', database='paper', charset="utf8")
    curs = conn.cursor()
    nowtime = time.time()
    curs.execute('select keyword,time from paper_infor')
    values = curs.fetchall()
    dic = {}  # 用字典储存关键字和时间，便于下文检索
    for k, v in values:
        dic[k] = v
    if values == ():  # 数据库为空
        print(0)
        data, pic_url, price_picurl = Search(key)
        jd = json.dumps(data[0], ensure_ascii=False, default=lambda obj: obj.__dict__)
        tb = json.dumps(data[1], ensure_ascii=False, default=lambda obj: obj.__dict__)
        curs.execute(
            "insert into paper_infor (keyword,jd_items,tb_items,time,pic_url,price_picurl) values('%s','%s','%s','%s','%s','%s')" % (
                key, jd, tb, time.time(), pic_url, price_picurl))
        conn.commit()
        curs.close()
        conn.close()
        return data, pic_url, price_picurl
    else:
        if key in dic:  # 关键字在数据库中存在

            if nowtime - float(dic[key]) > 86400:  # 如果两次查询时间差大于一天，则重新写入
                print((1))
                data, pic_url, price_picurl = Search(key)
                jd = json.dumps(data[0], ensure_ascii=False, default=lambda obj: obj.__dict__)
                tb = json.dumps(data[1], ensure_ascii=False, default=lambda obj: obj.__dict__)
                curs.execute(
                    "update paper_infor set jd_items='%s',tb_items='%s',time='%s',pic_url='%s',price_picurl='%s' where keyword='%s'" % (
                        jd, tb, time.time(), pic_url, price_picurl, key))
                conn.commit()
                curs.close()
                conn.close()
                return data, pic_url, price_picurl

            else:
                print(2)
                curs.execute("select jd_items,tb_items,pic_url,price_picurl from paper_infor where keyword='%s'" % key)
                content = curs.fetchall()
                jd = json.loads(content[0][0])
                jd_items = list(map(f, jd))
                tb = json.loads(content[0][1])
                tb_items = list(map(f, tb))
                pic_url = content[0][2]
                price_picurl = content[0][3]
                data = [jd_items, tb_items]
                return data, pic_url, price_picurl

        else:  # 关键字在数据库中不存在
            print('3')
            data, pic_url, price_picurl = Search(key)
            jd = json.dumps(data[0], ensure_ascii=False, default=lambda obj: obj.__dict__)
            tb = json.dumps(data[1], ensure_ascii=False, default=lambda obj: obj.__dict__)
            curs.execute(
                "insert into paper_infor (keyword,jd_items,tb_items,time,pic_url,price_picurl) values('%s','%s','%s','%s','%s','%s')" % (
                    key, jd, tb, time.time(), pic_url, price_picurl))
            conn.commit()
            curs.close()
            conn.close()
            return data, pic_url, price_picurl
