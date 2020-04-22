#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.crontab import *
from db.database import database
from apscheduler.schedulers.background import BackgroundScheduler
import random, datetime
import sys
sys.path.append("..")


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
    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()
    # 添加调度任务,调度方法为 timedTask，触发器选择 interval(间隔性)，间隔时长为 30 秒
    scheduler.add_job(test_task, "cron", hour="13", minute="03", second="0")
    scheduler.add_job(test_task, "interval", seconds=30)   # 定期执行任务,每隔30秒执行一次
    # 启动调度任务
    scheduler.start()

    # t = threading.Thread(target=task, args=())
    # t.start()


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