# encoding:utf-8

import json
import time
import os

from BaseHandler import BaseHandler
from view import *


class AjaxFindWebsite(BaseHandler):
    @BaseHandler.admin_authed
    def post(self):
        print "ajax==============>"
        arry = self.get_arguments("arry[]")
        print "arry=============>", arry
        num_arry = self.application.dbutil.getKeyDomain(arry)
        self.write(json.dumps(num_arry))


class AdminFindDetail(BaseHandler):
    @BaseHandler.admin_authed
    def get(self):
        keyword = self.get_argument("keyword")
        page = int(self.get_argument("page", 1))
        pagesize = int(self.get_argument("pagesize", "10"))

        skiprecord = pagesize * (page - 1)
        domainlist = self.application.dbutil.getKeywordDetails(skiprecord, pagesize, keyword)

        count = self.application.dbutil.getAllKeywordDetails(keyword)
        pages = count / pagesize
        if count % pagesize > 0:
            pages += 1

        # myuser = self.get_cookie("username")
        myuser = self.admin
        self.render("backend/keyword_details.html", myuser=myuser, admin_nav=31, domainlist=domainlist, page=page, pagesize=pagesize, pages=pages, count=count, keyword=keyword)


class AjaxBindPermission(BaseHandler):
    @BaseHandler.admin_authed
    def post(self):
        userid = self.get_argument("userid")
        result1 = self.application.dbutil.getUserPermission(userid)
        result2 = self.application.dbutil.getAllPermission()
        print "++++++++++++++++++++++++++++++"
        print result1
        print result2
        self.write(json.dumps({"userpermission": result1, "allpermission": result2}))


class AjaxPermissionBind(BaseHandler):
    @BaseHandler.admin_authed
    def post(self):
        userid = self.get_argument("userid")
        username = self.get_argument("username")
        permission_list = self.get_arguments('playlist[]')
        print "=====================>>>", userid, username, type(permission_list)
        # permission_list = json.loads(permission_list)
        for p in permission_list:
            print p
        result = self.application.dbutil.updatePermission(userid, username, permission_list)
        if not result:
            return self.write(json.dumps({"status": "success", "error": u'修改权限失败!'}))
        return self.write(json.dumps({"status": "success", "error": u'修改权限成功!'}))
