import xlwt
import xlrd
import json
import pandas as pd

from matching import mine

z_scope = 2   #z轴浮动次数
z_size = 2  #z轴浮动大小
multiple = 1  #半径放大倍数
percent = 0.4  #匹配率


def read_csv_file(path):
    df = pd.read_csv(path)
    return df


def cluster_excle(path,path_answer,savepath):
    df = read_csv_file(path)
    answer_df = read_csv_file(path_answer)
    results = []
    serial_number = df["序列编号"]
    serial_number_answer = answer_df["序列编号"]
    data_list = df["影像结果"]
    data_answer_list = answer_df["影像结果"]
    for i in range(len(serial_number)):
        has_answer = 0
        answer_is_true = 0
        data = json.loads(data_list[i])
        # data_direction = json.loads(data["direction"])
        # print(type(data_direction))
        # print(data_direction)
        for j in range(len(serial_number_answer)):
            if serial_number[i] == serial_number_answer[j]:
                has_answer = 1
                imgDataList = []
                data_answer = json.loads(data_answer_list[j])
                data_direction = json.loads(data_answer["direction"])
                answer_img_num = j + 10002

                json_str = "{\"x\":%s,\"y\":%s,\"z\":%s,\"mind\":%s,\"maxd\":%s,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
                    float(data["x"]), float(data["y"]), float(data["z"]), float(data["mind"]),
                    float(data["maxd"]))

                answer_json_str = "{\"x\":%s,\"y\":%s,\"z\":%s,\"mind\":%s,\"maxd\":%s,\"direction\":\"{\"x\":%s,\"y\":%s,\"z\":%s}\"}" % (
                    float(data_answer["x"]), float(data_answer["y"]), float(data_answer["z"]),
                    float(data_answer["mind"]),
                    float(data_answer["maxd"]),float(data_direction["x"]),float(data_direction["y"]),float(data_direction["z"]))


                js_answer = {
                    "imgNo": answer_img_num,
                    "imgData": answer_json_str
                }
                js = {
                    "imgNo": i + 2,
                    "imgData": json_str
                }
                # data_answers = json.loads(data_answer[j])
                # print(data_answers["direction"])
                # print(answer_json_str)
                imgDataList.append(js)
                imgDataList.append(js_answer)

                for g in range(z_scope):
                    json_str_less = "{\"x\":%s,\"y\":%s,\"z\":%s,\"mind\":%s,\"maxd\":%s,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
                        float(data["x"]), float(data["y"]), float(data["z"] + (-g - 1) * z_size), float(data["mind"]),
                        float(data["maxd"]))
                    js_less = {
                        "imgNo": -g - 1,
                        "imgData": json_str_less
                    }
                    json_str_than = "{\"x\":%s,\"y\":%s,\"z\":%s,\"mind\":%s,\"maxd\":%s,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
                        float(data["x"]), float(data["y"]), float(data["z"] + (g + 1) * z_size), float(data["mind"]),
                        float(data["maxd"]))
                    js_than = {
                        "imgNo": g + 1,
                        "imgData": json_str_than
                    }
                    imgDataList.append(js_less)
                    imgDataList.append(js_than)

                roundness = {
                    "imgDataList": imgDataList,
                    "imgType": "ELLIPSE",
                    "percent": percent
                }
                # roundness = json.dumps(roundness)
                # print(roundness)
                f = mine(roundness)
                print(f)
                info = f['info']["list"][0]
                if answer_img_num in info:
                    results.append(1)
                    answer_is_true = 1
                    print(1)
                    break
                else:
                    # results.append(0)
                    print(0)
                    continue

        if answer_is_true != 1 and has_answer ==1:
            results.append(0)
        if has_answer == 0:
            results.append("无")
            print("无")
        # print("*"*100)
        # print(len(results))
    df["诊断结果"] = results
    # print(len(results))
    df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")







    # df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")








#读取文件
path_answer = r"E:\first\cluster\2019_6_12\data.csv"
path = r"E:\first\cluster\2019_6_12\answer.csv"
savepath = r"E:\first\cluster\2019_6_12\data_answer4.csv"

cluster_excle(path,path_answer,savepath)
# df = pd.read_csv(path)
# serial_number = df["序列编号"]
# data = df["影像结果"]
# print(type(nd))
# print(data[0])
# print(type(data[0]))