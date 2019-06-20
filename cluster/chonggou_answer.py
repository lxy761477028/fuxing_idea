import xlwt
import xlrd
import json
import pandas as pd

from matching import mine
from check import judge

def read_csv_file(path):
    df = pd.read_csv(path)
    return df


def cluster_excle(path,savepath):
    answer_df = read_csv_file(path)
    serial_number_answer = answer_df["序列编号"]
    ls1 = answer_df["影像结果编号"]
    ls2 = answer_df["序列编号"]
    ls3 = answer_df["开始时间"]
    ls4 = answer_df["提交时间"]
    ls5 = answer_df["病灶"]
    ls6 = answer_df["影像工具"]
    data = answer_df["影像结果"]
    ls7 = []
    ls8 = []
    ls9 = []
    ls10 = []
    ls11 = []
    for i in range(len(serial_number_answer)):
        ls_data = json.loads(data[i])
        ls7.append(ls_data["maxd"])
        ls8.append(ls_data["mind"])
        ls9.append(ls_data["x"])
        ls10.append(ls_data["y"])
        ls11.append(ls_data["z"])

    answer_df1 = pd.DataFrame(columns=('影像结果编号',"序列编号","开始时间","提交时间","病灶","影像工具","maxd","mind","x","y","z"))
    answer_df1["影像结果编号"] = ls1
    answer_df1["序列编号"] = ls2
    answer_df1["开始时间"] = ls3
    answer_df1["提交时间"] = ls4
    answer_df1["病灶"] = ls5
    answer_df1["影像工具"] = ls6
    answer_df1["maxd"] = ls7
    answer_df1["mind"] = ls8
    answer_df1["x"] = ls9
    answer_df1["y"] = ls10
    answer_df1["z"] = ls11
    answer_df1.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")







    # df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")








#读取文件
path_answer = r"E:\fuxing_idea\cluster\2018_6_14\answer.csv"
path = r"E:\fuxing_idea\cluster\2018_6_14\noduleCls1.csv"
savepath = r"E:\fuxing_idea\cluster\2018_6_14\jinbiaozhu.csv"

cluster_excle(path_answer, savepath)
# df = pd.read_csv(path)
# serial_number = df["序列编号"]
# data = df["影像结果"]
# print(type(nd))
# print(data[0])
# print(type(data[0]))