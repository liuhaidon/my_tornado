import functools
import tornado.web
import base64
import json
from tornado.escape import utf8
from hashlib import md5


class AuthHandler(tornado.web.RequestHandler):
    realm = "liu_hai_dong"
    basic_auth_conf = "config/basic_auth.json"

    def __init__(self, *argc, **argkw):
        super(AuthHandler, self).__init__(*argc, **argkw)

    def get_config_info(self):
        with open(self.basic_auth_conf, 'r') as fr:
            content = json.loads(fr.read())
        return content

    @classmethod
    def basic_authenticated(cls, method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            # Authorization: Basic base64("user:passwd")
            auth_header = self.request.headers.get('Authorization', None)
            if auth_header is not None:   # Basic YWRtaW46YWRtaW4=
                auth_mode, auth_base64 = auth_header.split(' ', 1)
                assert auth_mode == 'Basic'
                # auth_username, auth_password = auth_base64.decode('base64').split(':', 1)
                auth_username, auth_password = str(base64.b64decode(auth_base64), "utf-8").split(':', 1)
                if auth_username == 'admin' or auth_password == 'admin':
                    self.write('ok')
                else:
                    self.write('fail')
            else:
                '''
                HTTP/1.1 401 Unauthorized
                WWW-Authenticate: Basic realm="ren_jie"
                '''
                self.set_status(401)
                self.set_header('WWW-Authenticate', 'Basic realm="%s"' % cls.realm)
            return method(self, *args, **kwargs)
        return wrapper

# https://blog.csdn.net/junfeng666/article/details/79310992
# http://xiaorui.cc/archives/1904
# https://blog.csdn.net/yypsober/article/details/50718716
# https://zhidao.baidu.com/question/1450826798120826540.html
