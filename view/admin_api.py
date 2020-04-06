# encoding:utf-8
from BaseHandler import BaseHandler
import time
from base64 import b64encode, b64decode
import sys
import json
from view.__init__ import *
# 参考：http://blog.sina.com.cn/s/blog_13d84115b0102yg6q.html
# 参考：https://www.cnblogs.com/Erick-L/p/7237459.html
# https://blog.csdn.net/WGH100817/article/details/101722014
# https://www.cnblogs.com/wanghzh/articles/5898327.html


class AdminSaveLog(BaseHandler):
    @BaseHandler.api_authentication
    def post(self):
        sitename = self.get_argument("sitename", None)
        log_type = self.get_argument("log_type", None)
        content = self.get_argument("content", None)
        headers = self.request.headers
        auth = headers.get("auth-api", None)
        if not auth:
            return self.write(json.dumps({"status": False, "msg": "can not to access！"}))
        result = self.check_auth(auth)
        if not result:
            return self.write(json.dumps({"status": False, "msg": "auth fail！"}))
        if content:
            content = json.loads(content)
            sql = "INSERT INTO table_log(r_time,r_type,r_url,r_code,r_size,referer,user_agent,spider,ip,domain) VALUES"
            count = 1
            for c in content:
                r_time = c.get("rtime", time.strftime("%Y/%m/%d %H:%M:%S"))
                r_type = c.get("rtype", "POST")
                r_url = c.get("rurl", "http://www.baidu.com")
                r_code = c.get("rcode", "200")
                r_size = c.get("rsize", "6.38")
                referer = c.get("referer", "")
                user_agent = c.get("user_agent", "")
                spider = c.get("spider", "")
                ip = c.get("ip", "")
                domain = c.get("domain", "")
                if count == 1:
                    sql += "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    r_time, r_type, r_url, r_code, r_size, referer, user_agent, spider, ip, domain)
                else:
                    sql += ",('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    r_time, r_type, r_url, r_code, r_size, referer, user_agent, spider, ip, domain)
                count += 1
        if sitename == "test_log":
            result = self.application.dbutil1.save(sql)
        elif sitename == "www.alige.com":
            result = self.application.dbutil2.save(sql)
        return self.write(json.dumps(result))

    def check_xsrf_cookie(self):
        _xsrf = self.get_argument("_xsrf", None)

    def check_auth(self, auth):
        if auth == "bt.cn.auth":
            return True
        else:
            return False


# class AdminSelectLog(BaseHandler):
#     def get(self):
#         choose = self.get_argument("choose", None)
#         content = self.get_argument("content", None)
#         sitename = self.get_argument("sitename", None)
#         headers = self.request.headers
#         auth = headers.get("auth-api", None)
#         if not auth:
#             return self.write(json.dumps({"status": False, "msg": "can not to access！"}))
#         result = self.check_auth(auth)
#         if not result:
#             return self.write(json.dumps({"status": False, "msg": "auth fail！"}))
#         if sitename == "test_log":
#             sql = "SELECT * from table_log where %s='%s'" % (choose, content)
#             result = self.application.dbutil1.select(sql)
#         elif sitename == "www.alige.com":
#             sql = "SELECT * from table_log where %s='%s'" % (choose, content)
#             result = self.application.dbutil2.select(sql)
#         for r in result:
#             print("r===>", r)
#         return self.write(json.dumps({"status": "success", "msg": result}))
#
#     def check_auth(self, auth):
#         if auth == "bt.cn.auth":
#             return True
#         else:
#             return False

