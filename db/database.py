#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
import time

class database():
    conn = MongoClient('127.0.0.1')
    # conn = MongoClient(host='192.168.8.162', port=27017, connect=False, serverSelectionTimeoutMS=3)
    db = conn['ads']

    @classmethod
    def getDB(cls):
        return cls.db

