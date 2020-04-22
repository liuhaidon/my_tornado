class PageHelper:
    """分页类"""
    def __init__(self, current_page='1', page_item=1):
        all_page, c = divmod(page_item, 5)
        if c > 0:
            all_page += 1
        try:
            current_page = int(current_page)
        except:
            current_page = 1
        if current_page < 1:
            current_page = 1

        self.current_page = current_page  # 当前页
        self.all_page = all_page          # 总页数

    @property
    def start(self):
        """显示数据的起点索引"""
        return (self.current_page - 1) * 5

    @property
    def end(self):
        """显示数据的末尾索引"""
        return self.current_page * 5

    def page_num_show(self, baseurl):
        """
        写入{% raw str_page %}模板中的内容
        :param baseurl: 该段代码不仅可以在/index/中使用，也可以在/home/等等页码使用，
        :return: 返回一段字符串形式的html代码块，包括首页，页码数，上一页等等内容
        """
        # 计算9个页码的起始索引
        list_page = []
        if self.current_page <= 4:
            s = 0
            e = min(self.all_page, 9)
        elif self.current_page > self.all_page - 4:
            s = max(0, self.all_page - 9)
            e = self.all_page
        else:
            s = self.current_page - 5
            e = self.current_page + 4
        # 首页
        first_page = '<a href="%s1">首页</a>' % (baseurl)
        list_page.append(first_page)

        # 上一页current_page-1
        if self.current_page <= 1:
            prev_page = '<a href="javascript:void(0);">上一页</a>'
        else:
            prev_page = '<a href="%s%s">上一页</a>' % (baseurl, self.current_page - 1)
        list_page.append(prev_page)

        # 9个页码数
        for p in range(s, e):
            if p + 1 == self.current_page:
                temp = '<a href="%s%s" class="active">%s</a>' % (baseurl, p + 1, p + 1)
                list_page.append(temp)
            else:
                temp = '<a href="%s%s">%s</a>' % (baseurl, p + 1, p + 1)
                list_page.append(temp)

        # 下一页next_page+1
        if self.current_page >= self.all_page:
            next_page = '<a href="javascript:void(0);">下一页</a>'
        else:
            next_page = '<a href="%s%s">下一页</a>' % (baseurl, self.current_page + 1)
        list_page.append(next_page)

        # 尾页
        last_page = '<a href="%s%s">尾页</a>' % (baseurl, self.all_page)
        list_page.append(last_page)

        # 页面跳转
        jump = """<input type="text"/><a οnclick="Jump('%s',this);">go</a>""" % (baseurl,)
        script = """<script>
            function Jump(url,self){
                var v=self.previousElementSibling.value;
                if (v.trim().length>0){
                    location.href=url+v;
                }
        }
        </script>"""
        list_page.append(jump)
        list_page.append(script)

        str_page = "".join(list_page)
        return str_page



# https://www.jianshu.com/p/b5c8afdfe82b
# https://blog.csdn.net/kukudehui/rss/list
# https://blog.csdn.net/iiiiher/article/details/77587368
# https://blog.csdn.net/lincoco49/article/details/90373140
