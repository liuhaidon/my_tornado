# encoding:utf-8
import json
from logger import *
from passlib.hash import pbkdf2_sha512

from tornado.escape import json_encode,json_decode
from BaseHandler import BaseHandler
from bson import DBRef, ObjectId
import time


class AdminLoginHandler(BaseHandler):
    """登录"""
    def get(self):
        print self.request.arguments
        print self.request.headers
        nexts = self.request.arguments.get("next")
        referer_url = '/admin/home'
        if 'Referer' in self.request.headers:
            referer_url = '/' + '/'.join(self.request.headers['Referer'].split("/")[3:])
        error = ""
        username = self.get_cookie("username")
        if username:
            error = "您已登录账号:%s,如继续则退出当前账号" % username

        next = referer_url
        if nexts:
            next = nexts[0]
        else:
            url = ""
        print "url===>", url
        self.render("backend/login.html", url=next, error=error)

    def post(self, *args, **kwargs):
        print self.request.arguments
        self.logging.info(('LoginHandler argument %s') % (self.request.arguments))
        url, pwd, name = (value[0] for key, value in self.request.arguments.items() if key != '_xsrf'
                          and key != 'checkbox')
        if not pwd:
            self.render("backend/login.html", url=url, error="密码不能为空")
        self.logging.info(('admin user  %s login in' % (name)))

        res = self.begin_backend_session(name, pwd)
        if not res:
            self.render("backend/login.html", url=url, error="用户名或密码不正确")
        ip_info = self.request.remote_ip
        # logger().info("登陆用户：%s===>" % (name))
        name = "登陆用户：" + name
        self.application.dbutil.login(name, ip_info)
        if url == '/admin/login':
            self.redirect('/admin/home')
        else:
            self.set_cookie("username", name)
            self.redirect(url)


class AdminLogoutHandler(BaseHandler):
    """注销"""
    def get(self):
        self.post()

    def post(self):
        self.end_backend_session()
        self.redirect('/admin/login')


class AdminHomeHandler(BaseHandler):
    """后台主页"""
    @BaseHandler.admin_authed
    def get(self):
        # myuser = self.get_cookie("username")
        myuser = self.admin
        self.render("backend/home.html", myuser=myuser, admin_nav=0)


class AdminSysUsers(BaseHandler):
    """查询用户"""
    @BaseHandler.admin_authed
    def get(self):
        current_page = int(self.get_argument("page", 1))
        RECORD_OF_ONE_PAGE = self.application.settings["record_of_one_page"]
        skiprecord = RECORD_OF_ONE_PAGE * (current_page - 1)

        user_list = self.application.dbutil.getUsers(skiprecord, RECORD_OF_ONE_PAGE)
        count = len(user_list)

        pages = int(round(count / RECORD_OF_ONE_PAGE))
        if count % RECORD_OF_ONE_PAGE:
            pages += 1

        list_page = []
        if current_page > 1:
            last_page = '<a href="/admin/sysusers?page=%s">上一页</a>' % (current_page - 1)
        else:
            last_page = '<a href="/admin/sysusers?page=%s">上一页</a>' % (current_page)
        list_page.append(last_page)

        for p in range(pages):
            tmp = '<a href="/admin/sysusers?page=%s">%s</a>' % (p + 1, p + 1)
            list_page.append(tmp)

        if current_page < pages:
            next_page = '<a href="/admin/sysusers?page=%s">下一页</a>' % (current_page + 1)
        else:
            next_page = '<a href="/admin/sysusers?page=%s">下一页</a>' % (current_page)
        list_page.append(next_page)
        str_page = "".join(list_page)

        # myuser = self.get_cookie("username")
        myuser = self.admin
        self.render("backend/system_user_query.html", myuser=myuser, admin_nav=11, users=user_list,
                    current_page=current_page, page_count=str_page, count=count)


class AdminFindSysUser(BaseHandler):
    """查找用户是否已经注册过"""
    @BaseHandler.admin_authed
    def post(self):
        username = self.get_argument("username", None)
        flag = self.application.dbutil.findUser(username)
        if not flag:
            self.write(json.dumps({"status": 'error', "msg": u'已经注册过'}))
        else:
            self.write(json.dumps({"status": 'ok', "msg": u'没有注册过'}))


class AdminAddSysUser(BaseHandler):
    """添加用户"""
    @BaseHandler.admin_authed
    def post(self):
        info = dict()
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        role = self.get_argument("role", None)
        createdat = time.strftime("%Y-%m-%d %H:%M:%S")

        ip_infp = self.request.remote_ip

        info["username"] = username
        info["password"] = password
        info["role"] = role

        for k, v in info.iteritems():
            if not v:
                return self.write(json.dumps({"status": 'error', "msg": k + "为必选项，请输入信息！"}))

        res = self.application.dbutil.addUser(username, password, role, createdat, ip_infp)
        if not res:
            logger().info("增加用户失败：===>")
            return self.write(json.dumps({"msg": u'增加用户失败', "status": 'error'}))
        logger().info("增加用户成功：===>")
        return self.write(json.dumps({"status": 'ok', "msg": u"增加用户成功！"}))


class AdminDeleteSysUser(BaseHandler):
    """删除用户"""
    @BaseHandler.admin_authed
    def post(self):
        datas = self.request.arguments
        del datas['_xsrf']
        ip_infp = self.request.remote_ip
        for key, value in datas.items():
            uid = int(value[0])
            flag = self.application.dbutil.delUser(uid, ip_infp)
        if flag:
            logger().info("删除用户失败：===>")
            self.write(json.dumps({"status": 'ok', "msg": u'删除系统用户成功'}))
        logger().info("删除用户成功：===>")
        self.write(json.dumps({"status": 'ok', "msg": u'删除系统用户失败'}))


class AdminModifySysUser(BaseHandler):
    """修改用户"""
    @BaseHandler.admin_authed
    def get(self, id):
        record = self.db.tb_system_user.find_one({"_id": ObjectId(id)})
        return self.render("backend/system_user_modify.html", myuser=self.admin, admin_nav=21, user=record)

    def post(self, id):
        newprofile = {
            'id': self.get_argument("id", None),
            'userid': self.get_argument("userid", None),
            'brief': self.get_argument("brief", None),
            'mobile': self.get_argument("mobile", None),
            'status': self.get_argument("status", None),
            'regtime': self.get_argument("regtime", None),
        }
        for k, v in newprofile.iteritems():
            if not v:
                return self.write(json.dumps({"status": 'error', "msg": k + "为必选项，请输入信息！"}))
        return self.write(json.dumps({"status": 'ok', "msg": "修改管理员用户成功！"}))


class AdminRepassSystem(BaseHandler):
    """修改密码"""
    @BaseHandler.admin_authed
    def post(self):
        datas = self.request.arguments
        ip_infp = self.request.remote_ip

        pass3 = self.get_argument("password3", None)
        pass4 = self.get_argument("password4", None)
        if pass3 != pass4:
            return self.write(json.dumps({"status": 'error', "msg": "确认密码跟新密码不一致！"}))

        pass3 = pbkdf2_sha512.encrypt(pass3)
        userid = self.get_argument("uid", None)
        print "pass3===>", pass3
        flag = self.application.dbutil.updatePassWord(userid, pass3, ip_infp)
        if not flag:
            logger().info("修改用户密码失败：===>")
            self.write(json.dumps({"status": 'ok', "msg": u'修改密码失败'}))
        logger().info("修改用户密码成功：===>")
        self.write(json.dumps({"status": 'ok', "msg": u'修改密码成功'}))
































