# encoding:utf-8
import requests, json, time, io
from BaseHandler import BaseHandler
from db.sqlite import Sqlite
from dingtalk import SecretClient
from view.__init__ import *

class AdminIndex(BaseHandler):
    def get(self):
        self.render('index.html')


# 获取用户userinfo
class AdminUser(BaseHandler):
    def get(self):
        code = self.get_argument("code", None)

        AppKey = "dings8usahjse288pz2n"
        AppSecret = "4j_E5eKZc3s7eVwCpoI1nQDF6kdAZnOzZUKQEqrriPLvnAV2NaMYQY7HLQS_20M9"
        url = "https://oapi.dingtalk.com/gettoken?appkey={0}&appsecret={1}".format(AppKey, AppSecret)
        resp = requests.get(url)
        resp = resp.json()
        access_token = resp["access_token"]

        url1 = "https://oapi.dingtalk.com/user/getuserinfo?access_token={0}&code={1}".format(access_token, code)
        resp1 = requests.get(url1)
        resp1 = resp1.json()

        url2 = "https://oapi.dingtalk.com/user/get?access_token={0}&userid={1}".format(access_token, resp1["userid"])
        resp2 = requests.get(url2)
        resp2 = resp2.json()
        return self.write(json.dumps({"status": "success", "userinfo": resp2}))


# 获取公司所有人
class AdminUsers(BaseHandler):
    def get(self):
        token = "03e71698604f327caa174bd548dae932"
        bumen_url = "https://oapi.dingtalk.com/department/list?access_token=%s" % (token)
        res_bumen = requests.get(bumen_url)
        str_bumen = res_bumen.text
        json_bumen = json.loads(str_bumen)
        res = json_bumen.get('department')
        bname_list = []
        bid_list = []
        for i in res:
            bumen_name = i.get('name')
            bname_list.append(bumen_name)
            bumen_id = i.get('id')
            bid_list.append(bumen_id)
        bumen_res = list(zip(bname_list, bid_list))
        bumen_data = dict(bumen_res)

        userlists = []
        for m in bid_list:  # 循环部门id
            member_url = "https://oapi.dingtalk.com/user/simplelist?access_token=%s&department_id=%s" % (token, m)
            res_member = requests.get(member_url)
            res_member = res_member.json()
            userlist = res_member["userlist"]
            userlists.extend(userlist)
            # with open('./member_id.txt', 'a') as f:
            # f.write(res_member.text)
        return self.write(json.dumps({"status": "success", "userlists": userlists}))


class AdminTasks(BaseHandler):
    def get(self):
        datas = self.request.arguments
        userid = self.get_argument("userid", None)
        sql = "SELECT * from tb_task where userid='%s'" % userid
        field = ["id", "userid", "content", "addtime", "endtime", "ctime", "type", "status", "name"]
        result = self.application.dbutil.select(sql)
        task_list = list_to_dict(field, result)
        return self.write(json.dumps({"status": "success", "data": task_list}))


class AdminAddTask(BaseHandler):
    def post(self):
        args = self.request.arguments
        ip = self.request.remote_ip
        headers = self.request.headers
        body = self.request.body_arguments
        userid = self.get_argument("userid", None)
        name = self.get_argument("name", None)
        content = self.get_argument("content", None)
        addtime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time()))
        endtime = ""
        ctime = ""
        tasktype = self.get_argument("type", None)
        status = "0"
        sql = "INSERT INTO tb_task(id,userid,name,content,addtime,endtime,ctime,type,status) VALUES(null,'%s','%s','%s','%s','%s','%s','%s','%s')" % (
        userid, name, content, addtime, endtime, ctime, tasktype, status)
        result = self.application.dbutil.insert(sql)
        return self.write(json.dumps({"status": "success", "add_result": result}))

    def check_xsrf_cookie(self):
        _xsrf = self.get_argument("_xsrf", None)

class AdminDeleteTask(BaseHandler):
    def post(self):
        taskid = self.get_argument("taskid", None)
        endtime = time.strftime("%Y/%m/%d %H:%M:%S")
        sql1 = "UPDATE tb_task set endtime='%s' where id='%s'" % (endtime, taskid)
        result = self.application.dbutil.update(sql1)
        sql2 = "INSERT INTO tb_backup select * from tb_task where id='%s'" % taskid
        result = self.application.dbutil.insert(sql2)
        sql3 = "DELETE from tb_task where id='%s'" % taskid
        result = self.application.dbutil.delete(sql3)
        if result == 1:
            return self.write(json.dumps({"status": "ok", "del_result": "删除任务成功"}))
        elif result == 0:
            return self.write(json.dumps({"status": "error", "del_result": "删除的任务id不存在"}))
        else:
            return self.write(json.dumps({"status": "error", "del_result": "删除任务失败"}))

    def check_xsrf_cookie(self):
        _xsrf = self.get_argument("_xsrf", None)


class AdminDetails(BaseHandler):
    def get(self):
        userid = self.get_argument("userid", None)
        tasktype = self.get_argument("type", "day_task")
        sql = "SELECT * from tb_task where userid='%s' and type='%s'" % (userid, tasktype)
        field = ["id", "userid", "content", "addtime", "endtime", "ctime", "type", "status", "name"]
        result = self.application.dbutil.select(sql)
        task_list = list_to_dict(field, result)
        # return self.write(json.dumps({"status": "success", "data": task_list}))
        self.render('details.html', task_list=task_list)


class AdminModifyTask(BaseHandler):
    def post(self):
        datas = self.request.arguments
        taskid = self.get_argument("tid", None)
        tasktype = self.get_argument("type", "todayTask")
        userid = self.get_argument("userid", None)
        endtime = time.strftime("%Y/%m/%d %H:%M:%S")
        endtime1 = datetime.datetime.strptime(endtime, '%Y/%m/%d %H:%M:%S')
        ctime = ""
        if taskid:
            sss = "SELECT addtime from tb_task where id='%s'" % taskid
            result = self.application.dbutil.select(sss)
            if result:
                addtime = datetime.datetime.strptime(result[0][0], '%Y/%m/%d %H:%M:%S')
                ctime = (endtime1 - addtime).total_seconds() / 60
                atime = str(int(round(ctime)))
                sql = "UPDATE tb_task set status='1',endtime='%s',ctime='%s' where id='%s'" % (endtime, atime, taskid)
                result = self.application.dbutil.update(sql)
                sql = "INSERT INTO tb_backup select * from tb_task where id='%s'" % taskid
                result = self.application.dbutil.insert(sql)
                sql = "DELETE from tb_task where id='%s'" % taskid
                result = self.application.dbutil.delete(sql)
        return self.write(json.dumps({"status": "success", "update": "修改任务完成"}))


class AdminModifyTask_back(BaseHandler):
    def post(self):
        datas = self.request.arguments
        tids = self.get_argument("tid", "")
        tasktype = self.get_argument("type", "todayTask")
        userid = self.get_argument("userid", None)
        tids = list(json.loads(tids))
        arry = []
        for tid in tids:
            arry.append(int(tid))
        # ssss = ','.join(['%s'] * len(tids))
        tup = tuple(arry)
        if len(tup) == 1:
            tup = "(" + str(tup[0]) + ")"
        endtime = ""
        ctime = ""
        # sql = "UPDATE tb_task set status='0',endtime="+endtime+",ctime="+ctime+" where userid="+userid+" and type="+tasktype+" and id not in ("+tup+")";
        sql = "UPDATE tb_task set status='0',endtime='%s',ctime='%s' where userid='%s' and type='%s' and id not in %s" % (
        endtime, ctime, userid, tasktype, tup)
        res = self.application.dbutil.update(sql)
        if tids:
            endtime = time.strftime("%Y/%m/%d %H:%M:%S")
            endtime1 = datetime.datetime.strptime(endtime, '%Y/%m/%d %H:%M:%S')
            for tid in tids:
                sss = "SELECT addtime,status from tb_task where id='%s'" % tid
                result = self.application.dbutil.select(sss)
                if result[0][1] == "0":
                    addtime = datetime.datetime.strptime(result[0][0], '%Y/%m/%d %H:%M:%S')
                    ctime = (endtime1 - addtime).total_seconds() / 3600
                    atime = str(int(round(ctime)))
                    sql = "UPDATE tb_task set status='1',endtime='%s',ctime='%s' where id='%s'" % (endtime, atime, tid)
                    result = self.application.dbutil.update(sql)
                # sql = "INSERT INTO tb_backup select * from tb_task where id='%s'" % tid
                # result = self.application.dbutil.insert(ssql)
        return self.write(json.dumps({"status": "success", "update": "修改任务完成"}))

    def check_xsrf_cookie(self):
        _xsrf = self.get_argument("_xsrf", None)


class AdminChangeTask(BaseHandler):
    def get(self):
        taskid = self.get_argument("taskid", None)
        tasktype = self.get_argument("type", None)
        sql = "UPDATE tb_task set type='%s' where id='%s'" % (tasktype, taskid)
        result = self.application.dbutil.update(sql)
        return self.write(json.dumps({"status": "success", "msg": "任务转换完成"}))


class AdminBackupTask(BaseHandler):
    def get(self):
        datas = self.request.arguments
        userid = self.get_argument("userid", "123")
        sql = "SELECT * from tb_backup where userid='%s' order by endtime desc" % userid
        field = ["id", "userid", "content", "addtime", "endtime", "ctime", "type", "status", "name"]
        result = self.application.dbutil.select(sql)
        back_list = list_to_dict(field, result)
        self.render('review.html', back_list=back_list)


class AdminAllTasks(BaseHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "https://www.bt.cn")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,content-type")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def get(self):
        datas = self.request.arguments
        sql = "select distinct name from tb_task"
        name_list = self.application.dbutil.select_name(sql)
        data_list = []
        for name in name_list:
            data_dict = dict()
            sql = "SELECT * from tb_task where name='%s'" % name
            field = ["id", "userid", "content", "addtime", "endtime", "ctime", "type", "status", "name"]
            result = self.application.dbutil.select(sql)
            task_list = list_to_dict(field, result)
            data_dict[name] = task_list
            data_list.append(data_dict)
        return self.write(json.dumps({"status": "success", "data": data_list}))

    def options(self):
        self.set_status(204)
        self.finish()


class AdminCreateTable(BaseHandler):
    def get(self):
        # sql = Sqlite()
        result = self.application.dbutil.create()
        if result:
            return self.write(json.dumps({"status": "ok", "msg": "创建表成功"}))
        else:
            return self.write(json.dumps({"status": "error", "msg": "创建表失败"}))
