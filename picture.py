import numpy as np
import matplotlib.pyplot as plt
def draw_picture(jd,tb,key):
    tb_lists=[];jd_lists=[]
    for i in tb:
        tb_lists.append(i.price)
    for i in jd:
        jd_lists.append(i.price)
    length=min(len(tb_lists),len(jd_lists))
    tt_lists=tb_lists[0:length]
    jd_lists=jd_lists[0:length]
    plt.figure(figsize=(7,4))
    plt.plot(tt_lists,'o--',label='淘宝价格排行',color='red')
    plt.plot(jd_lists,'o--', label='京东价格排行', color='blue')
    plt.xlabel("店铺")
    plt.ylabel("价格")
    plt.title("商品价格图")
    '''
    min_price=float(min(min(tt_lists),min(jd_lists)))
    max_price=float(max(max(tt_lists),max(jd_lists)))
    plt.ylim(min_price,max_price)
    '''
    plt.legend()
    price_picurl='static/%s.png'%key
    plt.savefig(price_picurl)
    plt.close()
    return price_picurl