from threading import Thread
from time import sleep
from app import run_app
from rabbit import mqListen


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper

@async
def A():
    mqListen()

def B():
    run_app()


A()
B()