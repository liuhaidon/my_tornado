#!/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from view.admin import *
from view.ajax import *
from view.front import *
from db.mysql import DBUtil
from utils.session import *
from utils.ueditor import *
from utils.pay import *

from session.session import MongoSessions
from session.auth import MongoAuthentication
from apscheduler.schedulers.background import BackgroundScheduler

define("domain", default="", help="run on the given domain", type=str)
define("ip", default="162.247.101.143", help="run on the given port", type=str)
define("port", default=8066, help="run on the given port", type=int)
define("develop", default=True, help="develop environment", type=bool)

'''
    author: liu
    时间: 2019/09/23
    服务端的架构体系:
        db  : adspush (mongodb)
        session : 基于mongodb
'''

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", index),
            (r"/index", index),
            (r"/login", user_login),
            (r"/logout", user_logout),

            (r"/admin/login", AdminLoginHandler),
            (r"/admin/logout", AdminLogoutHandler),
            (r"/admin/home", AdminHomeHandler),

            (r"/admin/sysusers", AdminSysUsers),
            (r"/admin/sysuser/add", AdminAddSysUser),
            (r"/admin/sysuser/delete", AdminDeleteSysUser),
            (r"/admin/sysuser/([0-9a-z]{24})", AdminModifySysUser),
            (r"/admin/system/repass", AdminRepassSystem),

            (r"/admin/permissions", AdminPermissions),
            (r"/admin/permission/add", AdminAddPermission),
            (r"/admin/permission/delete", AdminDeletePermission),

            (r"/admin/media/contents", AdminContents),

            (r"/ajax/sysuser/find", AjaxFindSysUser),
            (r"/ajax/permission/bind", AjaxBindPermission),  # 点击权限绑定
            (r"/ajax/bind/permission", AjaxPermissionBind),  # 点击确定

            (r"/admin/notices", AdminNoticeList),
            (r"/admin/notice/add", AdminAddNotice),
            (r"/admin/notice/delete", AdminDeleteNotice),
            # (r"/admin/notice/([0-9a-z]{24})", AdminModifyNotice),

            (r"/ajax/upload_image", UploadImageFile),        # 上传图片
            (r"/ajax/upload_video", UploadVideoFile),        # 上传视频
            (r"/admin/media/upload", RemotePictureHandler),   # 上传富文本：还要改动html页面与ueditor.py页面

            # (r"/admin/login/select", AdminLoginSelect),   # 用户登陆记录查询
            # (r"/admin/login/delete", AdminLoginDelete),   # 用户登陆记录删除

            (r"/hehe", AdminIndex),
            (r"/pay", AdminPay),
            (r"/aysic", AdminAysic),
            (r"/result", AdminResult),
        ]
        self.dbutil = DBUtil()
        self.frontend_auth = MongoAuthentication("ads", "tb_store_profile", "loginid")
        self.backend_auth = MongoAuthentication("ads", "tb_system_user", "userid")
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
                'redis_port': 6379,
                'redis_pass': 'redis123',
            },
            record_of_one_page=10,
            # ui_modules={
            #     "VideosListDisplay": VideosListDisplay,
            #     "ParticipantsListDisplay": ParticipantListDisplay,
            # }
        )

        self.settings = settings
        tornado.web.Application.__init__(self, handlers, **settings)
        self.session_manager = SessionManager(settings["session_secret"], settings["store_options"],
                                              settings["session_timeout"])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print("visit at", "http://127.0.0.1:%s" % options.port)

    # 创建后台执行的 schedulers
    scheduler = BackgroundScheduler()
    # 添加调度任务,调度方法为 timedTask，触发器选择 interval(间隔性)，间隔时长为 30 秒
    # scheduler.add_job(task, "cron", hour="13", minute="03", second="0")
    # scheduler.add_job(task, "interval", seconds=60*60*24)   # 定期执行任务
    # 启动调度任务
    scheduler.start()

    # t = threading.Thread(target=task, args=())
    # t.start()
    scheduler_job(app)   # 执行计划任务，定时推送任务
    tornado.ioloop.IOLoop.instance().start()
