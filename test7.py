# -*- coding:utf-8 -*-
import re
# s = '''first line
#        second line
#        third line'''
# result = re.match('\w+', s) #返回l
# print result
# re.search(r'y','liuyan1').group() #返回y


def main(name, *args):
    print name, args, type(args)
    return "success!!!"
main("张三", "男", "playgame")
main("张三", {"sex": "男"}, "dancing")
main("张三", ["hello", "world"], "dancing")
main("张三", *["hello", "world"])
main("张三", *"hello")

**kwargs表示创建一个名为 kwargs 的空字典，该字典可接受任意多个外界传入的关键字实参。
kwargs 字典将多于的实参，以关键字参数的形式传入，以字典的形式接收。