import xlwt
import xlrd
import json
import pandas as pd

from matching import mine
from check import judge



def cluster_excle(path,savepath):
    df = pd.read_csv(path, encoding="gbk")
    df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")







    # df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")








#读取文件
path_answer = r"E:\fuxing_idea\cluster\2018_6_14\answer.csv"
path = r"E:\fuxing_idea\cluster\2018_6_14\noduleCls1.csv"
savepath = r"E:\fuxing_idea\cluster\2018_6_14\noduleCls1_chonggou.csv"

cluster_excle(path, savepath)
# df = pd.read_csv(path)
# serial_number = df["序列编号"]
# data = df["影像结果"]
# print(type(nd))
# print(data[0])
# print(type(data[0]))