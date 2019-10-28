import os
import shutil


path = r"E:\fuxing_idea\beifen\8_7"
savepath = r"E:\fuxing_idea\beifen\save_path"

files = os.listdir(path)

print(files)
for i in files:
    lt = i.split("_")
    log_dir = savepath + '/' + lt[0]

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    print(lt)

    if "DWI" in lt:
        zp = path + '/' + i
        shutil.copy(zp, log_dir)

    if "CTA" in lt:
        zp = path + '/' + i
        shutil.copy(zp, log_dir)

