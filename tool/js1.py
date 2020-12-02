# -*- coding: utf-8 -*
import json, os


def path_list(path):
    path_list = []
    image_abpath_files = os.listdir(path)
    image_abpath_files.sort()
    for x in image_abpath_files:
        path_list.append(os.path.join(path, x))
    return path_list


def code_process(train_data, train_label, json_path):
    train_data_list = path_list(train_data)
    train_label_list = path_list(train_label)

    with open(json_path, "r") as f:
        fileJson = json.load(f)
        count_num = len(train_label_list)
        for x in range(count_num):
            json_json = {}
            with open(train_label_list[x], "r") as fs:
                test_lable = str(int(fs.readline().split(",")[1]))
                # if int(test_lable) > 5:
                #     continue
                test_lable = fileJson[test_lable]
                json_json["label"] = test_lable
                json_json["type"] = "classify"
                json_json["content"] = train_data_list[x]

                with open("/home/dataexa/insight-microservice/workspace/labeling/resultSet/24/text_image1.json", "a+") as f:
                    json_json = json.dumps(json_json)
                    f.writelines(json_json)

                    f.writelines('\n')


code_process("/home/dataexa/insight-microservice/workspace/labeling/resultSet/24/garbage/train_data",
             "/home/dataexa/insight-microservice/workspace/labeling/resultSet/24/garbage/train_label",
             "/home/dataexa/insight-microservice/workspace/labeling/resultSet/24/garbage_classify_rule.json")
