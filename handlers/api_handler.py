# -*-coding:utf-8-*-
import json
import time
import hashlib
import tornado.web

access_record = []
PID_LIST = ['qwe', 'ioui', '234s']


class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        # 获取url中全部数据
        pid = self.get_argument('pid', None)
        # 获取变量
        m5, client_time, i = pid.split('|')

        server_time = time.time()
        # 时间超过10s禁止
        if server_time > float(client_time) + 10:
            return self.write('滚')
        # 处理10s内容重复的请求
        if pid in access_record:
            return self.write('滚')
        access_record.append(pid)

        pid = PID_LIST[int(i)]
        ramdom_str = "%s|%s" % (pid, client_time)
        h = hashlib.md5()
        h.update(bytes(ramdom_str, encoding='utf-8'))
        server_m5 = h.hexdigest()
        # print(m5,server_m5)
        if m5 == server_m5:
            self.write("Hello, world")
        else:
            self.write('滚')


api_urls = [
    (r"/api/auth", AuthHandler),
]


if __name__ == "__main__":
    pass

# https://www.cnblogs.com/liujianzuo888/articles/5891068.html
# https://www.cnblogs.com/melonjiang/p/5704542.html
# https://www.cnblogs.com/zcok168/p/10104309.html
# https://www.bbsmax.com/A/1O5EbOAyd7/
# https://www.cnblogs.com/Erick-L/p/7237459.html
# https://blog.saintic.com/blog/241.html
# https://www.sohu.com/a/323076814_120145691
# https://blog.csdn.net/xiaochendefendoushi/article/details/81141096
