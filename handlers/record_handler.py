import json
from BaseHandler import BaseHandler


class AdminLoginRecord(BaseHandler):
    """用户登陆记录查询"""
    @BaseHandler.admin_authed
    def get(self):
        current_page = int(self.get_argument("page", 1))
        pagesize = self.application.settings["record_of_one_page"]

        skiprecord = pagesize * (current_page - 1)
        sql = "select * from tb_login_record order by logtime desc limit %s, %s" % (skiprecord, pagesize)
        login_list = self.application.dbutil.query(sql)

        field = ["id", "content", "ip_info", "logtime"]
        data_list = list_to_dict(field, login_list)

        sql = "select count(*) from tb_login_record"
        count = self.application.dbutil.query_all(sql)
        pages = count / pagesize
        if count % pagesize > 0:
            pages += 1
        self.render("backend/login_record.html", myuser=self.admin, admin_nav=11, login_list=data_list,
                    page=current_page, pagesize=pagesize, pages=pages, count=count)


class AdminLoginDelete(BaseHandler):
    """删除用户登陆记录"""
    @BaseHandler.admin_authed
    def post(self):
        datas = self.request.arguments
        del datas['_xsrf']
        for key, value in datas.items():
            lid = int(value[0])
            sql = "DELETE FROM tb_login_record WHERE id=%d" % lid
        result = self.application.dbutil.execute(sql)
        if result:
            self.write(json.dumps({"status": 'ok', "msg": u'删除登陆记录成功'}))
        self.write(json.dumps({"status": 'ok', "msg": u'删除登陆记录失败'}))


record_urls = [
    (r"/admin/login/record", AdminLoginRecord),  # 用户登陆记录查询
    (r"/admin/login/delete", AdminLoginDelete),  # 用户登陆记录删除
]


if __name__ == "__main__":
    pass
