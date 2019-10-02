#!/usr/bin/env python
# -*- coding:utf-8 -*-
from BaseHandler import BaseHandler
from view import *


class index(BaseHandler):
    def get(self):
        store = dict()
        store["playlist"] = [{"post": "ccc"}]
        return self.render("frontend/video.html", myuser=store)


class user_login(BaseHandler):
    """登录页"""
    def get(self):
        nexts = self.request.arguments.get("next")
        print(self.request)
        print(self.request.headers)
        referer_url = '/index'
        if 'Referer' in self.request.headers:
            referer_url = '/' + '/'.join(self.request.headers['Referer'].split("/")[3:])
            # print referer_url
        if self.user:
            if referer_url != '/register':
                self.redirect(referer_url)
        next = referer_url
        if nexts:
            next = nexts[0]
        self.render("frontend/login.html", url=next, error='')

    def check_xsrf_cookie(self):
        pass

    def post(self):
        print self.request.arguments
        userid = self.get_argument('account', None)
        pwd = self.get_argument('passwd', None)
        url = self.get_argument('url', None)
        print userid, pwd, url

        # print arguments.get('_xsrf', '')[0]
        # info = {}
        # if not mobile  or not pwd or arguments.get('_xsrf', '')[0] == '':

        # if not userid or not pwd:
        #     return self.render("frontend/login.html", url=url, error=u"登录异常", myuser={"loginid": userid})

        # res = self.begin_frontend_session(userid, pwd)
        # if not res:
        #     return self.render("frontend/login.html", url=url, error=u"用户名或密码不正确", myuser={"loginid": userid})

        print "url is ", url
        if url:
            self.redirect(url)
        else:
            self.redirect('/')

class user_logout(BaseHandler):
    """退出登录"""
    def get(self):
        self.post()

    def post(self):
        self.end_frontend_session()
        self.redirect('/login')

class test(BaseHandler):
    """测试推送"""
    @BaseHandler.authenticated
    def get(self):
        self.render("soc.html")