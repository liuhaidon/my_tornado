# encoding:utf-8
import json
import time,pymongo
from utils.logger import *
from view.ajax import *
from passlib.hash import pbkdf2_sha512

from tornado.escape import json_encode,json_decode
from BaseHandler import BaseHandler
from bson import DBRef, ObjectId


class AdminLoginRecord(BaseHandler):
    """用户登陆记录查询"""
    @BaseHandler.admin_authed
    def get(self):
        current_page = int(self.get_argument("page", 1))
        pagesize = self.application.settings["record_of_one_page"]
        skiprecord = pagesize * (current_page - 1)
        login_list = self.db.tb_login_record.find().skip(skiprecord).limit(pagesize).sort("atime", pymongo.ASCENDING)
        # login_list = self.db.tb_login_record.find().skip(skiprecord).limit(pagesize).sort("atime", pymongo.DESCENDING)
        pages = int(round(login_list.count() / pagesize))
        if login_list.count() % pagesize:
            pages += 1

        list_page = []
        if current_page > 1:
            last_page = '<a href="/admin/login/record?page=%s">上一页</a>' % (current_page - 1)
        else:
            last_page = '<a href="/admin/login/record?page=%s">上一页</a>' % (current_page)
        list_page.append(last_page)

        for p in range(pages):
            tmp = '<a href="/admin/login/record?page=%s">%s</a>' % (p + 1, p + 1)
            list_page.append(tmp)

        if current_page < pages:
            next_page = '<a href="/admin/login/record?page=%s">下一页</a>' % (current_page + 1)
        else:
            next_page = '<a href="/admin/login/record?page=%s">下一页</a>' % (current_page)
        list_page.append(next_page)
        str_page = "".join(list_page)
        self.render("backend/login_record_1.html", myuser=self.admin, admin_nav=11, login_list=login_list, page_count=str_page)


class AdminLoginDelete(BaseHandler):
    """删除用户登陆记录"""
    @BaseHandler.admin_authed
    def post(self):
        datas = self.request.arguments
        del datas['_xsrf']
        for key, value in datas.items():
            self.db.tb_login_record.remove({"_id": ObjectId(value[0])})
        self.write(json.dumps({"status": 'ok', "msg": u'删除登陆记录成功'}))


class AdminUserList(BaseHandler):
    """前端用户列表"""
    @BaseHandler.admin_authed
    def get(self):
        current_page = int(self.get_argument("page", "1"))
        pagesize = int(self.get_argument("pagesize", "20"))

        skiprecord = pagesize * (current_page - 1)
        sql = "select * from tb_user_profile order by createdat desc limit %s,%s" % (skiprecord, pagesize)
        user_list = self.application.dbutil.query(sql)
        field = ["id", "phone", "passwd", "createdat", "last_visit_time", "province", "city", "area"]
        data_list = list_to_dict(field, user_list)

        sql = "select count(*) from tb_user_profile"
        count = self.application.dbutil.queryall(sql)
        pages = count / pagesize
        if count % pagesize > 0:
            pages += 1
        self.render("backend/front_user_query.html", myuser=self.admin, admin_nav=21, users=data_list, page=current_page, pagesize=pagesize, pages=pages, count=count)


class AdminAddUser(BaseHandler):
    """添加前端用户"""
    @BaseHandler.admin_authed
    def post(self):
        phone = self.get_argument("phone", None)
        password = self.get_argument("password", None)
        province = self.get_argument("province", None)
        city = self.get_argument("city", None)
        area = self.get_argument("area", None)
        createdat = self.get_argument("createdat", None)
        last_time = time.strftime("%Y-%m-%d %H:%M:%S")
        info = dict()
        info["phone"] = phone
        info["password"] = password
        info["createdat"] = createdat
        for k, v in info.iteritems():
            if not v:
                return self.write(json.dumps({"status": 'error', "msg": k + "为必选项，请输入信息！"}))
        password = pbkdf2_sha512.encrypt(password)
        sql = "insert into tb_user_profile values(null, '%s', '%s', '%s', '%s', '%s', '%s','%s')" % \
              (phone, password, createdat, last_time, province, city, area)
        res = self.application.dbutil.execute(sql)
        if not res:
            return self.write(json.dumps({"msg": u'增加用户失败', "status": 'error'}))
        return self.write(json.dumps({"status": 'ok', "msg": u"增加用户成功！"}))


class AdminDeleteUser(BaseHandler):
    """删除前端用户"""
    @BaseHandler.admin_authed
    def post(self):
        datas = self.request.arguments
        del datas['_xsrf']
        for key, value in datas.items():
            uid = int(value[0])
            sql = "DELETE FROM tb_user_profile WHERE uid=%d" % uid
            result = self.application.dbutil.execute(sql)
        if not result:
            return self.write(json.dumps({"status": "error", "msg": u'删除用户失败'}))
        return self.write(json.dumps({"status": "ok", "msg": u'删除用户成功'}))


class AdminSysUsers(BaseHandler):
    """系统用户列表"""
    @BaseHandler.admin_authed
    def get(self):
        current_page = int(self.get_argument("page", 1))             # 当前第几页,默认第一页
        pagesize = self.application.settings["record_of_one_page"]   # 每页显示多少条记录

        user_list = self.db.tb_system_user.find({}).sort("time", pymongo.DESCENDING).skip((current_page - 1) * pagesize).limit(pagesize)
        pages = user_list.count() / pagesize
        if user_list.count() % pagesize > 0:
            pages += 1
        return self.render("backend/system_user_query.html", myuser=self.admin, admin_nav=22, users=user_list, page=current_page, pagesize=pagesize, pages=pages)


class AdminAddSysUser(BaseHandler):
    """添加用户"""
    @BaseHandler.admin_authed
    def post(self):
        print(self.request.arguments)
        info = dict()
        username = self.get_argument("userid", None)
        record = self.db.tb_system_user.find_one({"userid": username})
        if record:
            return self.write(json.dumps({"status": "error", "msg": "系统用户已经存在！"}))
        info["userid"] = username
        info["passwd"] = self.get_argument("passwd", None)
        info["role"] = self.get_argument("role", None)
        info["brief"] = self.get_argument("brief", None)
        info["email"] = self.get_argument("email", None)
        info["phone"] = self.get_argument("phone", None)

        for k, v in info.iteritems():
            if not v:
                return self.write(json.dumps({"status": "error", "msg": k + "为必选项，请输入信息！"}))
        last = self.db.tb_system_user.find_one({}, {"id": 1, "_id": 0}, sort=[("id", pymongo.DESCENDING)])
        info["id"] = int(last.get("id", 0)) + 1 if last else 1
        info["status"] = 1
        info["regtime"] = time.strftime("%Y-%m-%d %H:%M:%S")

        res = self.application.backend_auth.register(info)
        if res:
            print("register error", res)
            return self.write(json.dumps({"msg": u'注册系统用户失败', "status": "error"}))
        return self.write(json.dumps({"status": "success", "msg": u"系统用户增加成功！"}))


class AdminDeleteSysUser(BaseHandler):
    """删除系统用户"""
    @BaseHandler.admin_authed
    def post(self):
        datas = self.request.arguments
        del datas['_xsrf']
        for key, value in datas.items():
            self.db.tb_system_user.remove({"_id": ObjectId(value[0])})
        self.write(json.dumps({"status": 'ok', "msg": u'删除系统用户成功'}))


class AdminModifySysUser(BaseHandler):
    """修改系统用户"""
    @BaseHandler.admin_authed
    def get(self, id):
        record = self.db.tb_system_user.find_one({"_id": ObjectId(id)})
        return self.render("backend/system_user_modify.html", myuser=self.admin, admin_nav=22, sysuser=record)

    @BaseHandler.admin_authed
    def post(self, id):
        record = self.db.tb_system_user.find_one({"_id": ObjectId(id)})
        if not record:
            return self.write(json.dumps({"status": 'error', "msg": "修改的系统用户不存在！"}))
        newprofile = {
            'userid': self.get_argument("userid", None),
            'brief': self.get_argument("brief", None),
            'phone': self.get_argument("phone", None),
            'email': self.get_argument("email", None),
            'role': self.get_argument("role", None),
            'status': int(self.get_argument("status", None)),
            'regtime': self.get_argument("regtime", None),
        }
        for k, v in newprofile.iteritems():
            if not v:
                return self.write(json.dumps({"status": 'error', "msg": k + "为必选项，请输入信息！"}))
        m = self.db.tb_system_user.update_one({"_id": record.get('_id')}, {"$set": newprofile})
        return self.write(json.dumps({"status": 'ok', "msg": "修改系统用户成功！"}))


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
        flag = self.application.dbutil.updatePassWord(userid, pass3, ip_infp)
        if not flag:
            logger().info("修改用户密码失败：===>")
            self.write(json.dumps({"status": 'ok', "msg": u'修改密码失败'}))
        logger().info("修改用户密码成功：===>")
        self.write(json.dumps({"status": 'ok', "msg": u'修改密码成功'}))


class AdminPermissions(BaseHandler):
    """权限列表"""
    @BaseHandler.admin_authed
    def get(self):
        page = int(self.get_argument("page", 1))
        pagesize = int(self.get_argument("pagesize", "10"))

        skiprecord = pagesize * (page - 1)
        rightlist = self.application.dbutil.getPermissions(skiprecord, pagesize)

        count = self.application.dbutil.getAllPermissions()
        pages = count / pagesize
        if count % pagesize > 0:
            pages += 1

        self.render("backend/right_query.html", myuser=self.admin, admin_nav=22, right_list=rightlist, page=page,
                    pagesize=pagesize, pages=pages, count=count)


class AdminAddPermission(BaseHandler):
    """权限增加"""
    @BaseHandler.admin_authed
    def post(self):
        ip_info = self.request.remote_ip
        createdat = time.strftime("%Y-%m-%d %H:%M:%S")

        name = self.get_argument("name", None)
        title = self.get_argument("title", None)

        res = self.application.dbutil.addPermission(name, title, ip_info, createdat)
        if not res:
            return self.write(json.dumps({"msg": u'增加权限失败', "status": 'error'}))
        return self.write(json.dumps({"status": 'ok', "msg": u"增加权限成功！"}))


class AdminDeletePermission(BaseHandler):
    """删除权限"""
    @BaseHandler.admin_authed
    def post(self):
        datas = self.request.arguments
        del datas['_xsrf']
        ip_info = self.request.remote_ip
        for key, value in datas.items():
            rid = int(value[0])
            flag = self.application.dbutil.delPermission(rid, ip_info)
        if flag:
            self.write(json.dumps({"status": 'ok', "msg": u'删除权限成功'}))
        self.write(json.dumps({"status": 'ok', "msg": u'删除权限失败'}))


class AdminContents(BaseHandler):
    """图片视频富文本列表"""
    @BaseHandler.admin_authed
    def get(self):
        page = int(self.get_argument("page", 1))
        pagesize = self.application.settings["record_of_one_page"]

        skiprecord = pagesize * (page - 1)
        contents = self.application.dbutil.getContents(skiprecord, pagesize)

        count = self.application.dbutil.getAllContents()
        pages = count / pagesize
        if count % pagesize > 0:
            pages += 1
        categories = []

        self.render("backend/study_content_query.html", myuser=self.admin, admin_nav=41, contents=contents, page=page,
                    pagesize=pagesize, pages=pages, count=count,categories=categories)


class AdminNoticeList(BaseHandler):
    """系统公告列表"""
    @BaseHandler.admin_authed
    def get(self):
        current_page = int(self.get_argument("page", 1))
        pagesize = int(self.get_argument("pagesize", "20"))

        skiprecord = pagesize * (current_page - 1)
        notice_list = self.application.dbutil.getNotices(skiprecord, pagesize)

        count = self.application.dbutil.getAllNotices()
        pages = count / pagesize
        if count % pagesize > 0:
            pages += 1
        self.render("backend/notice_list.html", myuser=self.admin, admin_nav=91, notices=notice_list, page=current_page, pagesize=pagesize, pages=pages)


class AdminAddNotice(BaseHandler):
    """发布公告"""
    @BaseHandler.admin_authed
    def post(self):
        info = dict()
        info['title'] = self.get_argument('title')
        info['content'] = self.get_argument('content')
        info['userid'] = self.admin['userid']
        info['status'] = 1
        info['openid'] = -1
        info['atime'] = time.strftime("%Y-%m-%d %H:%M:%S")
        last = self.db.tb_notice_profile.find_one({}, {"id": 1, "_id": 0}, sort=[("id", pymongo.DESCENDING)])
        info['id'] = int(last.get("id", 0)) + 1 if last else 1
        self.db.tb_notice_profile.insert(info)

        return self.write(json.dumps({"status": "ok", "msg": u'增加系统公告成功'}))


class AdminDeleteNotice(BaseHandler):
    """删除公告"""
    @BaseHandler.admin_authed
    def post(self):
        datas = self.request.arguments
        del datas['_xsrf']
        for key, value in datas.items():
            self.db.tb_notice_profile.remove({"_id": ObjectId(value[0])})
        self.write(json.dumps({"status": 'ok', "msg": u'删除成功'}))


class AdminModifyNotice(BaseHandler):
    """修改公告"""
    @BaseHandler.admin_authed
    def get(self, id):
        record = self.db.tb_notice_profile.find_one({"_id": ObjectId(id)})
        self.render("backend/notice_modify.html", myuser=self.admin, admin_nav=91, notice=record)

    @BaseHandler.admin_authed
    def post(self, noticeid):
        record = self.db.tb_notice_profile.find_one({"_id": ObjectId(noticeid)})
        if not record:
            return self.write(json.dumps({"status": 'error', "msg": "修改的公告不存在！"}))

        newprofile = {
            'title': self.get_argument("title", None),
            'content': self.get_argument("content", None),
            'userid': self.get_argument("userid", None),
            'atime': self.get_argument("atime", None),
        }
        for k, v in newprofile.iteritems():
            if not v:
                return self.write(json.dumps({"status": 'error', "msg": k + "为必选项，请输入信息！"}))

        newprofile['status'] = self.get_argument("status", 1)

        m = self.db.tb_notice_profile.update({"_id": record.get('_id')}, {"$set": newprofile})
        return self.write(json.dumps({"status": 'ok', "msg": "修改公告成功！"}))


