# -*- coding: utf-8 -*-
import os, sys
import logging


def logger():
    # 获取logger的实例
    logger = logging.getLogger("log/log.txt")
    # 可以设置日志的级别
    logger.setLevel(logging.INFO)

    # 指定logger的输出格式
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    # 获取文件处理器，并设置级别
    file_handler = logging.FileHandler("log/log.txt")
    file_handler.setLevel(logging.INFO)
    # 文件日志按照指定的格式来写
    file_handler.setFormatter(formatter)

    # 终端日志对象
    # console_handler = logging.StreamHandler(sys.stdout)
    # 终端日志按照指定的格式来写
    # console_handler.setFormatter(formatter)

    # 把文件日志，终端日志对象添加到日志处理器logger中
    logger.addHandler(file_handler)
    # logger.addHandler(console_handler)

    return logger

# 不用的时候，将日志的hanlder移除
# 否则会常驻内存
# logger.removeHandler(file_handler)
# logger.removeHandler(console_handler)


def my_log():
    logging.basicConfig(level=logging.WARN,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.join(os.path.dirname(__file__), "log") + "web.log",
                        filemode='w')
    return logging


print(os.path.dirname(__file__))

