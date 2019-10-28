import os
import time
import shutil
import linecache


i = 1
j = 1
def find_gpu():
    path = r""
    savepath = r""
    log_size = os.path.getsize(path)
    save_log_path = savepath + '/' + "tf_gpu_log"
    if os.path.exists(save_log_path):
        save_log_size = os.path.getsize(save_log_path)
        if log_size > save_log_size:
            shutil.copy(path, savepath)
        if log_size == save_log_size:
            print("ni change")
        if log_size < save_log_size:
            global i
            os.rename(save_log_path, save_log_path + i)
            i +=1

    else:
        shutil.copy(path, savepath)
    print(log_size)
    linecache.checkcache('path')
    time.sleep(0.5)


def find_cpu():
    path = r""
    savepath = r""
    log_size = os.path.getsize(path)
    save_log_path = savepath + '/' + "tf_cpu_log"
    if os.path.exists(save_log_path):
        save_log_size = os.path.getsize(save_log_path)
        if log_size > save_log_size:
            shutil.copy(path, savepath)
        if log_size == save_log_size:
            print("ni change")
        if log_size < save_log_size:
            global j
            os.rename(save_log_path, save_log_path + j)
            j +=1

    else:
        shutil.copy(path, savepath)
    print(log_size)
    linecache.checkcache('path')
    time.sleep(0.5)

#
#
for i in range(100000000):
    find_gpu()
    find_cpu()
#
#


# import time
# def follow(thefile):
#     thefile.seek(0,2)
#     while True:
#         line = thefile.readline()
#         if not line:
#             time.sleep(0.1)
#         continue
#     yield line
# if __name__ == '__main__':
#     logfile = open(r"E:\fuxing_idea\beifen\8_7\1014186_first_BS_brain_rigid_affine_aligned.nii.gz","r")
#     loglines = follow(logfile)
#     for line in loglines:
#         print(line)

# #
#
# logfile='access.log'
# command="tail -f ‘+logfile+'|grep 'timeout'"
# popen=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
# while True:
# line=popen.stdout.readline().strip()
# print line

# import time
# file = open(‘access.log')
# while 1:
# where = file.tell()
# line = file.readline()
# if not line:
# time.sleep(1)
# file.seek(where)
# else:
# print line,