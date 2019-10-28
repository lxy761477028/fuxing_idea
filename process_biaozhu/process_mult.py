import multiprocessing
import time

def worker():
    print("work start:{0}".format(time.ctime()))
    time.sleep(10)
    print("work end:{0}".format(time.ctime()))


if __name__ == "__main__":
    p = multiprocessing.Process(target=worker)
    # p.daemon = True
    p.start()
    print("end!")