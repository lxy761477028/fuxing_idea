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
    data_answer_list = answer_df["影像结果"]
    ls1 = answer_df["影像结果编号"]
    ls2 = answer_df["序列编号"]
    ls3 = answer_df["开始时间"]
    ls4 = answer_df["提交时间"]
    ls5 = answer_df["病灶"]
    ls6 = answer_df["影像工具"]
    ls7 = answer_df["影像结果"]
    for i in range(len(serial_number_answer)):
        if ls1[i] != "重复":
            data_answer = json.loads(data_answer_list[i])
            for j in range(len(serial_number_answer)):
                if serial_number_answer[j] == serial_number_answer[i] and i != j:
                    data = json.loads(data_answer_list[j])
                    has_answer = 1
                    f = judge(data_answer["x"],data_answer["y"],data_answer["z"],data["x"],data["y"],data["z"],data_answer["maxd"],data["maxd"])
                    print(data_answer["x"],data_answer["y"],data_answer["z"],data["x"],data["y"],data["z"],data_answer["maxd"],data["maxd"])
                    print(f)

                    if f is True:
                        ls1 = ls1.copy()
                        ls1[j] = "重复"
        #                 results.append(1)
        #                 imgDataList.append(j + 2)
        #                 answer_is_true = 1
        #                 print(1)
        #                 break
        #             else:
        #                 # results.append(0)
        #                 print(0)
        #                 continue
    #
    #     if answer_is_true != 1 and has_answer ==1:
    #         results.append(0)
    #         imgDataList.append(0)
    #     if has_answer == 0:
    #         results.append("无")
    #         imgDataList.append("无")
    #         print("无")
    #
    # answer_df["诊断结果"] = results
    # answer_df["对应答案"] = imgDataList
    ls1 = ls1.copy()
    answer_df1 = pd.DataFrame(columns=('影像结果编号',"序列编号","开始时间","提交时间","病灶","影像工具","影像结果"))
    answer_df1["影像结果编号"] = ls1
    answer_df1["序列编号"] = ls2
    answer_df1["开始时间"] = ls3
    answer_df1["提交时间"] = ls4
    answer_df1["病灶"] = ls5
    answer_df1["影像工具"] = ls6
    answer_df1["影像结果"] = ls7
    answer_df1.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")







    # df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")








#读取文件
path_answer = r"E:\BaiduNetdiskDownload\cluster\2018_6_14\answer.csv"
path = r"E:\BaiduNetdiskDownload\cluster\2018_6_14\noduleCls1.csv"
savepath = r"E:\BaiduNetdiskDownload\cluster\2018_6_14\jinbiaozhun_quchong_620.csv"

cluster_excle(path_answer, savepath)
# df = pd.read_csv(path)
# serial_number = df["序列编号"]
# data = df["影像结果"]
# print(type(nd))
# print(data[0])
# print(type(data[0]))