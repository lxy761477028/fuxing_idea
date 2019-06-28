#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect(host="172.16.100.221", port=2009, user="root",
                     password="1qaz2wsx", database="ring_integration")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT * from t_study_pacs_info")

# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print("Database version : %s " % str(data))

# 关闭数据库连接
db.close()