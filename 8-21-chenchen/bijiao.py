import pandas as pd
import numpy as np
import csv
import sys,time
import os
from pydicom import dicomio
import json

def judge(x1,y1,z1,x2,y2,z2,d1,d2,PixelSpacing,SliceThickness):
    s = PixelSpacing
    xp = float(s[0])
    yp = float(s[1])
    zp = float(SliceThickness)
    x3 = (x1-x2)*xp
    y3 = (y1-y2)*yp
    z3 = (z1-z2)*zp
    if x3*x3+y3*y3+z3*z3<d1*d1/2:
        return True
    else:
        return False
# 工具函数
def judge_cube(x1,y1,z1,x2,y2,z2,d1,d2,PixelSpacing,SliceThickness):
    s = PixelSpacing
    xp = float(s[0])
    yp = float(s[1])
    zp = float(SliceThickness)
    if (abs(x1-x2)*xp<d1/2)&(abs(y1-y2)*yp<d1/2)&(abs(z1-z2)*zp<d1/2):
        return True
    else:
        return False
# def bboxes_iou(bbox1, bbox2):
def judge_twocube(x1,y1,z1,x2,y2,z2,d1,d2,PixelSpacing,SliceThickness):
    '''iou of two 3d bboxes. bbox: [z,y,x,d]'''
    s = PixelSpacing
    xp = float(s[0])
    yp = float(s[1])
    zp = float(SliceThickness)
    bbox1=[z1*zp,y1*yp,x1*xp,d1]
    bbox2=[z2*zp,y2*yp,x2*xp,d2]
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


test_path = r"E:\fuxing_idea\8-21-chenchen\8-21\nod_test.csv"
demo_path = r"E:\fuxing_idea\8-21-chenchen\8-21\nod_demo.csv"
save_test = r"E:\fuxing_idea\8-21-chenchen\8-21\nod_test_result_judge_cube.csv"
save_demo = r"E:\fuxing_idea\8-21-chenchen\8-21\nod_demo_result_judge_cube.csv"

def main(test_path,demo_path,save_demo, save_test):
    test_data = pd.read_csv(test_path, engine='python')
    demo_data = pd.read_csv(demo_path, engine='python')

    uid_test = test_data["series_instance_uid"]
    pixel_spacing_x = test_data["pixel_spacing_x"]
    pixel_spacing_y = test_data["pixel_spacing_y"]
    PixelSpacing = {}
    for i in range(len(pixel_spacing_x)):
        ll = [pixel_spacing_x[i],pixel_spacing_y[i]]
        PixelSpacing[uid_test[i]] = ll


    uid_demo = demo_data["序列编号"]
    data_demo = json.loads(demo_data["影像结果"][0])
    # print(data_demo["mind"])
    result_demo = []
    result_uid_demo = []
    num_demo = []
    for i in range(len(uid_demo)):
        num_demo.append(i)
        this_uid_resulr = 0
        this_uid_resulr_uid = "null"
        data_demo = json.loads(demo_data["影像结果"][i])
        for j in range(len(uid_test)):
            if uid_demo[i] == uid_test[j]:
                # print(data_demo)
                print(data_demo["x"], data_demo["y"], data_demo["z"], test_data["X"][j], test_data["Y"][j], test_data["coord_z"][j],
                      data_demo["maxd"], test_data["src_diameter"][j], PixelSpacing[uid_demo[i]], test_data["slice_thickness"][i])
                result = judge_cube(data_demo["x"], data_demo["y"], data_demo["z"], test_data["X"][j], test_data["Y"][j], test_data["coord_z"][j],
                      data_demo["maxd"], test_data["src_diameter"][j], PixelSpacing[uid_demo[i]], test_data["slice_thickness"][i])
                print(result)
                if result:
                    this_uid_resulr = 1
                    this_uid_resulr_uid = j
                    break
            else:
                pass
                # print(i)
        result_demo.append(this_uid_resulr)
        result_uid_demo.append(this_uid_resulr_uid)

    print(result_demo)
    print(result_uid_demo)
    demo_data["num"] = num_demo
    demo_data["result_demo"] = result_demo
    demo_data["result_uid_demo"] = result_uid_demo

    num_test = []
    result_test = []
    result_uid_test = []
    for n in range(len(uid_test)):
        num_test.append(n)
        if n in result_uid_demo:
            result_test.append(1)
            for f in range(len(result_uid_demo)):
                if n == result_uid_demo[f]:
                    result_uid_test.append(f)
        else:
            result_test.append(0)
            result_uid_test.append("null")
    test_data["num"] = num_test
    test_data["result_demo"] = result_test
    test_data["result_uid_demo"] = result_uid_test



    demo_data.to_csv(save_demo, quoting=1, index=False, header=True, encoding="utf_8_sig")
    test_data.to_csv(save_test, quoting=1, index=False, header=True, encoding="utf_8_sig")




    # print(test_data)
    # print(demo_data)
    # judge(x1, y1, z1, x2, y2, z2, d1, d2, PixelSpacing, SliceThickness)

if __name__ == '__main__':
    main(test_path, demo_path,save_demo, save_test)
    # ll = judge(182.03, 156.96, 181, 182.21, 156.67, 182, 3.88, 4.6, [0.662109375,0.662109375], 2)
    # print(ll)

# def judge(x1,y1,z1,x2,y2,z2,d1,d2,PixelSpacing,SliceThickness):
#     s = PixelSpacing
#     xp = float(s[0])
#     yp = float(s[1])
#     zp = float(SliceThickness)
#     x3 = (x1-x2)*xp
#     y3 = (y1-y2)*yp
#     z3 = (z1-z2)*zp
#     if x3*x3+y3*y3+z3*z3<d1*d1/4:
#         return True
#     else:
#         return False







