import pandas as pd
import numpy as np
import json
import requests
import os


# g_sdk_path = os.path.abspath(os.path.dirname(os.getcwd()))  # 当前目录的上层路径
# sys.path.append(g_sdk_path)

g_dr_api_url = 'http://dataapi.proxima-ai.com/'
g_annotation_api_url = 'http://annoapi.proxima-ai.com/'
g_account = '15088886661'
g_password = '123456789'


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


def get_token(g_dr_api_url, g_account, g_password):
    root = "v1/user/login"
    data = {
        "phoneNumber": g_account,
        "password": g_password
    }
    response = requests.post(g_dr_api_url + root, json=data)
    response_test = json.loads(response.text)
    token = response_test["result"][0]["token"]


path = r"E:\fuxing_idea\python_sdk\file\tct_0719_v2.csv"
def get_data(path):
    df = pd.read_csv(path)

    seriesinstanceUID_list = df["seriesinstanceUID"]
    studyinstanceUID_list = df["studyinstanceUID"]
    equipment_list = df["equipment"]
    bodypart_list = df["bodypart"]
    finding_list = df["finding"]
    conclusion_list = df["conclusion"]
    attribute_list = df["attribute"]
    custominfo_list = df["custominfo"]
    attachment_list = df["attachment"]
    taskpath_list = df["taskpath"]
    positive_list = df["positive"]
    userid_list = df["userid"]

    for i in range(len(seriesinstanceUID_list)):
        # print(seriesinstanceUID[i])
        data = {
            "seriesinstanceUID": seriesinstanceUID_list[i],
            "studyinstanceUID": studyinstanceUID_list[i],
            "equipment" : equipment_list[i],
            "bodypart" : bodypart_list[i],
            "finding" : finding_list[i],
            "conclusion" : conclusion_list[i],
            "attribute" : attribute_list[i],
            "custominfo" : custominfo_list[i],
            "attachment" : attachment_list[i],
            "taskpath" : taskpath_list[i],
            "positive" :positive_list[i],
            "userid" : userid_list[i]
        }
        data = json.dumps(data, cls=NpEncoder)
        # print(data)
        dic = json.loads(data)
        print(dic)

# GetToken()