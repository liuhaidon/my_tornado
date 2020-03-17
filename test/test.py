class Student:
    schoolage = 100
    schoolname = "信阳"  # 静态属性

    def __init__(self, value):
        ''' 初始化方法 '''
        self.value = value

    def ixmethod(self):
        ''' 实例方法，测试能否调用实例属性 '''
        print('ixmethod ->', self.value)

    def iymethod(self):
        ''' 实例方法，测试能否调用静态属性 '''
        print('iymethod ->', self.sfield)

    def cxmethod(cls):
        ''' 伪·类方法，测试能否调用实例属性 '''
        print('cxmethod ->', cls.value)

    @classmethod
    def cymethod(cls):
        ''' 真·类方法，测试能否调用静态属性 '''
        print('cymethod ->', cls.sfield)

    def sxmethod():
        ''' 伪·静态方法，尝试打印一条语句 '''
        print('apple')

    @staticmethod
    def symethod():
        ''' 真·静态方法，尝试打印一条语句 '''
        print('banana')

s = Student(1)

