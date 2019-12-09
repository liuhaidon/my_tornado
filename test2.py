# -*- coding:utf-8 -*-
# 导入tkinter模块
# import tkinter
import Tkinter
# 创建窗体
window = Tkinter.Tk()
# 修改title
window.title('2048')
# 获取屏幕宽度和高度
screen_width = window.winfo_screenwidth()
screen_height= window.winfo_screenheight()
print(screen_width)
print(screen_height)
# 计算游戏位置x和y坐标
x = (screen_width-400)/2
y = (screen_height-654)/2
# 设置显示格式
size = '%dx%d+%d+%d'%(400,654,x,y)
# 设置窗口位置
window.geometry(size)
#　获取画布对象
canvas = Tkinter.Canvas(window)
# 画布怎么放？(包装方式)
canvas.pack(expand=Tkinter.YES,fill=Tkinter.BOTH)
# 画一条线
canvas.create_line(30,30,80,30,fill='#FF0099',width=20)
# 画文字
canvas.create_text(300,300,text='PYTHON',fill='red',font='time 24 bold')
# 画图片
# 加载一个图片
bee_image = Tkinter.PhotoImage(file='bee.gif')
# 画图片
canvas.create_image(100,100,image=bee_image,anchor=Tkinter.NW,tag = 'BEE')
import time

while True:
    time.sleep(0.01)
    canvas.move('BEE',1,1)
    window.update()
# 显示
window.mainloop()
