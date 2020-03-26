import datetime

def datediff(beginDate, endDate):
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