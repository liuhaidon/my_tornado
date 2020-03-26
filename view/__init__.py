#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import random
import sys
sys.path.append("..")

from db.database import database

def id_auto_increment(last, id):
    """id自增1"""
    if last.count() > 0:
        lastone = dict()
        for item in last:
            lastone = item
        return str(int(lastone.get(id, 80000000)) + 1)
    else:
        return "80000001"


def strtodatetime(datestr, format):
    return datetime.datetime.strptime(datestr, format)


def datediff(beginDate, endDate):
    """计算时间相差天数，输入格式为：str"""
    format = "%Y-%m-%d %H:%M:%S"
    bd = strtodatetime(beginDate, format)
    ed = strtodatetime(endDate, format)
    oneday = datetime.timedelta(days=1)
    count = 0
    while bd.date() < ed.date():
        ed = ed - oneday
        count += 1
    return count


def random_number(length):
    """生成随机位数字符"""
    # seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    seed = "01234567890"
    sa = []
    for i in range(length):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt

def scheduler_job(app):
    pass

def load_base_data(app):
    db = database.getDB()

    #1.robots data
    robots = db.tb_robert_profile.find({}, {"_id": 0})
    g_robots = {"quene":[]}
    for v in robots:
        openId = "#"+v.get("openId")
        v["openId"] = openId
        g_robots["quene"].append(openId)
        g_robots[openId] = v
    app.robots = g_robots
    print("robots==>", app.robots)

def list_to_dict(field, list):
    """列表转成字典："""
    data_list = []
    for u in list:
        data = dict(zip(field, u))
        data_list.append(data)
    return data_list