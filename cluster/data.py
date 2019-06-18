

import json
import pandas as pd

from matching import mine


path = r"E:\first\cluster\2019_6_12\noduleCls.csv"

df = pd.read_csv(path, encoding="gbk")

serial_number = df["xulie"]
data_list_x = df["x"]
data_list_y = df["y"]
data_list_z = df["z"]
data_list_mind = df["mind"]
data_list_maxd = df["maxd"]

print(type(data_list_x))
print(data_list_x)