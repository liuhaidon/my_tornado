# encoding:utf-8
import os, time, json, traceback
import uuid
from BaseHandler import BaseHandler
from views import *


class AjaxFindSysUser(BaseHandler):
    """查找用户名是否已经注册过"""
    @BaseHandler.admin_authed
    def post(self):
        username = self.get_argument("username", None)
        flag = self.application.dbutil.findUser(username)
        if not flag:
            self.write(json.dumps({"status": 'error', "msg": u'已经注册过'}))
        else:
            self.write(json.dumps({"status": 'ok', "msg": u'没有注册过'}))


class AjaxFindWebsite(BaseHandler):
    @BaseHandler.admin_authed
    def post(self):
        arry = self.get_arguments("arry[]")
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
        self.write(json.dumps({"userpermission": result1, "allpermission": result2}))


class AjaxPermissionBind(BaseHandler):
    @BaseHandler.admin_authed
    def post(self):
        userid = self.get_argument("userid")
        username = self.get_argument("username")
        permission_list = self.get_arguments('playlist[]')
        # permission_list = json.loads(permission_list)
        for p in permission_list:
            pass
        result = self.application.dbutil.updatePermission(userid, username, permission_list)
        if not result:
            return self.write(json.dumps({"status": "success", "error": u'修改权限失败!'}))
        return self.write(json.dumps({"status": "success", "error": u'修改权限成功!'}))


class UploadImageFile(BaseHandler):
    def post(self):
        datas = self.request.arguments
        path = self.get_argument("path")
        name = self.get_argument("name", "")
        upload_path = os.path.join(self.settings['upload_path'], path)
        print(path, name, upload_path)
        # 若不存在此目录，则创建之
        if not os.path.isdir(upload_path):
            # upload_path = upload_path.replace("/", "\\") #windows platform
            os.makedirs(upload_path)
        file_metas = self.request.files.get('file', [])
        filename = ''
        try:
            for meta in file_metas:
                filename = meta['filename']
                ext = os.path.splitext(filename)[1]
                # 生成随机文件名
                filename = str(uuid.uuid4())
                filename = '%s%s' % (filename, ext)
                filepath = os.path.join(upload_path, filename)
                with open(filepath, 'wb') as up:
                    up.write(meta['body'])
        except Exception as e:
            return self.write(json.dumps({"status": 'error', "msg": u"上传失败，请重新上传"}))
        else:
            print(json.dumps({"status": 'ok', "msg": "", "base_url": "", "name": filename}))
            return self.write(json.dumps({"status": 'ok', "msg": "", "base_url": "", "name": filename}))


class UploadVideoFile(BaseHandler):
    def post(self):
        path = self.get_argument("path")
        input_name = self.get_argument("iname", "")
        nums = self.get_argument("chunks", "")
        num = self.get_argument("chunk", "")
        # 视频文件名
        filename = self.get_argument("name", "")

        upload_path = os.path.join(self.settings['upload_path'], path)
        print(path, nums, num, filename, upload_path)

        # 视频保存路径+视频文件名
        filepath = os.path.join(upload_path, filename)
        # 若不存在此目录，则创建之
        if not os.path.isdir(upload_path):
            # upload_path = upload_path.replace("/", "\\") #windows platform
            os.makedirs(upload_path)
        file_metas = self.request.files.get('file', [])
        # filename = ''
        try:
            for meta in file_metas:
                # ext = os.path.splitext(filename)[1]
                # 生成随机文件名
                # filename = str(uuid.uuid4())
                # filename = '%s%s' % (filename, ext)
                # filepath = os.path.join(upload_path, filename)
                with open(filepath, 'ab') as up:
                    up.write(meta['body'])
        except Exception as e:
            traceback.print_exc()
            print('视频文件上传失败,失败原因[{0}]'.format(str(e)))
            return self.write(json.dumps({"status": 'error', "msg": u"视频文件上传失败，请重新上传"}))
        else:
            print(json.dumps({"status": 'ok', "msg": "", "base_url": "", "name": filename}))
            return self.write(json.dumps({"status": 'ok', "msg": "", "base_url": "", "name": filename}))