#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from pymongo import MongoClient
# from mongoengine import connect


class database():
    conn = MongoClient('127.0.0.1')
    # time.sleep(2)
    # conn = MongoClient(host='127.0.0.1', port=27017, connect=False, serverSelectionTimeoutMS=6)
    db = conn['tornado']

    @classmethod
    def getDB(cls):
        return cls.db

