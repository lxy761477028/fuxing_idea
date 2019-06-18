# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 14:37:01 2018

@author: qx44
"""
import json
import math
import numpy as np


def load_ellipse(pt1, mat):
    index = 5
    a = mat[0] / 2 * index
    b = mat[1] / 2 * index
    area = 3.1415 * a * b
    x_min = (pt1[0] * index - a)
    x_max = (pt1[0] * index + a)
    y_min = (pt1[1] * index - b)
    y_max = (pt1[1] * index + b)
    if a > b:
        c = math.sqrt(a * a - b * b)
        #        focus1 = [pt1[0] - c, pt1[1]]
        #        focus2 = [pt1[0] + c, pt1[1]]
        mat1 = np.zeros((round(2 * a) + 1, round(2 * b) + 1))
        for i in range(round(x_min), round(x_min) + round(2 * a) + 1):
            for j in range(round(y_min), round(y_min) + round(2 * b) + 1):
                temp1 = math.sqrt(
                    (i - pt1[0] * index + c) * (i - pt1[0] * index + c) + (j - pt1[1] * index) * (j - pt1[1] * index))
                temp2 = math.sqrt(
                    (i - pt1[0] * index - c) * (i - pt1[0] * index - c) + (j - pt1[1] * index) * (j - pt1[1] * index))
                if temp1 + temp2 <= 2 * a:
                    mat1[i - round(x_min), j - round(y_min)] = 1
    elif b >= a:
        c = math.sqrt(b * b - a * a)
        #        focus1 = [pt1[0], pt1[1] - c]
        #        focus2 = [pt1[0], pt1[1] + c]
        mat1 = np.zeros((round(2 * a) + 1, round(2 * b) + 1))
        for i in range(round(x_min), round(x_min) + round(2 * a) + 1):
            for j in range(round(y_min), round(y_min) + round(2 * b) + 1):
                temp1 = math.sqrt(
                    (i - pt1[0] * index) * (i - pt1[0] * index) + (j - pt1[1] * index + c) * (j - pt1[1] * index + c))
                temp2 = math.sqrt(
                    (i - pt1[0] * index) * (i - pt1[0] * index) + (j - pt1[1] * index - c) * (j - pt1[1] * index - c))
                if temp1 + temp2 <= 2 * b:
                    mat1[i - round(x_min), j - round(y_min)] = 1
    mat_range = [x_min, x_max, y_min, y_max]
    min_length = min(2 * a, 2 * b)
    z = pt1[2] * index
    return area, mat_range, min_length, z, mat1


def load_rectangle(pt1, pt2):
    l1 = abs(pt1['x'] - pt2['x'])
    l2 = abs(pt1['y'] - pt2['y'])
    x_min = min(pt1['x'], pt2['x'])
    x_max = max(pt1['x'], pt2['x'])
    y_min = min(pt1['y'], pt2['y'])
    y_max = max(pt1['y'], pt2['y'])
    area = abs((pt1['x'] - pt2['x']) * (pt1['y'] - pt2['y']))
    mat_range = [x_min, x_max, y_min, y_max]
    min_length = min(l1, l2)
    z = pt1['z']
    return area, mat_range, min_length, z


def overlap(figure0, f1_info1, f1_info2, f2_info1, f2_info2):
    if figure0 == 'ELLIPSE':
        area1, mat_range1, min_length1, z1, mat1 = load_ellipse(f1_info1, f1_info2)
        area2, mat_range2, min_length2, z2, mat2 = load_ellipse(f2_info1, f2_info2)
    elif figure0 == 'RECTANGLE':
        area1, mat_range1, min_length1, z1 = load_rectangle(f1_info1, f1_info2)
        area2, mat_range2, min_length2, z2 = load_rectangle(f2_info1, f2_info2)
    iou = 0
    if not (z1 == z1):
        iou = 0
    elif mat_range1[0] > mat_range2[1] or mat_range1[1] < mat_range2[0] or mat_range1[2] > mat_range2[3] or mat_range1[
        3] < mat_range2[2]:
        iou = 0
    else:
        x_min0 = min(mat_range1[0], mat_range2[0])
        x_max0 = max(mat_range1[1], mat_range2[1])
        y_min0 = min(mat_range1[2], mat_range2[2])
        y_max0 = max(mat_range1[3], mat_range2[3])
        mat0 = np.zeros((round(x_max0) - round(x_min0), round(y_max0) - round(y_min0)))
        if figure0 == 'ELLIPSE':
            for i in range(round(x_min0), round(x_max0)):
                for j in range(round(y_min0), round(y_max0)):
                    if i >= round(mat_range1[0]) and round(i < mat_range1[1]) and j >= round(
                            mat_range1[2]) and j < round(mat_range1[3]):
                        if i >= round(mat_range2[0]) and round(i < mat_range2[1]) and j >= round(
                                mat_range2[2]) and j < round(mat_range2[3]):
                            mat0[i - round(x_min0), j - round(y_min0)] = mat1[i - round(mat_range1[0]), j - round(
                                mat_range1[2])] * mat2[i - round(mat_range2[0]), j - round(mat_range2[2])]
            add_on_x = min(abs(mat_range1[0] - mat_range2[1]), abs(mat_range1[1] - mat_range2[0]))
            add_on_y = min(abs(mat_range1[2] - mat_range2[3]), abs(mat_range1[3] - mat_range2[2]))
            overlap = sum(sum(mat0)) + (add_on_x + add_on_y) * 0.79
        #            print(overlap)
        else:
            overlap = min((mat_range1[1] - mat_range2[0]), (mat_range2[0] - mat_range1[1])) * min(
                (mat_range2[3] - mat_range1[2]), (mat_range2[2] - mat_range1[3]))
        iou = min(2 * overlap / (area1 + area2), 1)
    return iou


def load_figures(figure):
    figure0 = figure['imgType']
    threshold = figure['percent']
    img_list = figure['imgDataList']
    print(img_list)
    img_num = len(img_list)
    imgname_list = []
    img_info_list = []
    for i in range(img_num):

        tempstr = img_list[i]['imgData'].replace('True', '"t"').replace('False', '"f"')
        numpos = tempstr.index(',"direction')
        img_list[i]['imgData'] = json.loads(tempstr[0:numpos] + "}")
        img_list[i]['imgData']["direction"] = json.loads(
            tempstr[numpos + 1:len(tempstr)].replace('"direction":"', '').replace('"}', ''))
        imgname_list.append(img_list[i]['imgNo'])
        img_info_list.append(img_list[i]['imgData'])

    return figure0, threshold, img_num, imgname_list, img_info_list


def iou_total(figure0, img_num, imgname_list, img_info_list, threshold):
    similar = []
    drop_list = []
    for i in range(img_num):
        if i not in drop_list:
            temp = []
            temp.append(imgname_list[i])
            drop_list.append(i)
            for j in range(i, img_num):
                if j not in drop_list:
                    if figure0 == 'RECTANGLE':
                        f1_info1 = img_info_list[i]['point1']
                        f1_info2 = img_info_list[i]['point2']
                        f2_info1 = img_info_list[j]['point1']
                        f2_info2 = img_info_list[j]['point2']

                    elif figure0 == 'ELLIPSE' and img_info_list[i]['direction']['x'] >= img_info_list[i]['direction'][
                        'y']:
                        f1_info1 = [img_info_list[i]['x'], img_info_list[i]['y'], img_info_list[i]['z']]
                        f1_info2 = [img_info_list[i]['maxd'], img_info_list[i]['mind']]
                        f2_info1 = [img_info_list[j]['x'], img_info_list[j]['y'], img_info_list[j]['z']]
                        f2_info2 = [img_info_list[j]['maxd'], img_info_list[j]['mind']]
                    else:
                        f1_info1 = [img_info_list[i]['x'], img_info_list[i]['y'], img_info_list[i]['z']]
                        f1_info2 = [img_info_list[i]['mind'], img_info_list[i]['maxd']]
                        f2_info1 = [img_info_list[j]['x'], img_info_list[j]['y'], img_info_list[j]['z']]
                        f2_info2 = [img_info_list[j]['mind'], img_info_list[j]['maxd']]
                    ###得出figure相关的参数
                    iou = overlap(figure0, f1_info1, f1_info2, f2_info1, f2_info2)
                    if figure0 == 'ELLIPSE' and iou > threshold:
                        # print(iou)
                        temp.append(imgname_list[j])
                        drop_list.append(j)
                    elif figure0 == 'RECTANGLE' and iou > threshold:
                        temp.append(imgname_list[j])
                        drop_list.append(j)
            similar.append(temp)
    return similar


def mine(figure):
    figure0, threshold, img_num, imgname_list, img_info_list = load_figures(figure)

    try:
        similar = iou_total(figure0, img_num, imgname_list, img_info_list, threshold)
        return {"info":{"errormage": "success", "list": similar}, "detail": {}, "result": True, "code": 0}
    except Exception as e:
        print(e)
        return {"info": {"errormage": "success", "list": [[0]]}, "detail": {"errormsg": "error"}, "result": False,
                "code": 1}

