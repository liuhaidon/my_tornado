# -*- coding:utf-8 -*-
# import socket
# res = socket.getaddrinfo("s9zdg9kvt.hbbaaa.cn", 'http')
# print(res[0][4][0])

import time
import requests
import hashlib

PID = 'qwe'

current_time = time.time()
ramdom_str = "%s|%s" % (PID, current_time)
h = hashlib.md5()
h.update(bytes(ramdom_str, encoding='utf-8'))
UID = h.hexdigest()

q = "%s|%s|0" % (UID, current_time)
url = 'http://127.0.0.1:8066/api/auth?pid=%s' % q
print(url)
ret = requests.get(url)

print(ret.text)

# http://127.0.0.1:8066/api/auth?pid=c2539948caa7b7fe0d00fcd9d75b7574|1474341577.4938722|0
