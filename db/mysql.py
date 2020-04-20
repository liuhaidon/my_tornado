# encoding:utf-8
import pymysql
import time
import json
import traceback
from passlib.hash import pbkdf2_sha512
from db import mysql_statement


class DBUtil:
    def __init__(self, **kwargs):
        host = kwargs.get('host', '49.232.57.79')
        database = kwargs.get('database', 'study_tornado')
        user = kwargs.get('user', 'study_tornado')
        password = kwargs.get('password', '123456')
        port = kwargs.get('port', 3306)
        charset = kwargs.get('charset', 'utf8')
        connection = pymysql.connect(user=user, password=password, host=host, port=port, database=database, charset=charset)
        self.connection = connection
        if connection:
            self.cursor = connection.cursor()
        else:
            raise Exception('数据库连接参数有误！')

    def isloginsuccess(self, username, password):
        # sql = 'select count(*) from tb_user WHERE username=%s and password=%s'
        sql = "select * from tb_user WHERE username='%s'" % username
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        user = dict()
        if result:
            password_hash = result[2]
            rs = pbkdf2_sha512.verify(password, password_hash)
            if rs:
                user["userid"] = result[0]
                user["username"] = result[1]
                user["password"] = result[2]
                user["role"] = result[3]
                return user
            else:
                return False
        else:
            return False

    # 执行SQL语句返回受影响行（插入）
    def execute(self, sql):
        try:
            result = self.cursor.execute(sql)
            self.connection.commit()
            return result
        except Exception as ex:
            self.connection.rollback()
            traceback.print_exc()
            return ex

    # 执行SQL语句返回数据集
    def query(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            data = map(list, result)  # 将元组转换成列表
            # self.close()
            return data
        except Exception as ex:
            return ex

    # 查询某张表一共有多少条记录
    def query_all(self, sql):
        try:
            self.cursor.execute(sql)
            count = self.cursor.fetchone()
            return count[0]
        except Exception as ex:
            return ex

    # 关闭数据库连接
    def close(self):
        self.cursor.close()
        self.connection.close()

    def getUsers(self, m, n):
        # sql = 'select * from tb_user limit %s, %s' % (m, n)
        sql = 'select * from tb_user limit %s, %s'
        params = (m, n)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        user_list = []
        for b in result:
            info = {}
            info['userid'] = b[0]
            info['username'] = b[1]
            info['role'] = b[3]
            info['createdat'] = b[4]
            user_list.append(info)
        return user_list

    def getAllUsers(self):
        sql = "select count(*) from tb_user"
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def findUser(self, username):
        flag = True
        sql = "select count(*) from tb_user where username='%s'" % username
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        if count[0]:
            flag = False
        return flag

    def addUser(self, username, password, role, createdat):
        flag = True
        password = pbkdf2_sha512.encrypt(password)
        try:
            sql_str = "INSERT INTO tb_user(userid,username,password,role,createdat) VALUES (null, '%s', '%s', '%s', '%s')" % (
            username, password, role, createdat)
            self.cursor.execute(sql_str)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def delUser(self, uid, ip_info):
        atime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql_str1 = "select * from tb_user where userid=%s"
            params = (uid,)
            self.cursor.execute(sql_str1, params)
            result = self.cursor.fetchone()
            username = result[1]
            name = "删除用户：" + username
            sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, atime)
            self.cursor.execute(sql_str2)
            self.connection.commit()
        except:
            self.connection.rollback()

        sql = "DELETE FROM tb_user WHERE userid=%d" % uid
        flag = True
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def updatePassWord(self, userid, pass3, ip_info):
        atime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql_str1 = "select * from tb_user where userid=%s"
            params = (userid,)
            self.cursor.execute(sql_str1, params)
            result = self.cursor.fetchone()
            username = result[1]
            name = "修改密码：" + username
            sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, atime)
            self.cursor.execute(sql_str2)
            self.connection.commit()
        except:
            self.connection.rollback()

        sql = "update tb_user set password='%s' WHERE userid=%s" % (pass3, userid)
        flag = True
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    # 用户登陆时查询已经有的权限
    def getFindPermission(self, username):
        sql = "select * from tb_user_permission where username='%s'" % username
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        right_list = []
        for b in result:
            info = {}
            info['name'] = b[3]
            info['title'] = b[4]
            right_list.append(info)
        return right_list

    # 用户点击绑定时已经有的权限
    def getUserPermission(self, userid):
        sql = "select * from tb_user_permission where userid='%s'" % userid
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        right_list = []
        for b in result:
            info = {}
            info['name'] = b[3]
            info['title'] = b[4]
            right_list.append(info)
        return right_list

    # 所有权限
    def getAllPermission(self):
        sql = 'select * from tb_permission'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        rightlist = []
        for b in result:
            info = {}
            info['id'] = b[0]
            info['name'] = b[1]
            info['title'] = b[2]
            rightlist.append(info)
        return rightlist

    def getPermissions(self, m, n):
        # sql = 'select * from tb_permission limit %s,%s' % (m, n)
        sql = 'select * from tb_permission limit %s,%s'
        params = (m, n)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        rightlist = []
        for b in result:
            info = {}
            info['id'] = b[0]
            info['name'] = b[1]
            info['title'] = b[2]
            rightlist.append(info)
        return rightlist

    def getAllPermissions(self):
        sql = 'select count(*) from tb_permission'
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def updatePermission(self, userid, username, permission_list):
        try:
            sql_str1 = "delete from tb_user_permission where userid=%s"
            params = (userid,)
            self.cursor.execute(sql_str1, params)
            self.connection.commit()
        except:
            self.connection.rollback()

        flag = True
        for p in permission_list:
            p = json.loads(p)
            sql = "INSERT INTO tb_user_permission VALUES (null, '%s','%s','%s','%s')" % (
            userid, username, p["vid"], p["title"])
            try:
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                self.connection.rollback()
                flag = False
        return flag

    def addPermission(self, rname, title, ip_info, createdat):
        try:
            name = "增加权限：" + title
            sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, createdat)
            self.cursor.execute(sql_str2)
            self.connection.commit()
        except:
            self.connection.rollback()

        flag = True
        try:
            sql_str = "INSERT INTO tb_permission(id,name,title) VALUES (null, '%s', '%s')" % (rname, title)
            self.cursor.execute(sql_str)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def delPermission(self, rid, ip_info):
        atime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql_str1 = "select * from tb_permission where id=%s"
            params = (rid,)
            self.cursor.execute(sql_str1, params)
            result = self.cursor.fetchone()
            title = result[2]
            name = "删除权限：" + title
            sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, atime)
            self.cursor.execute(sql_str2)
            self.connection.commit()
        except:
            self.connection.rollback()

        sql = "DELETE FROM tb_permission WHERE id=%d" % (rid)
        flag = True
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def getContents(self,m,n):
        sql = 'select * from tb_media order by mid desc limit %s,%s'
        params = (m, n)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        domainlist = []
        for b in result:
            info = {}
            info['dmid'] = b[0]
            info['image'] = b[1]
            info['video'] = b[2]
            info['content'] = b[3]
            domainlist.append(info)
        return domainlist

    def getAllContents(self):
        sql = 'select count(*) from tb_media'
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def getDomains(self, m, n):
        # sql = 'select * from tb_domain where type is not null limit %s,%s' % (m, n)
        sql = 'select * from tb_domain where type is not null order by dmid desc limit %s,%s'
        params = (m, n)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        domainlist = []
        for b in result:
            info = {}
            info['dmid'] = b[0]
            info['domain'] = b[1]
            info['webname'] = b[2]
            info['ip_info'] = b[3]
            info['type'] = b[4]
            info['status'] = b[5]
            info['contect'] = b[6]
            info['createdat'] = b[7]
            info['updatedat'] = b[8]
            info['remark'] = b[9]
            domainlist.append(info)
        return domainlist

    def getAllDomains(self):
        sql = 'select count(*) from tb_domain where type is not null'
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def putDomain(self, domains):
        flag = True
        for domain in domains:
            try:
                sql_str1 = "select * from tb_domain where domain=%s"
                params = (domain,)
                self.cursor.execute(sql_str1, params)
                result = self.cursor.fetchone()
                if result:
                    flag = False
                    break
                sql_str2 = "INSERT INTO tb_domain(domain) VALUES ('%s')" % domain
                self.cursor.execute(sql_str2)
                self.connection.commit()
            except:
                self.connection.rollback()
                flag = False
        return flag

    def addDomain(self, dmid, domain, webname, ip_info, type, status, contect, createdat):
        flag = True
        try:
            sql_str = "INSERT INTO tb_domain VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % (
            dmid, domain, webname, ip_info, type, status, contect, createdat)
            self.cursor.execute(sql_str)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def delDoMain(self, dmid, ip_info):
        atime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql_str1 = "select * from tb_domain where dmid=%s"
            params = (dmid,)
            self.cursor.execute(sql_str1, params)
            result = self.cursor.fetchone()
            domain = result[1]
            name = "删除域名：" + domain
            sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, atime)
            self.cursor.execute(sql_str2)
            self.connection.commit()
        except:
            self.connection.rollback()

        sql = "DELETE FROM tb_domain WHERE dmid=%d" % dmid
        flag = True
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def selectDoMain(self, kind, content, m, n):
        content = str(content)
        sql = "select * from tb_domain WHERE %s='%s' order by dmid desc limit %s,%s" % (kind, content, m, n)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        domainlist = []
        for b in result:
            info = {}
            info['dmid'] = b[0]
            info['domain'] = b[1]
            info['webname'] = b[2]
            info['ip_info'] = b[3]
            info['type'] = b[4]
            info['status'] = b[5]
            info['contect'] = b[6]
            info['createdat'] = b[7]
            info['updatedat'] = b[8]
            info['remark'] = b[9]
            domainlist.append(info)
        return domainlist

    def selectAllDoMain(self, kind, content):
        sql = "select count(*) from tb_domain where %s='%s'" % (kind, content)
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def flagDomain(self, val, array):
        flag = True
        for dmid in array:
            dmid = filter(str.isdigit, dmid.encode("utf-8"))
            dmid = int(dmid)
            sql = "update tb_domain set status='%s' WHERE dmid=%d" % (val, dmid)
            try:
                self.cursor.execute(sql)
                self.connection.commit()
            except:
                self.connection.rollback()
                flag = False
        return flag

    def check_domain(self):
        sql = 'select * from tb_keyword'
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        for r in result:
            count = 0
            keyword = r[1]
            sql_n = 'select count(*) from tb_domain where contect="%s"' % keyword
            self.cursor.execute(sql_n)
            count = self.cursor.fetchone()
            sql_m = "update tb_keyword set domain_num='%s' WHERE keyword='%s'" % (count[0], keyword)
            try:
                self.cursor.execute(sql_m)
                self.connection.commit()
            except:
                self.connection.rollback()
                continue

    def updateComment(self, dmid, comment):
        dmid = dmid.encode("utf-8")
        dmid = int(dmid)
        sql = "update tb_domain set remark='%s' WHERE dmid=%s" % (comment, dmid)
        flag = True
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def getKeyWords(self, m, n):
        sql = 'select * from tb_keyword order by domain_num desc limit %s,%s' % (m, n)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        kwlist = []
        for b in result:
            info = {}
            info['kwid'] = b[0]
            info['keyword'] = b[1]
            info['type'] = b[2]
            info['region'] = b[3]
            info['domain_num'] = b[4]
            info['createdat'] = b[5]
            kwlist.append(info)
        return kwlist

    def getAllKeyWords(self):
        sql = 'select count(*) from tb_keyword'
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def addKeyWord(self, arry, type, region, createdat, ip_info):
        flag = True
        for keyword in arry:
            try:
                atime = time.strftime("%Y-%m-%d %H:%M:%S")
                name = "增加关键词：" + keyword
                sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, atime)
                self.cursor.execute(sql_str2)
                self.connection.commit()
            except:
                self.connection.rollback()

            try:
                # sql_str = "INSERT INTO tb_keyword VALUES ('%s', '%s', '%s', '%s',kwid)" % (keyword, type, region, createdat, 0)
                sql_str = "INSERT INTO tb_keyword(kwid,keyword,type,region,domain_num,createdat) VALUES (null, '%s', '%s', '%s', 0, '%s')" % (
                keyword, type, region, createdat)
                # print sql_str
                self.cursor.execute(sql_str)
                self.connection.commit()
            except:
                self.connection.rollback()
                flag = False
                return flag
                # logging.exception('Insert operation error')
        return flag

    def delKeyWord(self, kwid, ip_info):
        atime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql_str1 = "select * from tb_keyword where kwid=%s"
            params = (kwid,)
            self.cursor.execute(sql_str1, params)
            result = self.cursor.fetchone()
            keyword = result[1]
            name = "删除关键词：" + keyword
            sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, atime)
            self.cursor.execute(sql_str2)
            self.connection.commit()
        except:
            self.connection.rollback()

        sql = "DELETE FROM tb_keyword WHERE kwid=%d" % (kwid)
        flag = True
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def updateKeyWord(self, kwid):
        sql = "select * from tb_keyword WHERE kwid=%d" % kwid
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        keyword = ""
        if result:
            keyword = result[1]
        sql_l = "update tb_domain set type='正常',status='正常',contect='' WHERE contect='%s'" % keyword
        flag = True
        try:
            self.cursor.execute(sql_l)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def selectKeyWord(self, kind, content, m, n):
        content = str(content)
        sql = "select * from tb_keyword WHERE %s='%s' order by domain_num desc limit %s,%s" % (kind, content, m, n)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        kwlist = []
        for b in result:
            info = {}
            info['kwid'] = b[0]
            info['keyword'] = b[1]
            info['type'] = b[2]
            info['region'] = b[3]
            info['domain_num'] = b[4]
            info['createdat'] = b[5]
            kwlist.append(info)
        return kwlist

    def selectAllKeyWords(self, kind, content):
        sql = "select count(*) from tb_keyword where %s='%s'" % (kind, content)
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def getIpList(self, m, n):
        sql = 'select * from tb_ip_pool order by domain_num desc limit %s,%s' % (m, n)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        iplist = []
        for b in result:
            info = {}
            info['ipid'] = b[0]
            info['ip_address'] = b[1]
            info['num'] = b[2]
            iplist.append(info)
        return iplist

    def getAllIpList(self):
        sql = 'select count(*) from tb_ip_pool'
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def addIpAddress(self, ipid, address, num):
        flag = True
        try:
            sql_str = "INSERT INTO tb_ip_pool VALUES ('%s', '%s', '%s')" % (ipid, address, num)
            self.cursor.execute(sql_str)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def delIpAddress(self, ipid, ip_info):
        atime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql_str1 = "select * from tb_ip_pool where ipid=%s"
            params = (ipid,)
            self.cursor.execute(sql_str1, params)
            result = self.cursor.fetchone()
            ip_address = result[1]
            name = "删除IP：" + ip_address
            sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, atime)
            self.cursor.execute(sql_str2)
            self.connection.commit()
        except:
            self.connection.rollback()

        sql = "DELETE FROM tb_ip_pool WHERE ipid=%d" % (ipid)
        flag = True
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def selectIpAddress(self, kind, content, m, n):
        content = str(content)
        sql = "select * from tb_ip_pool WHERE %s='%s' order by domain_num desc limit %s,%s" % (kind, content, m, n)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        iplist = []
        for b in result:
            info = {}
            info['ipid'] = b[0]
            info['ip_address'] = b[1]
            info['num'] = b[2]
            iplist.append(info)
        return iplist

    def selectAllAddress(self, kind, content):
        sql = "select count(*) from tb_ip_pool where %s='%s'" % (kind, content)
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def task(self):
        array = []
        sql = "select * from tb_domain"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        dmlist = []
        for b in result:
            d = dict()
            d["dmid"] = b[0]
            d["domain"] = b[1]
            dmlist.append(d)

        sql = "select * from tb_keyword"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        kwlist = []
        for b in result:
            d = dict()
            d["kwid"] = b[0]
            d["keyword"] = b[1]
            d["type"] = b[2]
            d["region"] = b[3]
            kwlist.append(d)

        array.append(dmlist)
        array.append(kwlist)
        return array

    def check(self, domain):
        # for domain in array:
        sql = "update tb_domain set webname='%s',status='%s',type='%s',contect='%s',updatedat='%s' WHERE dmid=%d" % (
        domain["webname"], domain["status"], domain["type"], domain["contect"], domain["updatedat"], domain["dmid"])
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()

    def getAllKeyWord(self):
        sql = "select * from tb_keyword"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        kwlist = []
        for b in result:
            d = dict()
            d["kwid"] = b[0]
            d["keyword"] = b[1]
            d["type"] = b[2]
            d["region"] = b[3]
            kwlist.append(d)
        return kwlist

    def updateDomain(self, dmid, ip_info, webname, keyword="", re=False):
        dmid = int(dmid.encode("utf-8"))
        flag = True
        atime = time.strftime("%Y-%m-%d %H:%M:%S")
        try:
            sql_str1 = "select * from tb_domain where dmid=%s"
            params = (dmid,)
            self.cursor.execute(sql_str1, params)
            result = self.cursor.fetchone()
            domain = result[1]
            name = "更新域名：" + domain
            sql_str2 = "INSERT INTO tb_operate VALUES (null, '%s', '%s', '%s')" % (name, ip_info, atime)
            self.cursor.execute(sql_str2)
            self.connection.commit()
        except:
            self.connection.rollback()

        if not re:
            sql = "update tb_domain set webname='%s',status='待处理',type='非法网站',contect='%s',updatedat='%s' WHERE dmid=%d" % (
            webname, keyword, atime, dmid)
        else:
            sql = "update tb_domain set webname='%s',status='正常',type='正常',contect='%s',updatedat='%s' WHERE dmid=%d" % (
            webname, keyword, atime, dmid)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    def getIllegalWebsite(self, m, n):
        sql = 'select * from tb_domain where type="非法网站" and status="待处理" order by dmid desc limit %s,%s'
        params = (m, n)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        domainlist = []
        for b in result:
            info = {}
            info['dmid'] = b[0]
            info['domain'] = b[1]
            info['webname'] = b[2]
            info['ip_info'] = b[3]
            info['type'] = b[4]
            info['status'] = b[5]
            info['contect'] = b[6]
            info['createdat'] = b[7]
            info['updatedat'] = b[8]
            info['remark'] = b[9]
            domainlist.append(info)
        return domainlist

    def getAllIllegalWebsite(self):
        sql = 'select count(*) from tb_domain where type="非法网站" and status="待处理"'
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def getIpInfo(self, ipid):
        sql = 'select * from tb_ip_pool WHERE ipid=%s'
        params = (ipid,)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        return result[1]

    def getDetails(self, m, n, result):
        sql = "select * from tb_domain where ip_info=%s order by dmid desc limit %s,%s"
        params = (result, m, n)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        domainlist = []
        for b in result:
            info = {}
            info['dmid'] = b[0]
            info['domain'] = b[1]
            info['webname'] = b[2]
            info['ip_info'] = b[3]
            info['type'] = b[4]
            info['status'] = b[5]
            info['contect'] = b[6]
            info['createdat'] = b[7]
            info['updatedat'] = b[8]
            info['remark'] = b[9]
            domainlist.append(info)
        return domainlist

    def getAllDetails(self, result):
        sql = "select count(*) from tb_domain where ip_info='%s'" % result
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def getKeyDomain(self, arry):
        d = dict()
        for keyword in arry:
            sql = 'select count(*) from tb_domain where contect="%s"' % keyword
            self.cursor.execute(sql)
            count = self.cursor.fetchone()
            d[keyword] = count[0]
        return d

    def getKeywordDetails(self, m, n, result):
        sql = "select * from tb_domain where contect=%s order by dmid desc limit %s,%s"
        params = (result, m, n)
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        domainlist = []
        for b in result:
            info = {}
            info['dmid'] = b[0]
            info['domain'] = b[1]
            info['webname'] = b[2]
            info['ip_info'] = b[3]
            info['type'] = b[4]
            info['status'] = b[5]
            info['contect'] = b[6]
            info['createdat'] = b[7]
            info['updatedat'] = b[8]
            info['remark'] = b[9]
            domainlist.append(info)
        return domainlist

    def getAllKeywordDetails(self, result):
        sql = "select count(*) from tb_domain where contect='%s'" % result
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def getOperateRecord(self, m, n):
        sql = 'select * from tb_operate order by createdat desc limit %s,%s' % (m, n)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        loginlist = []
        for b in result:
            info = {}
            info['lid'] = b[0]
            info['content'] = b[1]
            info['ip_info'] = b[2]
            info['createdat'] = b[3]
            loginlist.append(info)
        return loginlist

    def getAllOperateRecord(self):
        sql = 'select count(*) from tb_operate'
        self.cursor.execute(sql)
        count = self.cursor.fetchone()
        return count[0]

    def delOperateRecord(self, rid):
        sql = "DELETE FROM tb_operate WHERE rid=%d" % (rid)
        flag = True
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except:
            self.connection.rollback()
            flag = False
        return flag

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    db = DBUtil()
    # sql = mysql_statement.update_field_name
    sql = "alter table tb_login_record change lid id int(11);"
    db.execute(sql)
