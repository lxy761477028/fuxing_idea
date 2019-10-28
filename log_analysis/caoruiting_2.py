import os
import json
import pandas as pd

path1 = r"E:\fuxing_idea\log_analysis\log\20190814\debug.log.1"
path2 = r"E:\fuxing_idea\log_analysis\log\20190814\debug.log"
path3 = r"E:\fuxing_idea\log_analysis\log\220\debug.log"
savepath = r"E:\fuxing_idea\log_analysis\log\20190814\debug.csv"
file1 = open(path1)
file2 = open(path2)
# file3 = open(path3)
i = 0
msg_list = []
for line in file1:
    if i <=10000000:
        try:
            data = json.loads(line)

            i +=1
            # print(i)
            msg = data["log_msg"]
            if msg.startswith("TimeDuration"):
                print(msg)
                msg_list.append(msg)
        except:
            print(i)
for line in file2:
    if i <=10000000:
        try:
            data = json.loads(line)

            i +=1
            # print(i)
            msg = data["log_msg"]
            if msg.startswith("TimeDuration"):
                print(msg)
                msg_list.append(msg)
        except:
            print(i)

# for line in file3:
#     if i <=10000000:
#         try:
#             data = json.loads(line)
#
#             i +=1
#             # print(i)
#             msg = data["log_msg"]
#             if msg.startswith("TimeDuration"):
#                 print(msg)
#                 msg_list.append(msg)
#         except:
#             print(i)

print(len(msg_list))
# type_list = []

serid_lt = []
type_lt = []
time_lt = []

for i in range(len(msg_list)):
    msg = msg_list[i]
    ll = msg.split(" ")
    serid_lt.append(ll[1])
    type_lt.append(ll[2])
    time_lt.append(ll[3])

print(len(serid_lt))
print(len(type_lt))
print(len(time_lt))

test_dict = {"serid": serid_lt,
             "type": type_lt,
             "time": time_lt,
             }

#
test_dict_df = pd.DataFrame(test_dict, columns=["serid", "type", "time"])
test_dict_df.to_csv(savepath, index=False, header=True,encoding="utf_8_sig")


    # if ll[2] not in type_list:
        # type_list.append(ll[2])

    # if "LungSeg-LungSegPrediction" in ll:
    #     pass
    # if "LungSeg-StageOneLungSegPrediction" in ll:
    #     pass
    # if "LungLeaf-FissureSegmentation-MergeResult" in ll:
    #     pass
    # if "LungLeaf-FissureSegmentation-PatchPrediction" in ll:
    #     pass
    # if "LungLeaf-FissureSegmentation-SlidingWindow" in ll:
    #     pass

    # for i in type_list:

# print(type_list)


