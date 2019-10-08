import pydicom
from pydicom import dicomio
import SimpleITK as sitk
import numpy as np

dicomPath1 = r"E:\fuxing_idea\dicom\Li_Yan_3a85e_00274.dcm"
#
dicomPath2 = r"E:\new_dir\1002480402170216154051\1.3.12.2.1107.5.1.4.58462.30000017021514463903100003011"

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
# dcm = SimpleITK.ReadImage(dicomPath)
# data = SimpleITK.GetArrayFromImage(dcm)
print(dcm.StationName)
#
# np_array = np.int16(data)
# image_array = np.squeeze(np_array)                                  #获得图像数据
#
# reader = SimpleITK.ImageFileReader()
# reader.LoadPrivateTagsOn()
# reader.ReadImageInformation()
#
# ImageType = reader.GetMetaData('0018|1140')
#
# print(ImageType)

# tag = str(dcm)
#
#
# #获取上传的mask.zip文件
# f = request.files['mask']
# #保存文件
# f.save(os.path.join("../file", zip_name))
# #打开文件
# file_zip = zipfile.ZipFile(zip_name_path, 'r')
# # 解压文件
# for file in file_zip.namelist():
#     file_zip.extract(file, "../file")
# # 关闭
# file_zip.close()
# def load_CT(folderName):
#     if os.path.isdir(folderName):
#         imgs, spc, ori, uid = ReadDICOMFolder(folderName)
#         imgs_old, spc_old, ori_old, uid_old = ReadDICOMFolder_old(folderName)
#         imgs_old = np.flip(imgs_old,axis=0)
#         flipped_flag =  np.array_equal(imgs[0],imgs_old[0])
#     else:
#         imgs, spc, ori, uid,itkImage = load_itk(folderName)
#         spc_old,ori_old = spc, ori
#         flipped_flag = itkImage
# #     print imgs.shape
#     time_e = time.time()
#     logger.debug('CT loading finished, time elapse: %s'%(str(time_e-time_s)))
#     return imgs, spc, spc_old, ori_old, uid, flipped_flag
#
#
# def ReadDICOMFolder(folderName, input_uid=None):
#
#     files = os.listdir(folderName)
#     file_paths = [os.path.join(folderName, f) for f in files]
#
#     dcms = []
#     zposes = []
#     for file_path in file_paths:
# #             if file_path[-3:] == 'DCM' or file_path[-3:] == 'dcm':
#         dcm = dicomio.read_file(file_path)
#         zpos = dcm.InstanceNumber
#         zposes.append(zpos)
#         sitk_img = sitk.ReadImage(file_path)
#         img = sitk.GetArrayFromImage(sitk_img)
#         dcms.append(img)
#
#     dcms = np.squeeze(np.array(dcms))
#     zposes = np.array(zposes)
#     zposes_copy = zposes.copy().tolist()
#
#     sorted_dcms = []
#
#     sorted_zposes = sorted(zposes)
#     for z in sorted_zposes:
#         ori_idx = zposes_copy.index(z)
#         sorted_dcms.append(dcms[ori_idx])
#
#     imageRaw = np.array(sorted_dcms)
#
#     uid = dcm.SeriesInstanceUID
#     origin = list(dcm.ImagePositionPatient)
#     origin.reverse
#
#     spc_z = dcm.SliceThickness
#     spc_yx = dcm.PixelSpacing
#     spacing = np.array([spc_z, spc_yx[0], spc_yx[1]])
#     return imageRaw, spacing, np.array(origin),uid
