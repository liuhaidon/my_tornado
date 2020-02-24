# encoding:utf-8
import time, sys,pymongo
from BaseHandler import BaseHandler
if sys.version_info[0] == 3:
    from importlib import reload
if sys.version_info[0] == 2:
    reload(sys)
    sys.setdefaultencoding("utf-8")

class AdminSysUsers1(BaseHandler):
    """系统用户列表"""
    @BaseHandler.admin_authed
    def get(self):
        current_page = int(self.get_argument("page", 1))             # 当前第几页,默认第一页
        pagesize = self.application.settings["record_of_one_page"]   # 每页显示多少条记录

        skiprecord = pagesize * (current_page - 1)
        user_list = self.application.dbutil.getUsers(skiprecord, pagesize)
        user_list = self.db.tb_system_user.find({}).sort("time", pymongo.DESCENDING).skip((current_page - 1) * pagesize).limit(pagesize)

        # 一共有多少条记录
        count = self.application.dbutil.getAllUsers()
        # 一共有多少页
        pages = count / pagesize
        if count % pagesize > 0:
            pages += 1
        return self.render("backend/system_user_query.html", myuser=self.admin, admin_nav=22, users=user_list, page=current_page, pagesize=pagesize, pages=pages, count=count)
