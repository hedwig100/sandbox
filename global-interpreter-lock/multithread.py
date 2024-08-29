import time
from threading import Thread

def countdown():
    n = 10000000
    while n > 0:
        n -= 1

if __name__ == '__main__':
    start = time.time()

    t1 = Thread(target=countdown)
    t2 = Thread(target=countdown)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    end = time.time()
    print(f"Time: {end - start}sec")