# -*- coding:utf-8 -*-
import time
import functools        # from functools import wraps


class Decorator:
    def __init__(self, *argc, **argkw):
        pass

    @classmethod
    def api_authentication(self, method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            print("haah")
        return wrapper

    @classmethod
    def timeit(self, func):   # 计时装饰器,输出程序运行时间
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)
            dt = time.time() - t0
            print(func.__name__, args, kwargs, dt)
            return result
        return wrapper


@Decorator.timeit
def f(m):
    for i in range(10000):
        s = 0
    time.sleep(1)
    for j in range(100):
        s = s + j
    return "test"


if __name__ == "__main__":
    result = f(3)
    print("===>", result)


# https://blog.csdn.net/tulan_xiaoxin/article/details/81112854
# https://blog.csdn.net/weixin_34416649/article/details/93116687
