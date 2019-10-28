import csv
import datetime
import shutil
import os


birth_data = []
dict_data = {}
sole_dict = {}
serial_number = []

path = r"E:\fuxing_idea\dicom_tag\xulie.csv"
file_path = r"E:\fuxing_idea\dicom_tag\file"
save_path = r"E:\fuxing_idea\dicom_tag\save_path"
with open(path, encoding='utf-8-sig') as csvfile:
    csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
    # birth_header = next(csv_reader)  # 读取第一行每一列的标题
    for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
        birth_data.append(row[0])
        number = row[0][0:8]
        try:
            birth_list = dict_data[number]
            birth_list.append(row[0])
            dict_data[number] = birth_list
        except KeyError:
            dict_data[number] = [row[0]]
    for key in dict_data:
        key_data = dict_data[key]
        time_data = datetime.datetime.strptime("2019-1-1", "%Y-%m-%d")
        for i in key_data:
            if len(i) == 22:

            check_time = i[8:12] + "-" + i[12:14] + "-" + i[14:16]
            date = datetime.datetime.strptime(check_time, "%Y-%m-%d")
            # time_data = date
            if date < time_data:
                sole_dict[key] = i
                time_data = date
            else:
                pass

f1 = open(save_path + '/test.txt','w')
for key in sole_dict:
    for key in sole_dict:
        f1.write(sole_dict[key]+"\n")
f1.close()

for key in sole_dict:
    file_name = sole_dict[key]
    old_path = os.path.join(file_path, file_name)
    new_path = os.path.join(save_path, file_name)

    shutil.move(old_path, new_path)
        # number = row[0][0:8]
        # serial_number.append(number)
    # for sole_number in birth_data:
    #     number = sole_number[0:8]
    #     if number not in serial_number:
    #         sole_data.append(sole_number)
    #         serial_number.append(number)
    #         # dict_data
    #     else:
    #         # over_time =
    #         print(number)
    # print(birth_data)
    # print(serial_number)
    # print(sole_data)
    print(dict_data)
    print(sole_dict)