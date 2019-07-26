# import xlwt
# import xlrd
import json
import pandas as pd

# from matching import mine
# from check import judge

def read_csv_file(path):
    df = pd.read_csv(path)
    return df

savepath = r"E:\fuxing_idea\chonggou_csv_7_22\7-23\answer1_answer_2_AI.csv"
path1 = r"E:\fuxing_idea\chonggou_csv_7_22\7-23\v3.6_0.95_fused_ry_result_0.65_chonggou1.csv"
# path2 = r"E:\fuxing_idea\chonggou_csv_7_22\7-23\answer2.csv"
# path = r"E:\fuxing_idea\chonggou_csv_7_22\7-23\study_series.csv"
answer1_df = read_csv_file(path1)

# stu_df = read_csv_file(path)
# print(answer_df.shape[1])
uid = list(answer1_df["序列编号"])

# uid3 = list(stu_df["seriesInstanceUID"])
bingzao  = list(answer1_df["病灶"])

yxgj = list(answer1_df["影像工具"])

yxjg = list(answer1_df["影像结果"])

#
# print(uid3)
# print(type(list(uid3)))
# print(len(uid3))


# uid = list(uid1) + list(uid2)
# bingzao = list(bingzao1) + list(bingzao2)
# yxgj = list(yxgj1) + list(yxgj2)
# yxjg = list(yxjg1) + list(yxjg2)
zdynr = []

uid3 = ["1.2.840.113619.2.327.3.50990949.252.1557875858.398.5",
        "1.2.840.113619.2.416.185672529007973468239270490648099079346",
        "1.2.840.113619.2.416.35548681728510935866904450868894084077",
        "1.3.12.2.1107.5.1.4.73436.30000019051500062573200014492",
        "1.3.12.2.1107.5.1.4.73436.30000019051500062573200080016"]
# print(len(uid1))
# print(len(uid2))
# print(len(uid))
# print(uid2)
# print(uid)
for i in range(len(yxgj)):
    zdynr.append(None)

list = []
for i in range(len(uid)):
    # print(i)
    if uid[i] not in uid3:
        # print(uid[i])
        # print(uid3)
        list.append(i)

uid4 = [uid[i] for i in range(len(uid)) if (i not in list)]
bingzao3 = [bingzao[i] for i in range(len(bingzao)) if (i not in list)]
yxgj3 = [yxgj[i] for i in range(len(yxgj)) if (i not in list)]
yxjg3 = [yxjg[i] for i in range(len(yxjg)) if (i not in list)]
zdynr3 = [zdynr[i] for i in range(len(zdynr)) if (i not in list)]
test_dict = {"序列编号": uid4,
             "病灶": bingzao3,
             "影像工具": yxgj3,
             "影像结果": yxjg3,
             "自定义内容": zdynr3,
             }

#
test_dict_df = pd.DataFrame(test_dict, columns=["序列编号", "病灶", "影像工具", "影像结果", "自定义内容"])
# test_dict_df = pd.DataFrame(test_dict,columns=["序列编号","病灶","影像工具","影像结果","自定义内容","结节位置（左肺）- 仅供分类",
#                                                "结节位置（右肺）- 仅供分类","肺内病灶类型 - 仅供分类",
#                                                "胸膜病灶类型 - 仅供分类","其它 - 仅供分类"])

test_dict_df.to_csv(savepath, quoting=1, index=False, header=True, encoding="utf_8_sig")























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

# cluster_excle(path_answer, savepath)
# df = pd.read_csv(path)
# serial_number = df["序列编号"]
# data = df["影像结果"]
# print(type(nd))
# print(data[0])
# print(type(data[0]))