import math
import numpy as np


def f_price(list):
    length = len(list)
    new_items = sorted(list)
    low = length / 4;
    high = length * 3 / 4
    x = new_items[int(low):int(high)]
    price = np.mean(x)
    low_price = price * 0.9;
    high_price = price * 1.1
    return low_price, high_price


def Sort(items):
    price_list = [];
    comment_list = []
    for i in items:
        price_list.append(float(i.price))
    for i in items:
        comment_num = 0
        if i.comment is None:
            pass
        else:
            for j in i.comment:
                comment_num = comment_num + int(i.comment[j])
        comment_list.append(comment_num)
    comment_list1 = np.array(comment_list)
    comment_list2 = np.where(comment_list1 < 10, 10, comment_list1)
    comment_list3 = np.log10(comment_list2) / math.e
    avg_comment = np.mean(comment_list3)
    low_price, high_price = f_price(price_list)
    for i in range(len(items)):
        if items[i].price < low_price:
            items[i].dis = 1 - (items[i].price - low_price) / low_price
            items[i].weight = items[i].dis * comment_list3[i]
        if items[i].price > high_price:
            if comment_list3[i] > avg_comment:
                items[i].dis = 1 + (items[i].price - high_price) / high_price
                items[i].weight = items[i].dis * comment_list3[i]
            else:
                items[i].dis = 1 - (items[i].price - high_price) / high_price
                items[i].weight = items[i].dis * comment_list3[i]
        else:
            items[i].dis = 1
            items[i].weight = items[i].dis * comment_list3[i]
    new_items = sorted(items, key=lambda x: x.weight, reverse=True)
    return new_items
