import os
import shutil
import pydicom
from os.path import join, getsize

from pydicom import dicomio
import SimpleITK as sitk
import numpy as np


# dicomPath2 = r"E:\new_dir\1002480402170216154051\1.3.12.2.1107.5.1.4.58462.30000017021514463903100003011"
def get_tag(dicomPath1,dicomPath2):
    dcm = pydicom.dcmread(dicomPath1)  # 选择一个普通的非压缩dcm文件作为转换模板
    image = sitk.ReadImage(dicomPath2)
    image_array = sitk.GetArrayFromImage(image)
    np_array = np.int16(image_array)
    image_array = np.squeeze(np_array)  # 读取有压缩分段的dcm图像数据
    dataset = pydicom.dcmread(dicomPath2)  # 用来修改Tag，图像读写相关的tag都要改
    dcm.data_element('PixelSpacing').value = dataset.data_element('PixelSpacing').value
    dcm.data_element('RescaleIntercept').value = dataset.data_element('RescaleIntercept').value
    dcm.data_element('RescaleSlope').value = dataset.data_element('RescaleSlope').value
    dcm.PixelData = image_array.tobytes()
    dcm.save_as(dicomPath2)
    dcm = dicomio.read_file(dicomPath2)
    return dcm.StudyDescription



dicomPath1 = r"E:\fuxing_idea\dicom\Li_Yan_3a85e_00274.dcm"

path = r"E:\新建文件夹 (2)"
del_path = r"E:\新建文件夹 (3)"
save_path = r"E:\新建文件夹 (4)"
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
    targetDir = os.path.join(save_path,dicom_list[0])

    shutil.copy(dicom_path, targetDir)

    # dcm = pydicom.read_file(dicom_path)
    StudyDescription = get_tag(dicomPath1,targetDir)
    os.remove(targetDir)
    need_str1 = "chest"
    need_str2 = "thorax"
    if need_str1 not in StudyDescription and need_str2 not in StudyDescription:
        shutil.move(file_path, save_path)
    print(StudyDescription)

