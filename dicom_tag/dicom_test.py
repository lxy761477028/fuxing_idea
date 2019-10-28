# import pydicom
# import os
import time
import datetime
#
# path = r""
# file = os.listdir(path)[0]
# file_path = os.path.join(path, file)
#
# dcm = pydicom.read_file(file_path)
# kvp = dcm.KVP
x = "20181129"




def time_add(x):
    year = int(x[0:4])
    month = int(x[4:6])
    day = int(x[6:8])
    if month ==10:
        new_year = year + 1
        new_month = 1
        new_day = day
    elif month == 11:
        new_year = year + 1
        if day >=28:
            new_month = 3
            new_day = day - 27
        else:
            new_month = 2
            new_day = day
    elif month == 12:
        new_year = year + 1
        new_month = 3
        if day == 31:
            new_day = 30
        else:
            new_day = day
    else:
        new_year = year
        new_month = month + 3
        if day == 31:
            new_day = 30
        else:
            new_day = day
    s = "%04d"%new_year + "%02d"%new_month + "%02d"%new_day
    # new_time = str(new_year) + str(new_month) + str(new_day)
    print(s)

# time_add(x)

def t_add(x):
    year = int(x[0:4])
    month = int(x[4:6])
    day = int(x[6:8])
    detester = "%04d"%year + "-" + "%02d"%month + "-" + "%02d"%day
    date = datetime.datetime.strptime(detester,"%Y-%m-%d")
    delta = datetime.timedelta(days=90)
    n_days = date+delta
    print(n_days)


list = "10998750201803190181"
t_add(x)
# x = 20180506
# a=x//10000
# b=(x-a*10000)//100
# c=x-a*10000-b*100
# # ll_30 = int(ll) - 30
# # print(ll_30)
# # gmt = time.gmtime()
# # time.struct_time(tm_year=a, tm_mon=b, tm_mday=c, tm_hour=6, tm_min=48, tm_sec=13, tm_wday=0, tm_yday=140, tm_isdst=0)
# gmt = str(a) + "-" + str(b) + "-" + str(c)
# print(a)
# print(b)
# print(c)
# print(gmt)