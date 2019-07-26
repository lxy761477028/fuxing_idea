# import xlwt
# import xlrd
import json
import pandas as pd

# from matching import mine
# from check import judge

def read_csv_file(path):
    df = pd.read_csv(path)
    return df

savepath = r"E:\fuxing_idea\chonggou_csv_7_22\file\v3.6_0.95_fused_ry_result_0.65_chonggou1.csv"
model_path = r"E:\fuxing_idea\chonggou_csv_7_22\file\moban.csv"
answer_path = r"E:\fuxing_idea\chonggou_csv_7_22\file\v3.6_0.95_fused_ry_result_0.65.csv"
model_df = read_csv_file(model_path)
answer_df = read_csv_file(answer_path)
print(answer_df.keys())
print(model_df["影像结果"])
# print(answer_df.shape[1])
uid = answer_df["uid"]
coordZ = answer_df["coordZ"]
coordY = answer_df["coordY"]
coordX = answer_df["coordX"]
diameter = answer_df["diameter"]
json_ls = []
bingzao = []
yxgj = []
zdynr = []
zuofei = []
youfei = []
fnbzlx = []
xmbzlx = []
qita = []
uid_ls = []
print(type(coordX[1]))
for i in range(len(answer_df)):
    data = {"y":float(coordY[i]),
            "x":float(coordX[i]),
            "z":float(coordZ[i]),
            "maxd":float(diameter[i])}
    uid_ls.append(uid[i])
    json_ls.append(data)
    bingzao.append("ANNO3")
    yxgj.append("ELLIPSE")
    zdynr.append(None)
    zuofei.append(None)
    youfei.append(None)
    fnbzlx.append(None)
    xmbzlx.append(None)
    qita.append(None)
"""
序列编号,
病灶,
影像工具,
影像结果,
自定义内容,
结节位置（左肺）- 仅供分类,
结节位置（右肺）- 仅供分类,\
肺内病灶类型 - 仅供分类,\
胸膜病灶类型 - 仅供分类,\
其它 - 仅供分类
"""
test_dict = {"序列编号": uid,
             "病灶": bingzao,
             "影像工具": yxgj,
             "影像结果": json_ls,
             "自定义内容": zdynr,
             # "结节位置（左肺）- 仅供分类": zuofei,
             #              # "结节位置（右肺）- 仅供分类": youfei,
             #              # "肺内病灶类型 - 仅供分类": fnbzlx,
             #              # "胸膜病灶类型 - 仅供分类": xmbzlx,
             #              # "其它 - 仅供分类": qita
             }

test_dict_df = pd.DataFrame(test_dict,columns=["序列编号","病灶","影像工具","影像结果","自定义内容"])
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