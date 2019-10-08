import os
import shutil
import pydicom
from os.path import join, getsize


path = r"E:\新建文件夹 (2)"
del_path = r"E:\新建文件夹 (3)"
file_list = os.listdir(path)
size = 30
print(file_list)
def getdirsize(dir):
   size = 0
   for root, dirs, files in os.walk(dir):
      size += sum([getsize(join(root, name)) for name in files])
   return size


for i in range(len(file_list)):
    file_name = file_list[i]
    file_path = os.path.join(path, file_name)
    print(file_path)
    file_size = getdirsize(file_path)
    print(file_size)
    save_path = os.path.join(del_path, file_name)
    if file_size <= size:
        shutil.move(file_path, save_path)

    dicom_list = os.listdir(file_path)
    dicom_path = os.path.join(file_path,dicom_list[0])
    dcm = pydicom.read_file(dicom_path)
    kvp = dcm.KVP
    need_str1 = "chest"
    need_str2 = "thorax"
    if need_str1 not in kvp and need_str2 not in kvp:
        shutil.move(file_path, save_path)
    print(kvp)

