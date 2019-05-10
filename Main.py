# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web

from view.admin import *
from tornado.options import define, options
from db.mysql import DBUtil
from utils.session import *
import socket
import threading
from apscheduler.schedulers.background import BackgroundScheduler

from session.session import MongoSessions
from session.auth import MongoAuthentication

define("domain", default="", help="run on the given domain", type=str)
define("ip", default="162.247.101.143", help="run on the given port", type=str)
define("port", default=8081, help="run on the given port", type=int)
define("develop", default=True, help="develop environment", type=bool)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/domain/api", AdminPutDomain),  # 域名入库

            (r"/admin/login", AdminLoginHandler),
            (r"/admin/logout", AdminLogoutHandler),
            (r"/admin/home", AdminHomeHandler),

            (r"/admin/sysusers", AdminSysUsers),
            (r"/admin/sysuser/add", AdminAddSysUser),
            (r"/admin/sysuser/delete", AdminDeleteSysUser),
            (r"/admin/sysuser/([0-9a-z]{24})", AdminModifySysUser),
            (r"/admin/system/repass", AdminRepassSystem),

            (r"/admin/domains", AdminDomains),
            # (r"/admin/domain/put", AdminPutDomain),
            (r"/admin/domain/add", AdminAddDomain),
            (r"/admin/domain/delete", AdminDeleteDomain),
            (r"/admin/domain/select", AdminSelectDomain),
            (r"/admin/domain/flag", AdminFlagDomain),
            (r"/admin/domain/update", AdminUpdateDomain),

            (r"/admin/keywords", AdminKeyWords),
            (r"/admin/keyword/add", AdminAddKeyWord),
            (r"/admin/keyword/delete", AdminDelKeyWord),
            (r"/admin/keyword/select", AdminSelectKeyWord),

            (r"/admin/ip_pool", AdminIpPool),
            (r"/admin/ip_address/add", AdminAddIp),
            (r"/admin/ip_address/delete", AdminDeleteIp),
            (r"/admin/ip_address/select", AdminSelectIp),
        ]
        self.dbutil = DBUtil()
        settings = dict(
            cookie_secret="e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
            xsrf_cookies=True,
            login_url='/login',
            admin_login_url="/admin/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            upload_path=os.path.join(os.path.dirname(__file__), "static/media"),
            json_path=os.path.join(os.path.dirname(__file__), "json"),
            attachment_path=os.path.join(os.path.dirname(__file__), "attachment"),
            develop_env="true",
            session_secret="3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
            session_timeout=1800,
            store_options={
                'redis_host': '127.0.0.1',
                'redis_port': 6380,
                'redis_pass': 'redis123',
            },
            record_of_one_page=15,
        )

        self.settings = settings
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = SessionManager(settings["session_secret"], settings["store_options"],
                                              settings["session_timeout"])

def task():
    dbutil = DBUtil()
    result = dbutil.task()
    dmlist = result[0]
    kwlist = result[1]
    array = []
    time.sleep(10)
    # print dmlist
    ua_list = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
               "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
               "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
               "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
               "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0",
               "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
               "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE"]
    ua = random.choice(ua_list)
    ua_header = {"User-Agent": ua}
    for d in dmlist:
        dname = d["domain"]
        dname = dname.encode("utf-8")
        domain = "http://" + dname
        # print "=========>",domain
        try:
            # 设置3秒爬取超时
            res = requests.get(domain, headers=ua_header, timeout=3)
            res.encoding = "utf-8"
            content = res.text
        except:
            continue

        # print "domain===>",dname
        # ip = socket.gethostbyname(dname)
        # print "ip===>",ip
        # sip = {'ip': ip}
        # time.sleep(0.1)
        # info = checkip(sip)
        # ip_info = ip + "=>" + info
        # d["ip_info"] = ip_info

        # titleRe = re.compile(r'<title>(.*)</title>|<meta name="keywords" content="(.*)"/>|<meta name="description" content="(.*)"/>')
        titleRe1 = re.compile(r'<title>(.*)</title>')
        titleRe2 = re.compile(r'<meta name="keywords" content="(.*)">')
        titles = titleRe1.findall(content)
        description = titleRe2.findall(content)
        if titles:
            d["webname"] = titles[0]
        else:
            d["webname"] = ""
        if description:
            d["contect"] = description[0]
        else:
            d["contect"] = ""
        d["status"] = "正常"
        d["type"] = "正常"
        d["createdat"] = time.strftime("%Y-%m-%d %H:%M:%S")

        titles.extend(description)
        arr2 = []
        for i in titles:
            for y in i:
                if y:
                    arr2.append(y)
        str = "".join(arr2)

        if not kwlist:
            break
        for kw in kwlist:
            keyword = kw["keyword"]
            mold = kw["type"]
            if mold == "标题":
                if keyword in str:
                    d["status"] = "待处理"
                    d["type"] = "非法网站"
                    break
            else:
                if keyword in content:
                    d["status"] = "待处理"
                    d["type"] = "非法网站"
                    break
        array.append(d)
    # print "array===>", array
    if array:
        dbutil.check(array)

# def checkip(ip):
#     URL = 'http://ip.taobao.com/service/getIpInfo.php'
#     info = ""
#     try:
#         r = requests.get(URL, params=ip, timeout=3)
#     except requests.RequestException as e:
#         print(e)
#     else:
#         try:
#             json_data = r.json()
#         except:
#             return info
#         if json_data[u'code'] == 0:
#             province = json_data[u'data'][u'region'].encode('utf-8')
#             city = json_data[u'data'][u'city'].encode('utf-8')
#             info = province + city
#         else:
#             print '查询失败,请稍后再试！'
#     return info
# def com():
#     print "mmm================="

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print("visit at", "http://127.0.0.1:%s" % options.port)

    # tornado.ioloop.PeriodicCallback(task, 1000 * 5).start()

    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()
    # 添加调度任务,调度方法为 timedTask，触发器选择 interval(间隔性)，间隔时长为 6 秒
    scheduler.add_job(task, 'interval', seconds=6)
    # scheduler.add_job(com, 'interval', seconds=6)
    # 启动调度任务
    scheduler.start()

    tornado.ioloop.IOLoop.instance().start()