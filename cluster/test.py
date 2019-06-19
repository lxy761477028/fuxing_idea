# import xlwt
# import xlrd
# import pandas as pd
#
# from matching import mine
#
# z_scope = 2   #z轴浮动次数
# z_size = 2  #z轴浮动大小
# multiple = 1  #半径放大倍数
# percent = 0.4  #匹配率
#
# #读取文件
# path = r"E:\first\cluster\2019_6_12\data.csv"
# answer_path = r"E:\first\cluster\2019_6_12\answer.csv"
# nd = pd.read_csv(path)
# serial_number = nd["序列编号"]
# data = nd["影像结果"]
# print(type(nd))
# print(data[0])
# print(type(data[0]))
#
#
# data = [{'imgNo': 78, 'imgData': '{"x":78.62,"y":303.39,"z":456.0,"mind":0.86,"maxd":2.29,"direction":"{"x":0.0,"y":0.0,"z":0}"}'}, {'imgNo': 10076, 'imgData': '{"x":425.14490005766277,"y":166.16575357076402,"z":551.0,"mind":10.210793673375278,"maxd":10.940136078616357,"direction":"{"x":14.252798148222837,"y":13.302611605007996,"z":0.0}"}'}]
#
# maping(data)
#
# {'info': {'errormage': 'success', 'list': [[79], [10070]]}, 'detail': {}, 'result': True, 'code': 0}

# a = -1
# b = abs(a)
# print(b)


from check import judge

f = judge(82.42, 255.42, 352, 416.1624365482233, 279.06598984771574, 392, 8.1, 10.606602395939085)
print(f)