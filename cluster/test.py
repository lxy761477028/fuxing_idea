# import requests
#
# URL = r'http://127.0.0.1:7000'
# data = {
#             "tenantCode": "CY",
#             "patientUid": "fdsaf",
#             "studyInstanceUID": "sdfasda",
#             "url": "ewqfewqf",
#             "diagStatus":0,
#             "abnormal":0
#         }
# response = requests.post(URL, json=data)
#
# print(response.text)


import sys
import pandas as pd
import numpy as np


def judge_twocube(x1,y1,z1,x2,y2,z2,d1,d2):
    '''iou of two 3d bboxes. bbox: [z,y,x,d]'''
    # s = PixelSpacing
    # xp = float(s[0])
    # yp = float(s[1])
    # zp = float(SliceThickness)
    bbox1=[z1,y1,x1,d1]
    bbox2=[z2,y2,x2,d2]
    # zmin, zmax, ymin, ymax, xmin, xmax
    bbox1 = [bbox1[0]-bbox1[3]/2, bbox1[0]+bbox1[3]/2,
             bbox1[1]-bbox1[3]/2, bbox1[1]+bbox1[3]/2,
             bbox1[2]-bbox1[3]/2, bbox1[2]+bbox1[3]/2]
    bbox2 = [bbox2[0]-bbox2[3]/2, bbox2[0]+bbox2[3]/2,
             bbox2[1]-bbox2[3]/2, bbox2[1]+bbox2[3]/2,
             bbox2[2]-bbox2[3]/2, bbox2[2]+bbox2[3]/2]
    # Intersection bbox and volume.
    int_zmin = np.maximum(bbox1[0], bbox2[0])
    int_zmax = np.minimum(bbox1[1], bbox2[1])
    int_ymin = np.maximum(bbox1[2], bbox2[2])
    int_ymax = np.minimum(bbox1[3], bbox2[3])
    int_xmin = np.maximum(bbox1[4], bbox2[4])
    int_xmax = np.minimum(bbox1[5], bbox2[5])
    int_z = np.maximum(int_zmax - int_zmin, 0.)
    int_y = np.maximum(int_ymax - int_ymin, 0.)
    int_x = np.maximum(int_xmax - int_xmin, 0.)
    int_vol = int_z * int_y * int_x
    vol1 = (bbox1[1] - bbox1[0]) * (bbox1[3] - bbox1[2]) * (bbox1[5] - bbox1[4])
    vol2 = (bbox2[1] - bbox2[0]) * (bbox2[3] - bbox2[2]) * (bbox2[5] - bbox2[4])
    iou = float(int_vol)/(vol1+vol2-int_vol)
    #iou = int_vol / vol1
    #iou2 = int_vol / vol2
    # return max(iou, iou2)
    if iou > 0:
        return True
    else:return False



def del_duplicates(dataframe):
    col = ['uid','x','y','z','d']
    predict = dataframe.reset_index(inplace=False)
    predict.rename(columns = {'index':'order'},inplace=True)
    lable = predict
    try:     predict.rename(columns={'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    try:     lable.rename(columns={'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    predict['all_01'] = 0
    predict['order2'] = 0
    print('\nChecking.....')
    for i in range(0,len(predict.uid)):
        fenmu=len(predict.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd = []
        cod_list = []
        tt = pd.DataFrame(lable[lable['uid'] == predict.uid[i]])
        index_tt = tt.index
        for j in index_tt:
            if judge_twocube(lable.x[j],lable.y[j],lable.z[j],predict.x[i],predict.y[i],predict.z[i],lable.d[j],predict.d[i]):
                normal_pd.append(1)
                cod_list.append(str(lable['order'][j]))
            else:
                normal_pd.append(0)
        if 1 in normal_pd:
            all_01 = normal_pd.count(1)
        else:
            all_01 = normal_pd.count(0)
        predict.loc[i,'all_01'] = all_01
        predict.loc[i,'order2'] = '-'.join(cod_list)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()
    predict = predict.drop_duplicates('order2')
    df = pd.DataFrame(predict,columns=col)
    return df


def rea_csv(path, savepath):
    df = pd.read_csv(path)
    df = del_duplicates(df)
    print(df)
    df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")


path = r"E:\fuxing_idea\bijiao\2018-6-21\jinbiaozhu.csv"
savepath = r"E:\fuxing_idea\bijiao\2018-6-21\jinbiaozhu_quchong.csv"

rea_csv(path, savepath)
