import random
import time, datetime
from threading import Thread
import Queue

t1 = datetime.datetime.now()
print t1
def work():
    while not q.empty():
        b = q.get()
        a = random.random()
        time.sleep(a)
if __name__ == "__main__":
    thread = []
    q = Queue.Queue()
    while True:
        print 33333
        for i in range(300):
            q.put(i)
        for i in range(6):
            t = Thread(target=work)
            t.start()
            thread.append(t)
        for i in thread:
            i.join()
        t2 = datetime.datetime.now()
        print t2

