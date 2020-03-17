# -*- coding:utf-8 -*-
import re
# s = '''first line
#        second line
#        third line'''
# result = re.match('\w+', s) #返回l
# print result
# re.search(r'y','liuyan1').group() #返回y
import pymysql,time
from passlib.hash import pbkdf2_sha512
class DBUtil:
    def __init__(self, **kwargs):
        user = kwargs.get('user', 'tornado')
        password = kwargs.get('password', 'liujiadon')
        host = kwargs.get('host', '106.15.88.182')
        port = kwargs.get('port', 3306)
        database = kwargs.get('database', 'tornado')
        charset = kwargs.get('charset', 'utf8')
        connection = pymysql.connect(user=user, password=password, host=host, port=port, database=database, charset=charset)
        self.connection = connection
        if connection:
            self.cursor = connection.cursor()
        else:
            raise Exception('数据库连接参数有误！')
db = DBUtil()
password = pbkdf2_sha512.encrypt("999999")
createdat = time.strftime("%Y-%m-%d %H:%M:%S")
try:
    sql_str = "INSERT INTO tb_user(userid,username,password,role,createdat) VALUES (null, '%s', '%s', '%s', '%s')" % (
    "hai", password, "test", createdat)
    db.cursor.execute(sql_str)
    db.connection.commit()
except:
    db.connection.rollback()

