from b import child2

def func1():
    print("This is func1 from child1.py in package a")

def call_func2():
    child2.func2()

def main():
    func1()
    call_func2()

if __name__ == "__main__":
    main()