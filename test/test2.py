# -*- coding:utf-8 -*-

import tornado.web         # web服务
import tornado.ioloop      # I/O 时间循环
import tornado.httpserver  # 新引入httpserver模块，单线程的http服务
from tornado.options import define, options

define("ip", default="", help="run on the given ip", type=str)
define("port", default=8066, type=int, help="run on the given port")
define("domain", default=[], type=str, help="run on the given domain", multiple=True)

class Mainhandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world!")

app = tornado.web.Application([
        (r"/index", Mainhandler),
    ])

if __name__ == "__main__":
    # 如果命令行没有传值，则使用默认值
    # tornado.options.parse_command_line()
    tornado.options.parse_config_file(path)
    # print tornado.options.options  # 输出多值选项

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    # tornado.ioloop.IOLoop.current().start()
    tornado.ioloop.IOLoop.instance().start()