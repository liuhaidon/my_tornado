#!/usr/bin/env python
# -*- coding:utf-8 -*-       # encoding:utf-8
import io
from utils.validate import VerifyCode
from BaseHandler import BaseHandler
import tornado.web


class AdminParam(BaseHandler):
    def set_default_headers(self):
        self.set_header('aaa', '111')
        self.set_header('aaa', '222')
        self.add_header('www', '333')
        self.add_header('www', '444')
        self.clear_header('www')

    def get(self):
        return self.render("test_param.html")

    def write_error(self, status_code, **kwargs):
        self.write("status_code:%s" % status_code)


class AdminResult(BaseHandler):
    def post(self, *args, **kwargs):
        datas = self.request.arguments
        print("datas===>", datas)
        args1 = self.get_argument("args1", "")
        args2 = self.get_argument("args2", "")      # 接收字典
        args3 = self.get_arguments("args3[]")       # 接收数组
        args4 = self.get_arguments("args4[]")       # 接收数组
        print(args1, type(args1))   # liu <class 'str'>
        print(args2, type(args2))   # {"age":"30","name":"don"} <class 'str'>
        print(args3, type(args3))   # ['1', 'liu'] <class 'list'>
        print(args4, type(args4))   # ['{"age":26,"name":"liu"}', '{"age":28,"name":"hai"}'] <class 'list'>


class LoginCode(tornado.web.RequestHandler):
    def get(self):
        self.render("image_code.html")       # 打开登录页面

    def post(self):
        username = self.get_argument('username')  # 接收用户提交的用户名
        password = self.get_argument('password')
        code = self.get_argument('code')
        print(username, password, code)


class ImageCode(tornado.web.RequestHandler):
    def get(self):
        mstream = io.BytesIO()
        img, code = VerifyCode().GetCodeImage(30, 4)
        img.save(mstream, "PNG")        # 将返回的验证码图片数据，添加到BytesIO临时保存
        self.write(mstream.getvalue())  # 从BytesIO临时保存，获取图片返回给img的 src= 进行显示


class NotFoundHandler(BaseHandler):
    def get(self):
        self.send_error(404)

    def write_error(self, status_code, **kwargs):
        self.render("error.html")


# self.get_argument(name, default=_ARG_DEFAULT, strip=True)
# 从请求体和查询字符串中返回指定参数name的值，如果出现多个同名参数，则返回最后一个的值。
# self.get_arguments(name, strip=True)
# 从请求体和查询字符串中返回指定参数name的值，注意返回的是list列表（即使对应name参数只有一个值）。若未找到name参数，则返回空列表[]。
# https://www.jianshu.com/p/27e2d81beed4
# https://blog.csdn.net/yangczcsdn/article/details/81301999
# https://www.cnblogs.com/x54256/p/8186322.html