# -*- coding:utf-8 -*-
import socket
res = socket.getaddrinfo("s9zdg9kvt.hbbaaa.cn", 'http')
print(res[0][4][0])