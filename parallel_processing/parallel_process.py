

import multiprocessing

def run_code1():
    print("hello")
def run_code2():
    print(123)
if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_code1)
    p2 = multiprocessing.Process(target=run_code2)
    print("1")

    p1.start()
    print("2")
    p2.start()
    print("3")


    p1.join()
    print("4")

    p2.join()
    print("5")