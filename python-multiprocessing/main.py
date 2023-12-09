from multiprocessing import Process
import time

dict = {}

def f(name):
    dict[1] = 0
    time.sleep(5)
    print('hello', name)
    print(dict)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    time.sleep(1)
    print(dict)
    p.join()
    print(dict)