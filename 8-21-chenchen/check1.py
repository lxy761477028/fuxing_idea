import pandas as pd
import numpy as np
import csv
import sys,time
import os
from pydicom import dicomio

def judge(x1,y1,z1,x2,y2,z2,d1,d2,PixelSpacing,SliceThickness):
    s = PixelSpacing
    xp = float(s[0])
    yp = float(s[1])
    zp = float(SliceThickness)
    x3 = (x1-x2)*xp
    y3 = (y1-y2)*yp
    z3 = (z1-z2)*zp
    if x3*x3+y3*y3+z3*z3<d1*d1/4:
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

def divide(jin_path, ai_path, uid_list_file ='', check_file = False, intersection = True):
    pred = pd.read_csv(ai_path, engine = 'python')
    biaozhu= pd.read_csv(jin_path, engine = 'python')
    predict=pd.DataFrame(pred)
    lable = pd.DataFrame(biaozhu)
    # if convert_lable == True:
    #     lable = convert2xyz(lable)
    # if prob_min != 0:
    #     try:    predict = predict[predict.probability >= prob_min]
    #     except: True
    #     try:    predict = predict[predict.det_probability >= prob_min]
    #     except: True
    # if prob_max != 1:
    #     try:    predict = predict[predict.probability <= prob_max]
    #     except: True
    #     try:    predict = predict[predict.det_probability <= prob_max]
    #     except: True
    # if prob_cls_min != 0:
    #     try:    predict = predict[predict.cls_probability >= prob_cls_min]
    #     except: True
    # if prob_cls_max != 1:
    #     try:    predict = predict[predict.cls_probability <= prob_cls_max]
    #     except: True
    if uid_list_file != '':
        uid_list = pd.read_csv(uid_list_file, engine = 'python')
        predict = predict[predict['uid'].isin(uid_list['uid'].tolist())].reset_index(drop = True)
        lable = lable[lable['uid'].isin(uid_list['uid'].tolist())].reset_index(drop = True)
    if intersection == True:
        predict = predict[predict['uid'].isin(lable['uid'].tolist())].reset_index(drop = True)
        lable = lable[lable['uid'].isin(predict['uid'].tolist())].reset_index(drop = True)
    try: predict.rename(columns = {'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace = True)
    except: True
    try: lable.rename(columns = {'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace = True)
    except: True
    time.sleep(0.1)
    print('\nChecking label file.....')
    col_lable = lable.columns.tolist().append('all_01')
    lable_result = pd.DataFrame(columns=col_lable)
    for i in range(0,len(lable.uid)):
        fenmu=len(lable.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(predict[predict['uid'] == lable.uid[i]])
        index_tt = tt.index#建立索引，直接按索引中提取信息
        for j in index_tt:
            # file_path = predict.path[j]
            # all_path = os.listdir(file_path)
            # path = predict.path[j]+'/'+all_path[0]
            #path =  predict.path[j]+'/000001.dcm'
            # if judge_twocube(lable.x[i],lable.y[i],lable.z[i],predict.x[j],predict.y[j],predict.z[j],lable.d[i],predict.d[j],path):  normal_pd.append(1)
            if judge(lable.x[i],lable.y[i],lable.z[i],predict.x[j],predict.y[j],predict.z[j],lable.d[i],predict.d[j],predict.PixelSpacing[i].split("\\"), predict.SliceThickness[i]):  normal_pd.append(1)
            else: normal_pd.append(0)
        if 1 in normal_pd: all_01 = 1
        else:              all_01 = 0
        data = pd.Series({
            'uid':lable.uid[i],
            'x':lable.x[i],
            'y':lable.y[i],
            'z':lable.z[i],
            'd':lable.d[i],
            'all_01':all_01,
        })
        lable_result = lable_result.append(data, ignore_index = True)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()

    print('\nChecking predict file.....')
    col_pred = predict.columns.tolist().append('all_01')
    pred_result = pd.DataFrame(columns=col_pred)
    for i in range(0,len(predict.uid)):
        fenmu=len(predict.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(lable[lable['uid'] == predict.uid[i]])
        index_tt = tt.index
        for j in index_tt:
            # file_path = predict.path[i]
            # all_path = os.listdir(file_path)
            # path = predict.path[i]+'/'+all_path[0]
            #path =  predict.path[i]+'/000001.dcm'
            if judge(lable.x[j],lable.y[j],lable.z[j],predict.x[i],predict.y[i],predict.z[i],lable.d[j],predict.d[i], predict.PixelSpacing[i].split("\\"), predict.SliceThickness[i]):  normal_pd.append(1)
            else: normal_pd.append(0)
        if 1 in normal_pd: all_01 = 1
        else:              all_01 = 0
        data = pd.Series({
            'uid': predict.uid[i],
            'x': predict.x[i],
            'y': predict.y[i],
            'z': predict.z[i],
            'd': predict.d[i],
            'all_01': all_01,
        })
        if 'final_prob' in predict.columns:
            data = pd.Series({
                'uid':predict.uid[i],
                'x':predict.x[i],
                'y':predict.y[i],
                'z':predict.z[i],
                'd':predict.d[i],
                'probability': predict.final_prob[i],
                'all_01': all_01
            })
        elif 'cls_probability' in predict.columns:
            data = pd.Series({
                'uid':predict.uid[i],
                'x':predict.x[i],
                'y':predict.y[i],
                'z':predict.z[i],
                'd':predict.d[i],
                'det_probability':predict.det_probability[i],
                'cls_probability':predict.cls_probability[i],
                'all_01':all_01
            })
        pred_result = pred_result.append(data, ignore_index = True)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()
    print('\n')
    if check_file == True:
        pred_result.to_csv(ai_path.replace('.csv','_check_result.csv'))
        lable_result.to_csv(jin_path.replace('.csv','_check_result.csv'))
        # if  convert == True:
        #     convertForm(predict_filename.replace('.csv','_check_result.csv'),predict_filename.replace('.csv','_check_result.xlsx'))
        #     convertForm(bianzhu_filename.replace('.csv','_check_result.csv'),bianzhu_filename.replace('.csv','_check_result.xlsx'))
        #     try:
        #         os.remove(bianzhu_filename.replace('.csv','_check_result.csv'))
        #         os.remove(predict_filename.replace('.csv','_check_result.csv'))
        #     except:True
    # TP_lable = lable_result.all_01.tolist().count(1)
    # FN = lable_result.all_01.tolist().count(0)
    # TP_pred = pred_result.all_01.tolist().count(1)
    # FP = pred_result.all_01.tolist().count(0)
    # print('\n以标注文件中预测正确的数量作为TP：')
    # recall_label = float(TP_lable) / (TP_lable + FN)
    # precision_label = float(TP_lable) / (TP_lable + FP)
    # print('\nTP  :',TP_lable,'\nFP  :',FP,'\nFN  :',FN)
    # print('recall   :', str(round(recall_label*100,2))+'%')
    # print('precision:', str(round(precision_label*100,2))+'%')
    # print('\n以预测文件中预测正确的数量作为TP：')
    # recall_pred = float(TP_pred)/(TP_pred+FN)
    # precision_pred = float(TP_pred)/(TP_pred+FP)
    # print('\nTP  :',TP_pred,'\nFP  :',FP,'\nFN  :',FN)
    # print('recall   :', str(round(recall_pred*100,2))+'%')
    # print('precision:', str(round(precision_pred*100,2))+'%')

    # if convert == True:
    #     print('\n正在生成 TP_pred, TP_lable, FP, FN 文件.....')
    #     TP_pred_file = pred_result[pred_result['all_01'] == 1]
    #     FP_file = pred_result[pred_result['all_01'] == 0]
    #     TP_lable_file = lable_result[lable_result['all_01'] == 1]
    #     FN_file = lable_result[lable_result['all_01'] == 0]
    #     TP_pred_file.to_csv(mark + 'TP_pred.csv',encoding='utf-8-sig')
    #     FP_file.to_csv(mark + 'FP.csv',encoding='utf-8-sig')
    #     TP_lable_file.to_csv(mark + 'TP_lable.csv',encoding='utf-8-sig')
    #     FN_file.to_csv(mark + 'FN.csv',encoding='utf-8-sig')
    #     convertForm(mark + 'TP_pred.csv',mark + 'TP_pred.xlsx')
    #     convertForm(mark + 'FP.csv',mark + 'FP.xlsx')
    #     convertForm(mark + 'TP_lable.csv',mark + 'TP_lable.xlsx')
    #     convertForm(mark + 'FN.csv',mark + 'FN.xlsx')


    #     if cache == False:
    #         print('\n正在移除中间文件......')
    #         try:
    #             os.remove(mark + 'TP_pred.csv')
    #             os.remove(mark + 'FP.csv')
    #             os.remove(mark + 'TP_lable.csv')
    #             os.remove(mark + 'FN.csv')
    #             print('\n中间文件移除成功......')
    #         except:print('\n中间文件移除失败......')
    # print('\n   Mission Complete ！')
    # return [recall_label,precision_label]

ai_path = r"E:\fuxing_idea\chonggou_csv_7_22\7_25\file\yxbzhjg_chg.csv"
jin_path = r"E:\fuxing_idea\chonggou_csv_7_22\7_25\file\syshbzh_chg.csv"


divide(jin_path, ai_path, check_file=True)