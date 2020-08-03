import threading
import time


x=True

def func1():
    global x
    while x:
       print("FUNC 1")
       time.sleep(0.1)
    

def func2():
    global x
    i=0
    while x:
        i+=1
        print("FUNC 2")
        time.sleep(0.5)
        if i==10:
            x=False


t1 = threading.Thread(target=func1,args=())
t2 = threading.Thread(target=func2,args=())
t1.start()
t2.start()