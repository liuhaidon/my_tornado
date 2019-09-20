import urllib2,re
import dns.resolver
import telnetlib,requests
# url = 'http://pv.sohu.com/cityjson?ie=utf-8'
# opener = urllib2.urlopen(url)
# m_str = opener.read()
# ipaddress = re.search('\d+.\d+.\d+.\d+', m_str).group(0)
# print ipaddress

# result = dns.resolver.query("liujiadon.top", 'A')
# for i in result.response.answer:
#     for j in i.items:
#         print j

# tn = telnetlib.Telnet("mx1.qq.com", 25, timeout=1)
# print tn
# if tn:
#     print "haha"
# else:
#     print "hehe"
domain = "http://www.baidu.com"
ua_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
res = requests.get(domain, headers=ua_header, timeout=8)
print res