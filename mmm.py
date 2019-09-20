# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os.path, time, requests
import tornado.httpclient

from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

define("ip", default="162.247.101.143", help="run on the given port", type=str)
define("port", default=8006, help="run on the given port", type=int)

class WelcomeHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor()  # 当发生阻塞时，能够创建一个新的线程来执行阻塞的任务(多线程)
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = yield self.fun()
        print "response======>", response
        self.write('---exe----')
        self.finish()

    @run_on_executor
    def fun(self):
        print "fun()函数被调用了======>"
        time.sleep(15)
        response = requests.get('http://127.0.0.1:8006/sync')
        return response

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        print "走你"
        self.write("### welcome login ###")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', WelcomeHandler),
            (r'/login', LoginHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print("visit at", "http://127.0.0.1:%s" % options.port)
    tornado.ioloop.IOLoop.instance().start()