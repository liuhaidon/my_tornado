#!/usr/bin/env python
# coding:utf-8
import io
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class VerifyCode:
    __length = 4  # 验证码长度
    __draw = None  # 画布
    __img = None  # 图片资源
    __code = None  # 验证码字符
    __str = None  # 自定义验证码字符集
    __inCurve = True  # 是否画干扰线
    __inNoise = True  # 是否画干扰点
    __type = 2  # 验证码类型 1、纯字母  2、数字字母混合
    __fontPatn = './class/fonts/2.ttf'  # 字体
    __fontSize = 20  # 字体大小

    def __init__(self):
        bg_color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
        self.__width, self.__heigth = 120, 45      # 画布宽度与高度
        self.__img = Image.new('RGB', (self.__width, self.__heigth), bg_color)   # 创建图形
        self.__draw = ImageDraw.Draw(self.__img)   # 创建画布，创建画笔

    def GetCodeImage(self, size=80, length=4):
        '''获取验证码图片
           @param int size   验证码大小
           @param int length 验证码长度
        '''
        self.__length = length
        self.__fontSize = size
        self.__width = self.__fontSize * self.__length
        self.__heigth = int(self.__fontSize * 1.5)

        # 生成验证码图片
        self.create_code()        # 创建验证码字符
        self.create_points()      # 绘制干扰点
        self.__printString()
        self.__cerateFilter()
        return self.__img, self.__code

    def create_code(self):
        if not self.__str:   # 是否自定义字符集合
            numbers = ''.join(map(str, range(3, 10)))  # 数字："3456789"
            srcLetter = "qwertyuipasdfghjkzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            srcUpper = srcLetter.upper()
            if self.__type == 1:
                self.__str = numbers
            else:
                self.__str = srcLetter + srcUpper + numbers
        # 构造验证码
        self.__code = random.sample(self.__str, self.__length)

    def __cerateFilter(self):
        '''模糊处理'''
        self.__img = self.__img.filter(ImageFilter.BLUR)
        filter = ImageFilter.ModeFilter(8)
        self.__img = self.__img.filter(filter)

    def create_points(self):
        '''绘制干扰点'''
        if not self.__inNoise:
            return
        font = ImageFont.truetype(self.__fontPatn, int(self.__fontSize / 1.5))
        for i in range(5):
            # 杂点颜色
            noiseColor = (random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
            putStr = random.sample(self.__str, 2)
            for j in range(2):
                # 绘杂点
                size = (random.randint(-10, self.__width), random.randint(-10, self.__heigth))
                self.__draw.text(size, putStr[j], font=font, fill=noiseColor)
        pass

    def create_lines(self):
        '''绘制干扰线'''
        if not self.__inCurve:
            return
        x = y = 0;

        # 计算曲线系数
        a = random.uniform(1, self.__heigth / 2)
        b = random.uniform(-self.__width / 4, self.__heigth / 4)
        f = random.uniform(-self.__heigth / 4, self.__heigth / 4)
        t = random.uniform(self.__heigth, self.__width * 2)
        xend = random.randint(self.__width / 2, self.__width * 2)
        w = (2 * math.pi) / t

        # 画曲线
        color = (random.randint(30, 150), random.randint(30, 150), random.randint(30, 150))
        for x in range(xend):
            if w != 0:
                for k in range(int(self.__heigth / 10)):
                    y = a * math.sin(w * x + f) + b + self.__heigth / 2
                    i = int(self.__fontSize / 5)
                    while i > 0:
                        px = x + i
                        py = y + i + k
                        self.__draw.point((px, py), color)
                        i -= i

    def __printString(self):
        '''打印验证码字符串'''
        font = ImageFont.truetype(self.__fontPatn, self.__fontSize)
        x = 0;
        # 打印字符到画板
        for i in range(self.__length):
            # 设置字体随机颜色
            color = (random.randint(30, 150), random.randint(30, 150), random.randint(30, 150))
            # 计算座标
            x = random.uniform(self.__fontSize * i * 0.95, self.__fontSize * i * 1.1);
            y = self.__fontSize * random.uniform(0.3, 0.5);
            # 打印字符
            self.__draw.text((x, y), self.__code[i], font=font, fill=color)

_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))

def create_validate_code(size=(120, 30),
     chars=init_chars,
     img_type="GIF",
     mode="RGB",
     bg_color=(255, 255, 255),
     fg_color=(0, 0, 255),
     font_size=18,
     font_type="class/fonts/2.ttf",
     length=4,
     draw_lines=True,
     n_line=(1, 2),
     draw_points=True,
     point_chance=2):
    '''
    @todo: 生成验证码图片
    @param size: 图片的大小，格式（宽，高），默认为(120, 30)
    @param chars: 允许的字符集合，格式字符串
    @param img_type: 图片保存的格式，默认为GIF，可选的为GIF，JPEG，TIFF，PNG
    @param mode: 图片模式，默认为RGB
    @param bg_color: 背景颜色，默认为白色
    @param fg_color: 前景色，验证码字符颜色，默认为蓝色#0000FF
    @param font_size: 验证码字体大小
    @param font_type: 验证码字体，默认为 ae_AlArabiya.ttf
    @param length: 验证码字符个数
    @param draw_lines: 是否划干扰线
    @param n_lines: 干扰线的条数范围，格式元组，默认为(1, 2)，只有draw_lines为True时有效
    @param draw_points: 是否画干扰点
    @param point_chance: 干扰点出现的概率，大小范围[0, 100]
    @return: [0]: PIL Image实例
    @return: [1]: 验证码图片中的字符串
    '''

    width, height = size  # 宽， 高
    img = Image.new(mode, size, bg_color)  # 创建图形
    draw = ImageDraw.Draw(img)  # 创建画笔

    def get_chars():
        '''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    def create_lines():
        '''绘制干扰线'''
        line_num = random.randint(*n_line)  # 干扰线条数

        for i in range(line_num):
            # 起始点
            begin = (random.randint(0, size[0]), random.randint(0, size[1]))
            # 结束点
            end = (random.randint(0, size[0]), random.randint(0, size[1]))
            draw.line([begin, end], fill=(0, 0, 0))

    def create_points():
        '''绘制干扰点'''
        chance = min(100, max(0, int(point_chance)))  # 大小限制在[0, 100]

        for w in range(width):
            for h in range(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    def create_strs():
        '''绘制验证码字符'''
        c_chars = get_chars()
        strs = ' %s ' % ' '.join(c_chars)  # 每个字符前后以空格隔开

        font = ImageFont.truetype(font_type, font_size)
        font_width, font_height = font.getsize(strs)

        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=fg_color)

        return ''.join(c_chars)

    if draw_lines:
        create_lines()
    if draw_points:
        create_points()
    strs = create_strs()

    # 图形扭曲参数
    params = [1 - float(random.randint(1, 2)) / 100,
              0,
              0,
              0,
              - float(random.randint(1, 10)) / 100,
              float(random.randint(1, 2)) / 500,
              0.001,
              float(random.randint(1, 2)) / 500
              ]
    img = img.transform(size, Image.PERSPECTIVE, params)  # 创建扭曲

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强（阈值更大）

    return img, strs  # 返回验证码图片，和字符串类型验证码


if __name__ == "__main__":
    vie = VerifyCode()
    codeImage = vie.GetCodeImage(80, 4)
    # print(codeImage)

    out = io.BytesIO()
    codeImage[0].save(out, "png")
    print(out.getvalue())

# create_validate_code()
# https://www.cnblogs.com/adc8868/p/6902829.html
# https://www.cnblogs.com/adc8868/p/6897662.html?utm_source=itdadao&utm_medium=referral

# https://www.bbsmax.com/A/GBJrLbZBd0/
# https://www.cnblogs.com/shenwenlong/p/5710993.html
# https://www.cnblogs.com/zknublx/p/8021599.html
# https://blog.csdn.net/dandanfengyun/article/details/85644258
