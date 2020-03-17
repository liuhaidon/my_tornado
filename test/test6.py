import tornado.ioloop
import tornado.web
from tornado.options import define, options
import os.path,time,requests

define("port", default=8003, help="run on the given port", type=int)

class WelcomeHandler(tornado.web.RequestHandler):
    def get(self):
        time.sleep(8)
        response = requests.get("http://www.baidu.com", timeout=8)
        response = response.text
        return self.write(response)

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("### welcome !!! ###")

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