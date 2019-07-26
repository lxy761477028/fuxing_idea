
import urllib.request
import requests
import json
import os
#
# url= "http://172.16.100.221:5000/get_file?file_path=/opt/alpha/appdata/autotest/UT/FFRct_Adapters_UT/Data&file_name=4433121_img.zip"
# # file = urllib.request.urlopen(url)
# file = urllib.request.urlretrieve(url, "./hahah")
# # new_filename = "jjjnn" + '.' + "zip"  # 修改了上传的文件名
# # file.save(os.path.join("./", new_filename))
# print(file)

data = {
  "method": "read_dicom",
  "ver": "2.0",
  "requestId": 54321,
  'data':{"ser_id":"1.3.12.2.1107.5.1.4.73757.30000017091200222701600058375",
  	'dicomPath': '/opt/alpha/appdata/autotest/UT/FFRct_Adapters_UT/Data/Li_Yan/'
  }
}
url = r"http://127.0.0.1:7000/"
#
response = requests.post(url, json=data)
# print(response)
#
print(response.text)

# url = r"http://172.16.100.221:5000/get_file?file_path=../file&file_name=1.3.12.2.1107.5.1.4.73757.30000017091200222701600058375_mask.raw"
#
# response = requests.get(url)
# response.raise_for_status()
# playFile = open('RomeoAndJuliet.raw', 'wb')
# for chunk in response.iter_content(100000):
#     playFile.write(chunk)
# playFile.close()



# print(response.text)