# -*- coding:utf-8 -*-
import datetime


def date_diff(beginDate, endDate):
    """计算时间相差天数，输入格式为：str"""
    format = "%Y-%m-%d %H:%M:%S"
    bd = datetime.datetime.strptime(beginDate, format)
    ed = datetime.datetime.strptime(endDate, format)
    oneday = datetime.timedelta(days=1)
    count = 0
    while bd.date() < ed.date():
        ed = ed - oneday
        count += 1
    return count


def data_type(data):
    """ 判断数据类型 """
    if isinstance(data, str):
        return {"type": "", "msg": "字符串类型！"}
    if isinstance(data, bytes):
        return {"type": "", "msg": "字节类型！"}


def list_to_dict(field, list):
    """列表转成字典："""
    data_list = []
    for u in list:
        data = dict(zip(field, u))
        data_list.append(data)
    return data_list
# data_type("liu")
# data_type(b"liu")
