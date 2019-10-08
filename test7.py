# -*- coding:utf-8 -*-
import re
# s = '''first line
#        second line
#        third line'''
# result = re.match('\w+', s) #返回l
# print result
# re.search(r'y','liuyan1').group() #返回y

def introduction(name,age,hobby="runing"):
    intro ="My name is %s,I'm %d years old,my hobby is %s."%(name,age,hobby)
    print(intro)

introduction("Amanda",23)
#而给默认参数传值时，则覆盖
introduction("Amanda",age=23,hobby="eating")

def main(name, score=60, *args, **kwargs):
    print name, score, args, kwargs
    return "success!!!"
main("张三", sex="男")          # 不给默认参数传值时，默认使用默认参数值
main("张三", 80, sex="男")      # 而给默认参数传值时，则覆盖
main("张三", 80, 90, sex="男")
