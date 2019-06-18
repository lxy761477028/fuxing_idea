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
    data = df["影像结果"]
    data_answer = answer_df["影像结果"]
    data_answer = json.loads(data_answer[3])
    print(data_answer['x'])




path = r"E:\first\cluster\2019_6_12\data.csv"
path_answer = r"E:\first\cluster\2019_6_12\answer.csv"
savepath = r"E:\first\cluster\2019_6_12\data_answer.csv"

cluster_excle(path,path_answer,savepath)