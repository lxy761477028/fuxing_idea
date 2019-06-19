# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv
import sys,time
import os
# 工具函数
def judge_old(x1,y1,z1,x2,y2,z2,d1,d2):
    # 判断是否在范围d内，返回TRUE为预测到。返回FALSE说明两中心店距离大于d，即没预测到
    if (x1-x2)*(x1-x2)+(y1-y2)*(y1-y2)+(z1-z2)*(z1-z2)<(d1/0.7+d2)*(d1/0.7+d2):
        return True
    else:
        return False
# def bboxes_iou(bbox1, bbox2):
def judge(x1,y1,z1,x2,y2,z2,d1,d2):
    '''iou of two 3d bboxes. bbox: [z,y,x,d]'''
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
    # iou = int_vol / vol1
    # iou2 = int_vol / vol2
    # return max(iou, iou2)
    print(iou)
    if iou > 0.3:
        return True
    else:
        return False

def d_range(x):
        if abs(x)<4:
            return '小'
        elif abs(x)>=10:
            return '大'
        else:return '中'

def change_value(data_in):
    data_in['desity']=data_in.desity.replace(1,'实性')
    data_in['desity']=data_in.desity.replace(2,'混合性')
    data_in['desity']=data_in.desity.replace(3,'纯磨玻璃')
    data_in['desity']=data_in.desity.replace(4,'纯钙化')
    data_in['desity']=data_in.desity.replace(5,'胸膜实性')
    data_in['desity']=data_in.desity.replace(6,'胸膜钙化')
    data_in['desity']=data_in.desity.replace(7,'胸膜斑化')
    data_in['boundary']=data_in.boundary.replace(1,'清楚')
    data_in['boundary']=data_in.boundary.replace(2,'模糊')
    data_in['b1']=data_in.b1.replace(1,'光滑')
    data_in['b2']=data_in.b2.replace(1,'分叶')
    data_in['b3']=data_in.b3.replace(1,'毛刺')
    data_in['b4']=data_in.b4.replace(1,'毛糙')
    data_in['b5']=data_in.b5.replace(1,'棘突')
    data_in['xg1']=data_in.xg1.replace(1,'聚拢')
    data_in['xg2']=data_in.xg2.replace(1,'推移')
    data_in['xm']=data_in.xm.replace(1,'接触')
    data_in['xm']=data_in.xm.replace(2,'非接触')
    data_in['desity']=data_in.desity.replace(0,'')
    data_in['boundary']=data_in.boundary.replace(0,'')
    data_in['b1']=data_in.b1.replace(0,'')
    data_in['b2']=data_in.b2.replace(0,'')
    data_in['b3']=data_in.b3.replace(0,'')
    data_in['b4']=data_in.b4.replace(0,'')
    data_in['b5']=data_in.b5.replace(0,'')
    data_in['xg1']=data_in.xg1.replace(0,'')
    data_in['xg2']=data_in.xg2.replace(0,'')
    data_in['xm']=data_in.xm.replace(0,'')
    try:
        data_in['d123']=data_in.d123.replace(1,'小')
        data_in['d123']=data_in.d123.replace(2,'中')
        data_in['d123']=data_in.d123.replace(3,'大')

    except:True
    return data_in

def save_to_scv(filename,data):
    # 保存csv
    file = open(filename,'a', newline='')
    csv_write = csv.writer(file,dialect='excel')
    csv_write.writerow(data)
    file.close()

def convertForm(path,save_path3 ,path_model=r'C:\Users\wyk_0\PycharmProjects\Fosun\convert\template.xlsx'):
    # path ： 原始数据的地址 如：path = r'E:\FOSUN\20180820\excel_clean\input.csv'
    # path_model ： 输出的模板 如：path_model = r'E:\FOSUN\20180820\excel_clean\output.xlsx'
    # save_path3 ： 最终输出的表格，存储在哪个路径 如：save_path3 = r'E:\FOSUN\20180820\excel_clean\output_new3.xlsx'
    index = np.array(['序列UID', '图像层厚（mm)', '结节位置（左肺）', '结节位置（右肺）', '数量(整肺）',
       '结节最大径中心X(像素坐标)', '结节最大径中心Y(像素坐标)', '结节最大径中心层面Z(像素坐标)',
       '结节最大径长度(毫米)', '结节最短径长度（毫米）（垂直于最大径的最长径）', '密度', '结节密度分类',
       '边界', '边缘征象', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16',
       'Unnamed: 17', '内部征象', 'Unnamed: 19', 'Unnamed: 20', 'Unnamed: 21',
       'Unnamed: 22', 'Unnamed: 23', '结节周围血管', 'Unnamed: 25',
       'Unnamed: 26', '支气管征象', 'Unnamed: 28', 'Unnamed: 29', 'Unnamed: 30',
       '与胸膜的关系', '胸膜的改变', 'Unnamed: 33', 'Unnamed: 34', '合并表现',
       'Unnamed: 36', 'Unnamed: 37', 'Unnamed: 38', '病人姓名', '性别', '年龄', '既往病史',
       '结节所在肺野', '实验室检查', 'Unnamed: 45', 'Unnamed: 46', '肿瘤标志物', 'Unnamed: 48',
       'Unnamed: 49', 'Unnamed: 50', 'Unnamed: 51', '良恶性', '可靠程度',
       '是否有随访', '随访记录', '备注', '标注分类'])
    #序列UID	图像层厚（mm)	结节位置（左肺）	结节位置（右肺）	数量(整肺）	结节最大径中心X(像素坐标)	结节最大径中心Y(像素坐标)
    #结节最大径中心层面Z(像素坐标)	结节最大径长度(毫米)	结节最短径长度（毫米）（垂直于最大径的最长径）	密度	结节密度分类
    #边界	边缘征象					内部征象						结节周围血管			支气管征象				与胸膜的关系
    #胸膜的改变			合并表现				病人姓名	性别	年龄	既往病史	结节所在肺野	实验室检查			肿瘤标志物
    #良恶性	可靠程度	是否有随访	随访记录	备注	标注分类
    if path.split('.')[-1] == 'csv':
        df = pd.read_csv(path, engine='python')
    if path.split('.')[-1] == 'xlsx':
        df = pd.read_excel(path)
    if path_model.split('.')[-1] == 'csv':
        df_model = pd.read_csv(path_model, engine='python')
    if path_model.split('.')[-1] == 'xlsx':
        df_model = pd.read_excel(path_model)
    #df_model = pd.read_excel(path_model)
    num = df_model.shape[0]
    df_model.drop(list(range(1,num)),inplace=True, axis = 0)

    df_empty = pd.DataFrame(columns=index)
    if 'uid'in df.columns:
        df_empty[u'序列UID'] = df['uid']
    if 'seriesuid'in df.columns:
        df_empty[u'序列UID'] = df['seriesuid']
    if 'coordX' in df.columns:
        df_empty['结节最大径中心X(像素坐标)'] = (df['coordX']+0.5).apply(int)
    if 'x' in df.columns:
        df_empty['结节最大径中心X(像素坐标)'] = (df['x']+0.5).apply(int)
    if 'coordY' in df.columns:
        df_empty['结节最大径中心Y(像素坐标)'] = (df['coordY']+0.5).apply(int)
    if 'y' in df.columns:
        df_empty['结节最大径中心Y(像素坐标)'] = (df['y']+0.5).apply(int)
    if 'coordZ' in df.columns:
        df_empty['结节最大径中心层面Z(像素坐标)'] = (df['coordZ']+0.5).apply(int)
    if 'z' in df.columns:
        df_empty['结节最大径中心层面Z(像素坐标)'] = (df['z']+0.5).apply(int)
    if 'diameter_mm' in df.columns:
        df_empty['结节最大径长度(毫米)'] = df['diameter_mm']
    if 'diameter' in df.columns:
        df_empty['结节最大径长度(毫米)'] = df['diameter']
    if 'd' in df.columns:
        df_empty['结节最大径长度(毫米)'] = df['d']
    if 'image_path' in df.columns:
        df_empty['边缘征象'] = df['image_path']
    if 'type' in df.columns:
        df_empty['备注'] = df['type']
    if 'spacing' in df.columns:
        df_empty['图像层厚（mm)'] = df['spacing']
    if 'id' in df.columns:
        df_empty['年龄'] = df['id']
    if 'probability' in df.columns:
        df_empty['备注'] = df['probability']
    if 'det_probability' in df.columns:
        df_empty['备注'] = df['det_probability']
    if 'cls_probability' in df.columns:
        df_empty['随访记录'] = df['cls_probability']
    final = df_model.append(df_empty)
    final.to_excel(save_path3, index = False)  #将最后结果存储，不许存储可注释本行
    return final
############################################################################################
# 原始检测函数
def check_data(predict_filename,bianzhu_filename,hospital_name,prob=0):
    pred   = pd.read_csv( predict_filename,engine='python')
    biaozhu= pd.read_csv(bianzhu_filename,engine='python')
    predict=pd.DataFrame(pred)
    try:    predict=predict[predict.probability>=prob]
    except: True
    lable=pd.DataFrame(biaozhu)
    try:     predict.rename(columns={'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    csvfilename = hospital_name+'_'+'check_result.csv'
    crosstabname = hospital_name+'_'+'crosstab.csv'
    final_success_rate_file = hospital_name+'_'+'success_rate.csv'
    try:
        os.remove(csvfilename)
        os.remove(crosstabname)
        os.remove(final_success_rate_file)
    except:True
    time.sleep(0.5)
    out_title=['uid','x','y','z','d','all_01','desity','boundary','b1','b2','b3','b4','b5','xg1','xg2','xm','d123']
    save_to_scv(csvfilename,out_title)
    lable['d123'] = lable.d.apply(lambda x: d_range(x))
    print('\nChecking.....')


    for i in range(0,len(lable.uid)):
        # 打印进度
        fenmu=len(lable.uid)
        sys.stdout.write('\r%s%%'%round((i / fenmu * 100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(predict[predict['uid'] == lable.uid[i]])
        index_tt = tt.index#建立索引，直接按索引中提取信息
        for j in index_tt:
            if judge(lable.x[i],lable.y[i],lable.z[i],predict.x[j],predict.y[j],predict.z[j],lable.d[i],predict.d[j]):
                normal_pd.append(1)
            else:
                normal_pd.append(0)
        if 1 in normal_pd: all_01 = 1
        else:              all_01 = 0
        #保存数据

        out=[lable.uid[i],lable.x[i],lable.y[i],lable.z[i],lable.d[i],all_01,lable.desity[i],lable.boundary[i],lable.b1[i],lable.b2[i],lable.b3[i],lable.b4[i],lable.b5[i],lable.xg1[i],lable.xg2[i],lable.xm[i],lable.d123[i]]
        save_to_scv(csvfilename,out)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()
    time.sleep(0.5)



    # 计算成功率部分
    print('\n正在计算成功率')
    file= pd.read_csv(csvfilename,engine='python')
    data_in=pd.DataFrame(file)
    del_title=['uid','x','y','z','d','all_01']
    for i in del_title:
        try:out_title.remove(i)
        except:True
    title=out_title
    for m in range(0,len(title)):
        a=pd.crosstab(data_in[title[m]],data_in['all_01'],margins=True)
        b=a[1]/(a[0]+a[1])
        b=pd.DataFrame(b)
        b.to_csv(final_success_rate_file,mode='a')
        a=pd.DataFrame(a)
        a.to_csv(crosstabname,mode='a',encoding='utf-8-sig')
    a=pd.read_csv(final_success_rate_file,engine='python',encoding='utf-8-sig')
    a=a[(a.desity!='0')&(a.desity!='All')]
    a=a.set_index(["desity"])
    a.to_csv(final_success_rate_file,encoding='utf-8-sig')
    print('结果已保存...\n校对结果文件名为：',csvfilename,'\n列联表文件名为：',crosstabname,'\n成功率结果文件名为：',final_success_rate_file)

# 结果直接生成报表格式
def check_sig(predict_filename, bianzhu_filename, hospital_name, prob=0, prob_max=1):
    pred   = pd.read_csv( predict_filename,engine='python')
    biaozhu= pd.read_csv(bianzhu_filename,engine='python')
    predict=pd.DataFrame(pred)
    try:    predict = predict[predict.probability>=prob]
    except: True
    try:    predict = predict[predict.probability<=prob_max]
    except: True
    lable = pd.DataFrame(biaozhu)
    try:     predict.rename(columns = {'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    csvfilename = hospital_name+'_'+'check_result.csv'
    final_success_rate_file = hospital_name+'_'+'success_rate.xlsx'
    try:
        os.remove(csvfilename)
        os.remove(final_success_rate_file)
    except:True
    time.sleep(0.1)
    out_title=['uid','x','y','z','d','all_01','desity','boundary','b1','b2','b3','b4','b5','xg1','xg2','xm','d123']
    save_to_scv(csvfilename,out_title)
    lable['d123'] = lable.d.apply(lambda x: d_range(x))
    print('\nChecking.....')
    for i in range(0,len(lable.uid)):
        fenmu=len(lable.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(predict[predict['uid'] == lable.uid[i]])
        index_tt = tt.index#建立索引，直接按索引中提取信息
        for j in index_tt:
            if judge(lable.x[i],lable.y[i],lable.z[i],predict.x[j],predict.y[j],predict.z[j],lable.d[i],predict.d[j]):  normal_pd.append(1)
            else: normal_pd.append(0)
        if 1 in normal_pd: all_01 = 1
        else:              all_01 = 0
        out=[lable.uid[i],lable.x[i],lable.y[i],lable.z[i],lable.d[i],all_01,lable.desity[i],lable.boundary[i],lable.b1[i],lable.b2[i],lable.b3[i],lable.b4[i],lable.b5[i],lable.xg1[i],lable.xg2[i],lable.xm[i],lable.d123[i]]
        save_to_scv(csvfilename,out)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()
    time.sleep(0.5)
    print('\n正在计算成功率')
    file= pd.read_csv(csvfilename,engine='python')
    TP_FNlist=file.all_01.value_counts()
    TP_label=TP_FNlist[1]
    FN=TP_FNlist[0]
    data_in = change_value(file)
    del_title = ['uid','x','y','z','d','all_01']
    for i in del_title:
        try:out_title.remove(i)
        except:True
    empty = pd.DataFrame({'feature':['实性','混合性','纯磨玻璃','纯钙化','胸膜实性','胸膜钙化','胸膜斑化',
                                     '清楚','模糊','光滑','分叶','毛刺','毛糙','棘突','聚拢','推移','接触','非接触',
                                     '小','中','大']})
    inner = pd.DataFrame([])
    for i in out_title:
        a=pd.crosstab(data_in[i],data_in.all_01)
        a.rename(columns={0:'未检出',1:'检出'},inplace=True)
        a=pd.DataFrame(a)
        inner = pd.concat([inner,a])
    empty = pd.merge(empty,inner,left_on='feature',right_index=True)
    empty['总数'] = empty['检出'] + empty['未检出']
    empty['检出率'] = empty['检出']/(empty['总数'] + 0.00001)
    empty['检出率'] = empty['检出率'].apply(lambda x: format(x, '.1%'))
    empty.to_excel(final_success_rate_file,encoding='utf-8-sig')
    print('结果已保存...\n校对结果文件名为：',csvfilename,'\n成功率结果文件名为：',final_success_rate_file)

def compare(pred_check_result,cls_check_result):
    pred = pd.read_csv( pred_check_result, engine = 'python' )
    cls = pd.read_csv( cls_check_result, engine = 'python' )
    P = pd.DataFrame(pred)
    C = pd.DataFrame(cls)
    P['pred_01'], P['cls_01'] = P['all_01'], C['all_01']
    res = P[P.pred_01 == 1]
    v_name = ['desity','boundary','b1','b2','b3','b4','b5','xg1','xg2','xm','d123']
    for i in v_name:
        df_empty = pd.DataFrame(columns=['预测总数', '删除数量', '误删率'])
        a = pd.crosstab(res[i],res.cls_01)
        a = pd.DataFrame(a)
        df_empty['预测总数'] = a[0]+a[1]
        df_empty['删除数量'] = a[0]
        df_empty['误删率'] = a[0]/(a[0]+a[1])
        df_empty.to_csv('DBA_'+cls_check_result,mode='a',encoding='utf-8-sig')
    print('\n误删情况结果文件名为：','DBA_'+cls_check_result)
    # P.to_csv('merge_table_'+cls_check_result)
    P.to_excel('merge_table_' + cls_check_result.replace('csv','xlsx'))

# 计算大中小结节probability的mean和var
def anti_check(predict_filename,bianzhu_filename,hospital_name,prob=0):
    pred   = pd.read_csv( predict_filename,engine='python')
    biaozhu = pd.read_csv(bianzhu_filename,engine='python')
    biaozhu = change_value(biaozhu)
    predict=pd.DataFrame(pred)
    try:    predict=predict[predict.probability>=prob]
    except: True
    lable=pd.DataFrame(biaozhu)
    try:     predict.rename(columns={'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    csvfilename = hospital_name+'_'+'check_result.csv'
    final_success_rate_file = hospital_name+'_mean_and_var.xlsx'
    try:
        os.remove(csvfilename)
        os.remove(final_success_rate_file)
    except:True
    time.sleep(0.1)
    out_title=['uid','x','y','z','d','probability','all_01','desity','boundary','b1','b2','b3','b4','b5','xg1','xg2','xm','d123']
    save_to_scv(csvfilename,out_title)
    lable['d123'] = lable.d.apply(lambda x: d_range(x))
    print('\nChecking.....')
    for i in range(0,len(predict.uid)):
        fenmu=len(predict.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        tt = pd.DataFrame(lable[lable['uid'] == predict.uid[i]])
        index_tt = tt.index
        for j in index_tt:
            if judge(lable.x[j],lable.y[j],lable.z[j],predict.x[i],predict.y[i],predict.z[i],lable.d[j],predict.d[i]):
                all_01=1
                out=[predict.uid[i],predict.x[i],predict.y[i],predict.z[i],predict.d[i],predict.probability[i],all_01,lable.desity[j],lable.boundary[j],lable.b1[j],lable.b2[j],lable.b3[j],lable.b4[j],lable.b5[j],lable.xg1[j],lable.xg2[j],lable.xm[j],lable.d123[j]]
                save_to_scv(csvfilename,out)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()
    time.sleep(0.1)
    print('\n正在计算成功率')
    file= pd.read_csv(csvfilename,engine='python')
    data_in=pd.DataFrame(file)

    empty = pd.DataFrame({'feature':['实性','混合性','纯磨玻璃','纯钙化','胸膜实性','胸膜钙化',
                                     '胸膜斑化','清楚','模糊','光滑','分叶','毛刺','毛糙','棘突','聚拢','推移','接触','非接触']})
    for j in ['小','中','大']:
        data2=pd.DataFrame(data_in[data_in.d123==j])
        out_title=['desity','boundary','b1','b2','b3','b4','b5','xg1','xg2','xm']
        inner = pd.DataFrame([])
        for i in out_title:
            data3 = pd.DataFrame(data2,columns=[i,'probability'])#.reset_index()
            x = data3.groupby(by=[i]).mean()
            x.rename(columns={'probability':str(j)+'_mean'}, inplace=True)
            a = data3.groupby(by=[i]).var()
            a.rename(columns={'probability':str(j)+'_var'}, inplace=True)
            c=data3.groupby(by=[i]).count()
            c.rename(columns={'probability':str(j)+'_counts'}, inplace=True)
            x = pd.concat([x,a],axis=1)
            x = pd.concat([x,c],axis=1)
            inner = pd.concat([inner,x])
        empty = pd.merge(empty,inner,left_on='feature',right_index=True,how='outer')
    empty.to_excel(final_success_rate_file,encoding='utf-8-sig')

# 以一个结果作为 lable 去检测另一个结果
def inter_check(predict_filename,bianzhu_filename):
    pred   = pd.read_csv( predict_filename,engine='python')
    biaozhu = pd.read_csv(bianzhu_filename,engine='python')
    predict = pd.DataFrame(pred)
    lable=pd.DataFrame(biaozhu)
    try:     predict.rename(columns={'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    try:     lable.rename(columns={'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    if 'probability' in predict.columns:
        out_title=['uid','coordX','coordY','coordZ','diameter','all_01','probability']
    elif 'cls_probability'  in  predict.columns:
        out_title=['uid','coordX','coordY','coordZ','diameter','all_01','det_probability','cls_probability']
    else:out_title=['uid','coordX','coordY','coordZ','diameter','all_01']
    save_to_scv(bianzhu_filename.replace('.csv','_out.csv'),out_title)
    print('\nChecking.....')
    for i in range(0,len(predict.uid)):
        fenmu=len(predict.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(lable[lable['uid'] == predict.uid[i]])
        index_tt = tt.index
        for j in index_tt:
            if judge(lable.x[j],lable.y[j],lable.z[j],predict.x[i],predict.y[i],predict.z[i],lable.d[j],predict.d[i]):
                normal_pd.append(1)
            else:
                normal_pd.append(0)
        if 1 in normal_pd: all_01 = 1
        else:              all_01 = 0
        if 'probability' in predict.columns:
            out=[predict.uid[i],predict.x[i],predict.y[i],predict.z[i],predict.d[i],all_01,predict.probability[i]]
        elif 'cls_probability'  in  predict.columns:
            out=[predict.uid[i],predict.x[i],predict.y[i],predict.z[i],predict.d[i],all_01,predict.det_probability[i],predict.cls_probability[i]]
        else:out=[predict.uid[i],predict.x[i],predict.y[i],predict.z[i],predict.d[i],all_01]
        save_to_scv(bianzhu_filename.replace('.csv','_out.csv'),out)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()

# 合并不同概率的结果
def merge_diff_prob(pred_or_cls_file,prob_list):
    empty = pd.DataFrame({'feature':['实性','混合性','纯磨玻璃','纯钙化','胸膜实性','胸膜钙化','胸膜斑化',
                                 '清楚','模糊','光滑','分叶','毛刺','毛糙','棘突','聚拢','推移','接触','非接触',
                                 '小','中','大']})
    for i in prob_list:
        filename=str(i)+pred_or_cls_file.replace('.csv','_success_rate.xlsx')
        a=pd.read_excel(filename)
        empty[str(i)]=a['检出率']
    empty.to_excel(pred_or_cls_file.replace('.csv','')+'_merge_table.xlsx',encoding='utf-8-sig')

# 计算TP、FP、FN、precision、recall，并生成TP、FP、FN的机器可读的文件。
def divide(predict_filename, bianzhu_filename, mark ='', uid_list_file ='', prob_min = 0, prob_max = 1, prob_cls_min = 0 , prob_cls_max = 1, convert = True,cache = False, check_file = False):
    pred   = pd.read_csv( predict_filename, engine = 'python')
    biaozhu= pd.read_csv( bianzhu_filename, engine = 'python')
    predict=pd.DataFrame(pred)
    lable = pd.DataFrame(biaozhu)
    if prob_min != 0:
        try:    predict = predict[predict.probability >= prob_min]
        except: True
        try:    predict = predict[predict.det_probability >= prob_min]
        except: True
    if prob_max != 1:
        try:    predict = predict[predict.probability <= prob_max]
        except: True
        try:    predict = predict[predict.det_probability <= prob_max]
        except: True
    if prob_cls_min != 0:
        try:    predict = predict[predict.cls_probability >= prob_cls_min]
        except: True
    if prob_cls_max != 1:
        try:    predict = predict[predict.cls_probability <= prob_cls_max]
        except: True
    if uid_list_file != '':
        uid_list = pd.read_csv(uid_list_file, engine = 'python')
        predict = predict[predict['uid'].isin(uid_list['uid'].tolist())].reset_index(drop = True)
        lable = lable[lable['uid'].isin(uid_list['uid'].tolist())].reset_index(drop = True)
    predict = predict[predict['uid'].isin(lable['uid'].tolist())].reset_index(drop = True)
    lable = lable[lable['uid'].isin(predict['uid'].tolist())].reset_index(drop = True)
    try: predict.rename(columns = {'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace = True)
    except: True
    try: lable.rename(columns = {'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace = True)
    except: True
    time.sleep(0.1)
    print('\nChecking label file.....')
    lable_result = pd.DataFrame(columns = ['uid','x','y','z','d','all_01'])
    for i in range(0,len(lable.uid)):
        fenmu=len(lable.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(predict[predict['uid'] == lable.uid[i]])
        index_tt = tt.index#建立索引，直接按索引中提取信息
        for j in index_tt:
            if judge(lable.x[i],lable.y[i],lable.z[i],predict.x[j],predict.y[j],predict.z[j],lable.d[i],predict.d[j]):  normal_pd.append(1)
            else: normal_pd.append(0)
        if 1 in normal_pd: all_01 = 1
        else:              all_01 = 0
        data = pd.Series({
            'uid':lable.uid[i],
            'x':lable.x[i],
            'y':lable.y[i],
            'z':lable.z[i],
            'd':lable.d[i],
            'all_01':all_01
        })
        lable_result = lable_result.append(data, ignore_index = True)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()

    print('\nChecking predict file.....')
    if 'probability' in predict.columns:
        pred_result = pd.DataFrame(columns = ['uid','x','y','z','d','probability','all_01'])
    if 'cls_probability'  in  predict.columns:
        pred_result = pd.DataFrame(columns = ['uid', 'x', 'y', 'z', 'd', 'det_probability', 'cls_probability', 'all_01'])
    for i in range(0,len(predict.uid)):
        fenmu=len(predict.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(lable[lable['uid'] == predict.uid[i]])
        index_tt = tt.index
        for j in index_tt:
            if judge(lable.x[j],lable.y[j],lable.z[j],predict.x[i],predict.y[i],predict.z[i],lable.d[j],predict.d[i]):  normal_pd.append(1)
            else:  normal_pd.append(0)
        if 1 in normal_pd: all_01 = 1
        else:              all_01 = 0
        if 'probability' in predict.columns:
            data = pd.Series({
                'uid':predict.uid[i],
                'x':predict.x[i],
                'y':predict.y[i],
                'z':predict.z[i],
                'd':predict.d[i],
                'probability':predict.probability[i],
                'all_01':all_01
            })
        if 'cls_probability'  in  predict.columns:
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
        pred_result.to_csv(predict_filename.replace('.csv','_check_result.csv'))
        lable_result.to_csv(bianzhu_filename.replace('.csv','_check_result.csv'))
        if  convert == True:
            convertForm(predict_filename.replace('.csv','_check_result.csv'),predict_filename.replace('.csv','_check_result.xlsx'))
            convertForm(bianzhu_filename.replace('.csv','_check_result.csv'),bianzhu_filename.replace('.csv','_check_result.xlsx'))
            try:
                os.remove(bianzhu_filename.replace('.csv','_check_result.csv'))
                os.remove(predict_filename.replace('.csv','_check_result.csv'))
            except:True
    TP_lable = lable_result.all_01.tolist().count(1)
    FN = lable_result.all_01.tolist().count(0)
    TP_pred = pred_result.all_01.tolist().count(1)
    FP = pred_result.all_01.tolist().count(0)
    print('\n以标注文件中预测正确的数量作为TP：')
    recall_label = TP_lable / (TP_lable + FN)
    precision_label = TP_lable / (TP_lable + FP)
    print('\nTP  :',TP_lable,'\nFP  :',FP,'\nFN  :',FN)
    print('recall   :', str(round(recall_label*100,2))+'%')
    print('precision:', str(round(precision_label*100,2))+'%')
    print('\n以预测文件中预测正确的数量作为TP：')
    recall_pred = TP_pred/(TP_pred+FN)
    precision_pred = TP_pred/(TP_pred+FP)
    print('\nTP  :',TP_pred,'\nFP  :',FP,'\nFN  :',FN)
    print('recall   :', str(round(recall_pred*100,2))+'%')
    print('precision:', str(round(precision_pred*100,2))+'%')

    if convert == True:
        print('\n正在生成 TP_pred, TP_lable, FP, FN 文件.....')
        TP_pred_file = pred_result[pred_result['all_01'] == 1]
        FP_file = pred_result[pred_result['all_01'] == 0]
        TP_lable_file = lable_result[lable_result['all_01'] == 1]
        FN_file = lable_result[lable_result['all_01'] == 0]
        TP_pred_file.to_csv(mark + 'TP_pred.csv')
        FP_file.to_csv(mark + 'FP.csv')
        TP_lable_file.to_csv(mark + 'TP_lable.csv')
        FN_file.to_csv(mark + 'FN.csv')
        convertForm(mark + 'TP_pred.csv',mark + 'TP_pred.xlsx')
        convertForm(mark + 'FP.csv',mark + 'FP.xlsx')
        convertForm(mark + 'TP_lable.csv',mark + 'TP_lable.xlsx')
        convertForm(mark + 'FN.csv',mark + 'FN.xlsx')


        if cache == False:
            print('\n正在移除中间文件......')
            try:
                os.remove(mark + 'TP_pred.csv')
                os.remove(mark + 'FP.csv')
                os.remove(mark + 'TP_lable.csv')
                os.remove(mark + 'FN.csv')
                print('\n中间文件移除成功......')
            except:print('\n中间文件移除失败......')
    print('\n   Mission Complete ！')
    return [recall_label,precision_label]

def double_lable_check(lable1,lable2):
    pred   = pd.read_csv( lable1,engine='python')
    biaozhu = pd.read_csv(lable2,engine='python')
    predict = pd.DataFrame(pred)
    lable=pd.DataFrame(biaozhu)
    try:     predict.rename(columns={'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    try:     lable.rename(columns={'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace=True)
    except:  True
    if 'probability' in predict.columns:
        out_title=['uid','coordX','coordY','coordZ','diameter','all_01','probability']
    elif 'cls_probability'  in  predict.columns:
        out_title=['uid','coordX','coordY','coordZ','diameter','all_01','det_probability','cls_probability']
    else:out_title=['uid','coordX','coordY','coordZ','diameter','all_01']
    save_to_scv(lable2.replace('.csv','_out.csv'),out_title)
    print('\nChecking.....')
    for i in range(0,len(predict.uid)):
        fenmu=len(predict.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(lable[lable['uid'] == predict.uid[i]])
        index_tt = tt.index
        for j in index_tt:
            if judge(lable.x[j],lable.y[j],lable.z[j],predict.x[i],predict.y[i],predict.z[i],lable.d[j],predict.d[i]):
                normal_pd.append(1)
            else:
                normal_pd.append(0)
        if 1 in normal_pd: all_01 = 1
        else:              all_01 = 0
        if 'probability' in predict.columns:
            out=[predict.uid[i],predict.x[i],predict.y[i],predict.z[i],predict.d[i],all_01,predict.probability[i]]
        elif 'cls_probability'  in  predict.columns:
            out=[predict.uid[i],predict.x[i],predict.y[i],predict.z[i],predict.d[i],all_01,predict.det_probability[i],predict.cls_probability[i]]
        else:out=[predict.uid[i],predict.x[i],predict.y[i],predict.z[i],predict.d[i],all_01]
        save_to_scv(lable2.replace('.csv','_out.csv'),out)
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()

def diff_tags_recall_precision(predict_filename, bianzhu_filename, mark ='', uid_list_file ='',index_file = '', prob_min = 0, prob_max = 1, prob_cls_min = 0 , prob_cls_max = 1, convert = True,cache = False, check_file = False):
    pred   = pd.read_csv( predict_filename, engine = 'python')
    biaozhu= pd.read_csv( bianzhu_filename, engine = 'python')
    if index_file != '':
        index_file= pd.read_csv( index_file, engine = 'python')
        pred = pd.merge(pred,index_file,on='uid')
        biaozhu = pd.merge(biaozhu,index_file,on='uid')
    predict=pd.DataFrame(pred)
    lable = pd.DataFrame(biaozhu)
    if prob_min != 0:
        try:    predict = predict[predict.probability >= prob_min]
        except: True
        try:    predict = predict[predict.det_probability >= prob_min]
        except: True
    if prob_max != 1:
        try:    predict = predict[predict.probability <= prob_max]
        except: True
        try:    predict = predict[predict.det_probability <= prob_max]
        except: True
    if prob_cls_min != 0:
        try:    predict = predict[predict.cls_probability >= prob_cls_min]
        except: True
    if prob_cls_max != 1:
        try:    predict = predict[predict.cls_probability <= prob_cls_max]
        except: True
    predict = predict[predict['uid'].isin(lable['uid'].tolist())].reset_index(drop = True)
    lable = lable[lable['uid'].isin(predict['uid'].tolist())].reset_index(drop = True)
    try: predict.rename(columns = {'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace = True)
    except: True
    try: lable.rename(columns = {'coordX':'x', 'coordY': 'y', 'coordZ': 'z', 'diameter': 'd'}, inplace = True)
    except: True
    print('\nChecking label file.....')
    lable_result = lable.copy()
    pred_result = predict.copy()
    lable_result['all_01'] = -9
    pred_result['all_01'] = -9
    for i in range(0,len(lable.uid)):
        fenmu=len(lable.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(predict[predict['uid'] == lable.uid[i]])
        index_tt = tt.index#建立索引，直接按索引中提取信息
        for j in index_tt:
            if judge(lable.x[i],lable.y[i],lable.z[i],predict.x[j],predict.y[j],predict.z[j],lable.d[i],predict.d[j]):  normal_pd.append(1)
            else: normal_pd.append(0)
        if 1 in normal_pd: lable_result.loc[i,'all_01'] = 1
        else:              lable_result.loc[i,'all_01'] = 0
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()
    if check_file == True:
        lable_result.to_csv(bianzhu_filename.replace('.csv','_check_result.csv'),encoding = 'utf-8-sig')
    print('\nChecking predict file.....')
    for i in range(0,len(predict.uid)):
        fenmu=len(predict.uid)
        sys.stdout.write('\r%s%%'%round((i/fenmu*100),2))
        sys.stdout.flush()
        normal_pd=[]
        tt = pd.DataFrame(lable[lable['uid'] == predict.uid[i]])
        index_tt = tt.index
        for j in index_tt:
            if judge(lable.x[j],lable.y[j],lable.z[j],predict.x[i],predict.y[i],predict.z[i],lable.d[j],predict.d[i]):  normal_pd.append(1)
            else:  normal_pd.append(0)
        if 1 in normal_pd: pred_result.loc[i,'all_01'] = 1
        else:              pred_result.loc[i,'all_01'] = 0
    sys.stdout.write('\r%s%%'%(100))
    sys.stdout.flush()
    print('\n')
    if check_file == True:
        pred_result.to_csv(predict_filename.replace('.csv','_check_result.csv'),encoding = 'utf-8-sig')
    TP_lable = lable_result.all_01.tolist().count(1)
    FN = lable_result.all_01.tolist().count(0)
    TP_pred = pred_result.all_01.tolist().count(1)
    FP = pred_result.all_01.tolist().count(0)
    print('\n以标注文件中预测正确的数量作为TP：')
    recall_label = TP_lable / (TP_lable + FN)
    precision_label = TP_lable / (TP_lable + FP)
    print('\nTP  :',TP_lable,'\nFP  :',FP,'\nFN  :',FN)
    print('recall   :', str(round(recall_label*100,2))+'%')
    print('precision:', str(round(precision_label*100,2))+'%')
    print('\n以预测文件中预测正确的数量作为TP：')
    recall_pred = TP_pred/(TP_pred+FN)
    precision_pred = TP_pred/(TP_pred+FP)
    print('\nTP  :',TP_pred,'\nFP  :',FP,'\nFN  :',FN)
    print('recall   :', str(round(recall_pred*100,2))+'%')
    print('precision:', str(round(precision_pred*100,2))+'%')
    try:os.remove(mark + 'out_file.csv')
    except:True
    v_name = ['SliceThickness','ConvolutionKernel','Manufacturer','KVP','R&E']
    outfile_name=['hspt','v_type','n_type','TP_lable','TP_pred','FN','FP','recall_label','precision_label','recall_pred','precision_pred']
    save_to_scv(mark + 'out_file.csv',outfile_name)
    for i in v_name:
        list = lable_result[i].drop_duplicates().tolist()
        for j in list:
            df_lable = lable_result[lable_result[i] == j]
            df_pred = pred_result[pred_result[i] == j]
            TP_lable = df_lable.all_01.tolist().count(1)
            FN = df_lable.all_01.tolist().count(0)
            TP_pred = df_pred.all_01.tolist().count(1)
            FP = df_pred.all_01.tolist().count(0)
            print('\n以标注文件中预测正确的数量作为TP：')
            recall_label = TP_lable / (TP_lable + FN)
            precision_label = TP_lable / (TP_lable + FP)
            print('\nTP  :',TP_lable,'\nFP  :',FP,'\nFN  :',FN)
            print('recall   :', str(round(recall_label*100,2))+'%')
            print('precision:', str(round(precision_label*100,2))+'%')
            print('\n以预测文件中预测正确的数量作为TP：')
            recall_pred = TP_pred/(TP_pred+FN)
            precision_pred = TP_pred/(TP_pred+FP)
            print('\nTP  :',TP_pred,'\nFP  :',FP,'\nFN  :',FN)
            print('recall   :', str(round(recall_pred*100,2))+'%')
            print('precision:', str(round(precision_pred*100,2))+'%')
            outfile_data=[mark,i,j,TP_lable,TP_pred,FN,FP,recall_label,precision_label,recall_pred,precision_pred]
            save_to_scv(mark + 'out_file.csv',outfile_data)


def inter_check2(predict_filename,bianzhu_filename):
    pred   = pd.read_csv( predict_filename,engine='python')
    biaozhu = pd.read_csv(bianzhu_filename,engine='python')
    predict = pd.DataFrame(pred)
    lable=pd.DataFrame(biaozhu)
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
            if judge(lable.x[j],lable.y[j],lable.z[j],predict.x[i],predict.y[i],predict.z[i],lable.d[j],predict.d[i]):
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
    predict.to_csv(predict_filename.replace('.csv','_result.csv'),index=False,encoding='utf-8-sig')
