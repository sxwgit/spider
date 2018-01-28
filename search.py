# endocing:utf-8
from jd_items import search_jd
from tb_items import search_tb
from picture import draw_picture
from multiprocessing import Pool
from sort import Sort


def Search(key):
    p = Pool(2)
    results = []
    for i in [search_jd, search_tb]:
        result = p.apply_async(i, args=(key,))
        results.append(result)
    p.close()
    p.join()
    jd_list, pic_url = results[0].get()
    tb_list = results[1].get()
    '''
    jd_list,pic_url=search_jd(key)
    tt_list=search_tt(key)
    '''
    data = [Sort(jd_list), Sort(tb_list)]
    price_picurl = draw_picture(jd_list, tb_list, key)
    return data, pic_url, price_picurl
Search('iphone6s')