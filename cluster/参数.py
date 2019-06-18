# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 14:37:01 2018

@author: qx44
"""
import json
import math
import numpy as np
import pandas
import xlrd
import xlwt


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
    max_length = max(2 * a, 2 * b)
    z = pt1[2] * index
    return area, mat_range, min_length, max_length, z, mat1


def load_rectangle(pt1, pt2):
    index = 1
    l1 = abs(pt1['x'] * index - pt2['x'] * index)
    l2 = abs(pt1['y'] * index - pt2['y'] * index)
    x_min = min(pt1['x'] * index, pt2['x'] * index)
    x_max = max(pt1['x'] * index, pt2['x'] * index)
    y_min = min(pt1['y'] * index, pt2['y'] * index)
    y_max = max(pt1['y'] * index, pt2['y'] * index)
    area = abs((pt1['x'] * index - pt2['x'] * index) * (pt1['y'] * index - pt2['y'] * index))
    mat_range = [x_min, x_max, y_min, y_max]
    min_length = min(l1, l2)
    max_length = max(l1, l2)
    z = pt1['z'] * index
    return area, mat_range, min_length, max_length, z


def overlap(figure0, f1_info1, f1_info2, f2_info1, f2_info2):
    if figure0 == 'ELLIPSE':
        area1, mat_range1, min_length1, max_length1, z1, mat1 = load_ellipse(f1_info1, f1_info2)
        area2, mat_range2, min_length2, max_length2, z2, mat2 = load_ellipse(f2_info1, f2_info2)
    elif figure0 == 'RECTANGLE':
        area1, mat_range1, min_length1, max_length1, z1 = load_rectangle(f1_info1, f1_info2)
        area2, mat_range2, min_length2, max_length2, z2 = load_rectangle(f2_info1, f2_info2)
    iou = 0
    if not (z1 == z2) and (abs(z1 - z2) > max(max_length1, max_length2)):
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

    # try:
    similar = iou_total(figure0, img_num, imgname_list, img_info_list, threshold)
    return {"info":{"errormage": "success", "list": similar}, "detail": {}, "result": True, "code": 0}
    # except Exception as e:
    #     print(e)
    #     return {"info":{"errormage": "success", "list": [[0]]}, "detail": {"errormsg":"error"}, "result": False, "code": 1}



path1 = r"E:\first\stu_pandas\ccyy\1.xlsx"
path2 = r"E:\first\stu_pandas\ccyy\2.xlsx"
path3 = r"E:\first\stu_pandas\ccyy\3.xlsx"
path_answer = r"E:\first\stu_pandas\ccyy\answer.csv"
scope = 2

work_book = xlrd.open_workbook(path2)

answer_sheet = pandas.read_csv(path_answer)
work_sheet = work_book.sheets()[0]

nrows = work_sheet.nrows
ncols = work_sheet.ncols
answer_nrows = len(answer_sheet)
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet('Sheet0', cell_overwrite_ok=True)
for n in range(len(work_sheet.row_values(0))):
    sheet.write(0, n, work_sheet.row_values(0)[n])
for i in range(1, nrows):
    imgDataList = []
    has_answer = 0
    work_list = work_sheet.row_values(i)
    # json_str = "{\"x\":%2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (float(work_list[4]), float(work_list[5]), float(work_list[3]), float(work_list[6]), float(work_list[6]))

    for n in range(len(work_list)):
        sheet.write(i, n, work_list[n])

    for j in range(1, answer_nrows):

        answer_list = answer_sheet.loc[j]
        answer_id = answer_list[1]
        if answer_id == work_list[2]:
            has_answer = 1
            json_str = "{\"x\":%2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
                            float(work_list[4]), float(work_list[5]), float(work_list[3]), float(work_list[6])*1, float(work_list[6])*1)

            answer_json_str = "{\"x\":%.2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
                            float(answer_list[3]), float(answer_list[4]), float(answer_list[5]), float(answer_list[5])*1, float(answer_list[5])*1)
            answer_img_num = int(answer_list[0]) + 100000
            js_answer = {
                "imgNo": answer_img_num,
                "imgData": answer_json_str
            }
            js = {
                "imgNo": i + 1,
                "imgData": json_str
            }
            # print(answer_json_str)
            imgDataList.append(js)
            imgDataList.append(js_answer)
            for g in range(scope):
                json_str_less = "{\"x\":%2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
                    float(work_list[4]), float(work_list[5]), float(work_list[3]) + (-g-1) * 2, float(work_list[6])*1,
                    float(work_list[6])*1)
                js_less = {
                    "imgNo": g + 1,
                    "imgData": json_str_less
                }
                json_str_than = "{\"x\":%2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
                    float(work_list[4]), float(work_list[5]), float(work_list[3]) + (g+1) * 2, float(work_list[6])*1,
                    float(work_list[6])*1)
                js_than = {
                    "imgNo": g - 1,
                    "imgData": json_str_than
                }
                imgDataList.append(js_less)
                imgDataList.append(js_than)

            print(imgDataList)

            roundness = {
                "imgDataList": imgDataList,
                "imgType": "ELLIPSE",
                "percent": 0.2
            }
            f = mine(roundness)

            info = f['info']["list"][0]
            if answer_img_num in info:
                for n in range(len(work_list)):
                    sheet.write(i, n, work_list[n])
                sheet.write(i, len(work_list) - 1, 1)

                print(f)
                print(1)
                print("*"*50)
                book.save(r"E:\first\stu_pandas\ccyy\zuixin_answer.xls")
                imgDataList = []
                break
            else:
                sheet.write(i, len(work_list) - 1, 0)
                print(f)
                print(0)
                print("@" * 50)
                book.save(r"E:\first\stu_pandas\ccyy\zuixin_answer.xls")
                imgDataList = []
                continue
    if has_answer == 0:
        sheet.write(i, len(work_list) - 1, "无")
        print("无")
        print("#" * 50)

book.save(r"E:\first\stu_pandas\ccyy\zuixin_answer.xls")
