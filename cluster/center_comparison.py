import xlwt
import xlrd
import json
import pandas as pd

from matching import mine
from check import judge


def cluster_excle(path,path_answer,save_path,save_answer_path):
    df = pd.read_csv(path)
    answer_df = pd.read_csv(path_answer)
    serial_number = df["序列编号"]
    serial_number_answer = answer_df["序列编号"]
    data_results = []
    answer_results = []
    for j in range(len(serial_number_answer)):
        answer_results.append(0)
    for i in range(len(serial_number)):
        has_answer = 0
        answer_is_true = 0
        answer_two_true = 0
        for j in range(len(serial_number_answer)):
            if serial_number[i] == serial_number_answer[j]:
                answer_results[j] = 2
                has_answer = 1
                f = judge(df["x"][i],df["y"][i], df["z"][i], answer_df["x"][j],
                          answer_df["y"][j], answer_df["z"][j], df["maxd"][i], answer_df["maxd"][j])
                print(df["x"][i],df["y"][i], df["z"][i], answer_df["x"][j],
                          answer_df["y"][j], answer_df["z"][j], df["maxd"][i], answer_df["maxd"][j])
                print(f)
                print("*"*50)
                print(len(data_results))
                print(i)

                if f is True:
                    if answer_two_true != 1:
                        data_results.append(1)
                        answer_results[j] = 1
                        answer_two_true = 1
                    else:
                        answer_results[j] = 1
                    answer_is_true = 1
                    print(1)
                    continue
                else:
                    # results.append(0)
                    print(0)
                    continue

        if answer_is_true != 1 and has_answer ==1:
            data_results.append(0)
        if has_answer == 0:
            data_results.append("无")
            print("无")
    print("#"*50)
    print(len(data_results))
    print(len(serial_number_answer))
    print(data_results)

    df["诊断结果"] = data_results
    answer_df["诊断结果"] = answer_results
    df.to_csv(save_path, index=False, header=True,encoding="utf_8_sig")
    answer_df.to_csv(save_answer_path, index=False, header=True,encoding="utf_8_sig")







    # df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")








#读取文件
path = r"E:\fuxing_idea\cluster\2019_6_20\noduleCls1_chonggou.csv"
path_answer = r"E:\fuxing_idea\cluster\2019_6_20\jinbiaozhu.csv"
savepath = r"E:\fuxing_idea\cluster\2019_6_20\noduleCls1_answer_621.csv"
save_answer_path = r"E:\fuxing_idea\cluster\2019_6_20\jinbiaozhu_answer_621.csv"

cluster_excle(path, path_answer, savepath,save_answer_path)
# df = pd.read_csv(path)
# serial_number = df["序列编号"]
# data = df["影像结果"]
# print(type(nd))
# print(data[0])
# print(type(data[0]))