# # import os
# import psutil
# # os.makedirs('E:\fuxing_idea\SCP')
#
#
# psutil.disk_usage('/')
# print(psutil.disk_io_counters())

# import urllib.request
# import requests
# # url = "http://127.0.0.1:5000/"
# # file = requests.post(url,json = data)
# #
# # print(file.text)

# import os
# os.system("python3 rabbit.py")
# os.system("python3 app.py")

# from celery import Celery
#
# app = Celery()
# app.config_from_object("celeryconfig")
#
# @app.task
# def taskA():
#     return 1
#
# @app.task
# def taskB():
#      return 2
#
# @app.task
# def add():
#     return 3
#
# taskA()
# taskB()
# add()

from threading import Thread
from time import sleep


# def async(f):
#     def wrapper(*args, **kwargs):
#         thr = Thread(target=f, args=args, kwargs=kwargs)
#         thr.start()
#
#     return wrapper
#
#
# @async
# def A():
#     sleep(10)
#     print("函数A睡了十秒钟。。。。。。")
#     print("a function")
#
#
# def B():
#     print("b function")
#
#
# A()
# B()

# dic = {"761745": "hjhjkk","87766":"90728975432897"}
#
# print(dic)
# del dic["7617"]
# print(dic)
import pandas as pd
path = r"E:\fuxing_idea\bijiao\2018-6-21\noduleCls1_chonggou.csv"
pred = pd.read_csv(path, engine= 'python')
# print(pred)
predict=pd.DataFrame(pred)

print(predict)