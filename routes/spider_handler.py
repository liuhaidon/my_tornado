# -*- coding:utf-8 -*-
import urllib
import requests

# url = "http://username@password:www.baidu.com/s?name=liu&age=12"
# res = urllib.quote_plus(url)
# print res

# url = 'http://www.baidu.com/s'
# values = {"name": "liu", "age": 12, "love": "游戏"}
# params = urllib.urlencode(values)
# print params, type(params)      # age=12&name=liu <type 'str'>
# print url + '?' + params        # http://www.baidu.com/s?age=12&name=liu
# result = urllib.unquote(params)
# print result, type(result)


#print(requests.get("http://www.sina.com.cn").text)
headers={}
res = requests.get("http://www.sina.com.cn",headers=headers)
res.encoding="utf-8"
print(res.text)
