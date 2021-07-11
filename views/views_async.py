# -*- coding:utf-8 -*-
""" tornado 异步通信 """
import tornado.web
import tornado.gen
import tornado.ioloop
import tornado.httpclient
import time


class SyncHandler(tornado.web.RequestHandler):
    """ 同步抓取网页 """
    def get(self):
        client = tornado.httpclient.HTTPClient()   # 同步HTTPClient
        response = client.fetch('http://127.0.0.1:8003/sync')  # 8000已经启动，去访问sync（相当于调用接口）
        print("同步http请求得到响应===>", response.body)
        self.write('----SyncHandler---')


class AsyncHandler(tornado.web.RequestHandler):
    """ 异步抓取网页1: 通过回调函数实现异步 """
    @tornado.web.asynchronous  # 将请求变成长连接
    def get(self):
        client = tornado.httpclient.AsyncHTTPClient()   # 异步AsyncHTTPClient
        # 阻塞完毕后调用 callback
        response = client.fetch('http://127.0.0.1:8003/sync', callback=self.on_response)
        print("异步http请求得到响应===>", response)
        self.write('OK' + '<br>')

    def on_response(self, response):
        print("on_response被调用了======>>>", response)
        self.write('----CallbackSyncHandler---')
        self.finish()  # 回调结束，请求结束，响应到浏览器（否则浏览器一直等待状态）


class BlockHandler(tornado.web.RequestHandler):
    def get(self):
        print("block function start...")
        time.sleep(10)
        self.write('block function end...')


class SleepHandler(tornado.web.RequestHandler):
    @tornado.gen.coroutine # 异步
    def get(self):
        yield tornado.gen.sleep(5)
        self.write(str(dt.datetime.now()))


api_urls = [
    (r"/sync", SyncHandler),
    (r"/async", AsyncHandler),
    # (r"/gen", GenHandler),
    # (r"/func", FuncHandler),
    # (r"/exe", ExeHandler),
]


if __name__ == "__main__":
    pass
