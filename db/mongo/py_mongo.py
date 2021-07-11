#!/usr/bin/python3
# -*- coding:utf-8 -*-
import time
import random
from pymongo import MongoClient
from bson import DBRef, ObjectId

conn = MongoClient(host='127.0.0.1', port=27017, connect=False, serverSelectionTimeoutMS=3)
db = conn['tornado']   # 返回tornado数据库,也可使用:db = conn.test

b = db["tb_user_profile"]
b.remove({})

# user = a["tb_gamedata_profile"]
# user = a["tb_exam_task]
# user = user.find_one({"openid": "oxK4Y49djryCbQ8ayK5A22URZKmk"})
# user_info = user.get("user_info")
# user_info["degree"] = 1
# users.update_one({"openid": "oxK4Y49djryCbQ8ayK5A22URZKmk"},{"$set":{"user_info":user_info}})
# user.remove({})

# aaa = a["tb_gamedata_profile"]
# aaa.remove({})
# user.remove({})

# sys = a["tb_fight_record"]
# sys.update_one({"id":6},{"$set":{"participants":[]}})
# sys.remove()


# b = a["tb_fight_task"]
# b.remove()

# f = a["tb_friend_profile"]
# f.remove({})
# f.insert({"openid": "oxK4Y49djryCbQ8ayK5A22URZKmk", "friendOpenid": "oxK4Y4-zAZ9Hq0pDcrjh0vwH1_bk"})
#           {"openid": "o8Q135M16EEAy7f5G3S1bnsVU_Bc", "friendOpenid": "o8Q135AKlAInUGDNJ8_QFzGJzbPg"},
#           {"openid": "o8Q135H-6r5qczfdIXXIuyxwi_0U", "friendOpenid": "o8Q135AKlAInUGDNJ8_QFzGJzbPg"}])

# f = a["tb_exam_task"]
# b = f.update_one({"id": 6},{"$set":{"participants":{}}})

# f = a["tb_quiz_task"]
# b = f.remove({"openid":"oxK4Y49djryCbQ8ayK5A22URZKmk"})

# f = a["tb_exam_task"]
# f.update({"id":2},{"$set":{"participants":{}}})
# a = conn["yearbook"]
# stu = a["student"]
# student1 = {'name': 'aaa','age': 20,'gender': '男',"score":[10,20,30]}
# student2 = {'name': 'bbb','age': 23,'gender': '男',"score":[40,56,56]}
# student3 = {'name': 'ccc','age': 26,'gender': '女',"score":[55,66,68],"ask":{"a":1,"b":"ss"}}
# stu.insert([student1,student2,student3])
# stu.remove({"age":[20,23]})
# arr = [20,23]
# for i in arr:
#     stu.remove({"age":i})

# b = "%05d" % 12
# print b,type(b)

# import time
# t = time.time()
# t = time.ctime()
# t = time.sleep(3)
# print t

# import xlwt
# 实例化一个Workbook()对象(即创建一个Excel文件)
# wbk = xlwt.Workbook()





