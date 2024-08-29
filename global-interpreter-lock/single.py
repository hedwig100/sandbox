import time

def countdown():
    n = 10000000
    while n > 0:
        n -= 1

if __name__ == '__main__':
    start = time.time()

    countdown()
    countdown()

    end = time.time()
    print(f"Time: {end - start}sec")