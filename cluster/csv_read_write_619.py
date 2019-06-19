import xlwt
import xlrd
import json
import pandas as pd

from matching import mine
from check import judge


z_scope = 5   #z轴浮动次数
z_size = 2  #z轴浮动大小
multiple = 1  #半径放大倍数
percent = 0.4  #匹配率


def read_csv_file(path):
    df = pd.read_csv(path)
    return df


def cluster_excle(path,path_answer,savepath):
    df = pd.read_csv(path, encoding="gbk")
    answer_df = read_csv_file(path_answer)
    results = []
    imgDataList = []
    serial_number = df["xulie"]
    serial_number_answer = answer_df["序列编号"]
    data_answer_list = answer_df["影像结果"]
    for i in range(len(serial_number)):
        data_x = df["x"][i]
        data_y = df["y"][i]
        data_z = df["z"][i]
        data_maxd = df["maxd"][i]
        has_answer = 0
        answer_is_true = 0
        for j in range(len(serial_number_answer)):
            if serial_number[i] == serial_number_answer[j]:
                has_answer = 1
                data_answer = json.loads(data_answer_list[j])
                f = judge(data_x,data_y,data_z,data_answer["x"],data_answer["y"],data_answer["z"],data_maxd,data_answer["maxd"])
                print(data_x,data_y,data_z,data_answer["x"],data_answer["y"],data_answer["z"],data_maxd,data_answer["maxd"])
                print(f)

                if f is True:
                    results.append(1)
                    imgDataList.append(j + 2)
                    answer_is_true = 1
                    print(1)
                    break
                else:
                    # results.append(0)
                    print(0)
                    continue

        if answer_is_true != 1 and has_answer ==1:
            results.append(0)
            imgDataList.append(0)
        if has_answer == 0:
            results.append("无")
            imgDataList.append("无")
            print("无")

    df["诊断结果"] = results
    df["对应答案"] = imgDataList
    df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")







    # df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")








#读取文件
path_answer = r"E:\BaiduNetdiskDownload\cluster\2018_6_14\answer.csv"
path = r"E:\BaiduNetdiskDownload\cluster\2018_6_14\noduleCls1.csv"
savepath = r"E:\BaiduNetdiskDownload\cluster\2018_6_14\noduleCls1_answer_619_daan_1.csv"

cluster_excle(path, path_answer, savepath)
# df = pd.read_csv(path)
# serial_number = df["序列编号"]
# data = df["影像结果"]
# print(type(nd))
# print(data[0])
# print(type(data[0]))