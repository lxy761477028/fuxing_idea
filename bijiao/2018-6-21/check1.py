# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import sys,time
import os

def judge1(x1,y1,z1,x2,y2,z2,d1,d2):#判断点是否在球体中
    x3=(x1-x2)*0.68359375#像素转换成毫米
    y3=(y1-y2)*0.68359375
    if x3*x3+y3*y3+(z1-z2)*(z1-z2)<d1*d1:
        return True
    else:
        return False

def judge11(x1,y1,z1,x2,y2,z2,d1,d2):#判断点是否在球体中
    if (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2)<(d1/0.68359375)*(d1/0.68359375):#毫米转换成像素
        return True
    else:
        return False

def judge2(x1,y1,z1,x2,y2,z2,d1,d2):#判断点是否在正方体中
    d = d1/0.68359375#毫米转换成像素
    if (abs(x1-x2)<d/2)&(abs(y1-y2)<d/2)&(abs(z1-z2)<d/2):
        return True
    else:
        return False

def judge22(x1,y1,z1,x2,y2,z2,d1,d2):#判断点是否在正方体中
    if (abs(x1-x2)*0.68359375<d1/2)&(abs(y1-y2)*0.68359375<d1/2)&(abs(z1-z2)<d1/2):#像素转换成毫米
        return True
    else:
        return False
    
def judge3(x1,y1,z1,x2,y2,z2,d1,d2):#正方形是否相交
    '''iou of two 3d bboxes. bbox: [z,y,x,d]'''
    bbox1=[y1,x1,d1/0.68359375]
    bbox2=[y2,x2,d2/0.68359375]
    # zmin, zmax, ymin, ymax, xmin, xmax
    bbox1 = [bbox1[0]-bbox1[2]/2, bbox1[0]+bbox1[2]/2,
             bbox1[1]-bbox1[2]/2, bbox1[1]+bbox1[2]/2]
    bbox2 = [bbox2[0]-bbox2[2]/2, bbox2[0]+bbox2[2]/2,
             bbox2[1]-bbox2[2]/2, bbox2[1]+bbox2[2]/2]
    # Intersection bbox and volume.
    int_ymin = np.maximum(bbox1[0], bbox2[0])
    int_ymax = np.minimum(bbox1[1], bbox2[1])
    int_xmin = np.maximum(bbox1[2], bbox2[2])
    int_xmax = np.minimum(bbox1[3], bbox2[3])
    int_y = np.maximum(int_ymax - int_ymin, 0.)
    int_x = np.maximum(int_xmax - int_xmin, 0.)
    int_vol = int_y * int_x
    vol1 = (bbox1[1] - bbox1[0]) * (bbox1[3] - bbox1[2])
    vol2 = (bbox2[1] - bbox2[0]) * (bbox2[3] - bbox2[2])
    iou = int_vol / vol1
    iou2 = int_vol / vol2
    # return max(iou, iou2)
    if max(iou, iou2) > 0:
        return True
    else:
        return False