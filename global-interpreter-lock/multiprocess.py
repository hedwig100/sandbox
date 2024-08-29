import time
from multiprocessing import Process

def countdown():
    n = 10000000
    while n > 0:
        n -= 1

if __name__ == '__main__':
    start = time.time()

    t1 = Process(target=countdown)
    t2 = Process(target=countdown)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end = time.time()
    print(f"Time: {end - start}sec")