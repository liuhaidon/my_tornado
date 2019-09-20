# -*- coding:utf-8 -*-
import os,requests,re
# a = os.access("aaa.txt", os.X_OK)
ua_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
__codings = ['utf-8', 'gbk', 'gb2312', 'big5', 'utf8']
domain = "http://" + "yirenyese.com"
try:
    # 设置3秒爬取超时
    res = requests.get(domain, headers=ua_header, timeout=12)
    if not res.encoding in __codings:
        tmp = res.text.lower()
        for c in __codings:
            if re.search('<meta .* charset=.?' + c, tmp):
                res.encoding = c
                break
    if res.encoding=='ISO-8859-1':res.encoding = 'utf-8'
    content = res.text
except:
    print 666
# print "content==",content
# if not content:
#     print "打不开"
print content
titleRe1 = re.compile(r'<title>(.*)</title>')
titles = titleRe1.findall(content)




