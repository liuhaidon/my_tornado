#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sqlite3

class Sqlite():
    __DB_FILE = None  # 数据库文件
    __DB_CONN = None  # 数据库连接对象
    __DB_TABLE = ""   # 被操作的表名称

    def __init__(self):
        self.__DB_FILE = "data/default.db"

    def __GetConn(self):
        # 取数据库对象
        try:
            if self.__DB_CONN == None:
                self.__DB_CONN = sqlite3.connect(self.__DB_FILE)
                self.__DB_CONN.text_factory = str
        except Exception as ex:
            return "error: " + str(ex)

sql.table('users').where('id=?',(1,)).setField('username',username)

result = sql.table('users').where('id=?',(1,)).setField('password',public.md5(password))
username = sql.table('users').where('id=?',(1,)).getField('username')
