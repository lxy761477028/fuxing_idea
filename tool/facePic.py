import os
import shutil

path = "/home/dataexa/PycharmProjects/fuxing_idea/tool/file/lfw"

lsdir = os.listdir(path)



for i in lsdir:
    pathDir = path + "/" + i
    picDir = os.listdir(pathDir)
    if len(picDir) != 2:
        shutil.rmtree(pathDir)
        print(len(picDir))




