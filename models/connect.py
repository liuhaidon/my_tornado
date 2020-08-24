#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models.admin import Base as Abase
from models.resource_model import Base as Rbase
from models.app_config import Base

# ORM创建表结构
from sqlalchemy import create_engine

default_configs = app_settings[const.DB_CONFIG_ITEM][const.DEFAULT_DB_KEY]
engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (
    default_configs.get(const.DBUSER_KEY),
    default_configs.get(const.DBPWD_KEY),
    default_configs.get(const.DBHOST_KEY),
    default_configs.get(const.DBPORT_KEY),
    default_configs.get(const.DBNAME_KEY),
), encoding='utf-8', echo=True)


def create():
    Base.metadata.create_all(engine)
    Abase.metadata.create_all(engine)
    Rbase.metadata.create_all(engine)
    print('[Success] 表结构创建成功!')


def drop():
    Base.metadata.drop_all(engine)
    Abase.metadata.drop_all(engine)
    Rbase.metadata.drop_all(engine)
    print('[Success] 表结构删除成功!')


if __name__ == "__main__":
    create()

# https://blog.csdn.net/panfuyong11/article/details/104966451
# https://blog.csdn.net/weixin_37947156/article/details/75243267
# https://segmentfault.com/a/1190000003856556
