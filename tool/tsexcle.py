# coding=utf-8
import time
import xlrd
import xlwt
from datetime import datetime
from dateutil.relativedelta import relativedelta
from xlrd import xldate_as_datetime, xldate_as_tuple

# 打开文件
data = xlrd.open_workbook('/tool/file/房源委托书管理报表2019.06-2020.10(1)(1)(1).xlsx')
writebook = xlwt.Workbook("/home/dataexa/PycharmProjects/fuxing_idea/tool/file/result.xlsx")
# 查看工作表
#data.sheet_names()
#print("sheets：" + str(data.sheet_names()))

# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name('2019.6-2020.10')

# 打印data.sheet_names()可发现，返回的值为一个列表，通过对列表索引操作获得工作表1
#table1 = data.sheet_by_index(0)
#print(table1)

# 获取行数和列数
# 行数：table.nrows
# 列数：table.ncols
#print("总行数：" + str(table.nrows))
#print("总列数：" + str(table.ncols))

# 获取整行的值 和整列的值，返回的结果为数组
# 整行值：table.row_values(start,end)
# 整列值：table.col_values(start,end)
# 参数 start 为从第几个开始打印，
# end为打印到那个位置结束，默认为none
#print("整行值：" + str(table.row_values(0)))
#print("整列值：" + str(table.col_values(0)))
#委托时间
#commissionTime = table.col_values(0) #委托时间
#client = table.col_values(2) #委托人
#entryTime = table.col_values(4)


# 获取某个单元格的值，例如获取B3单元格值
#cel_B3 = table.cell(3,2).value
#print("第三行第二列的值：" + cel_B3)

def logic(table, beginStart, timeInterval, cycle):
    worksheet = writebook.add_sheet('result')
    worksheet.write(0, 0, label="入职结束时间")
    worksheet.write(0, 1, label="入职起始时间")
    worksheet.write(0, 2, label="人数")
    worksheet.write(0, 3, label="签单数")
    worksheet.write(0, 4, label="平均签单量")
    m = 1
    allDta = []
    nrows = table.nrows
    ncols = table.ncols
    print(nrows)
    print(ncols)
    for i in range(cycle):

        ll = []
        num = []
        total = 0
        timeStart = datetime.strptime(beginStart, "%Y-%m-%d", )
        timeStart = timeStart - relativedelta(months=+i)
        timeEnd = timeStart - relativedelta(months=+1,days=-1)
#        print(timeStart)
#        print(timeEnd)
#
#        print(table.row_values(0))
        for j in range(1, nrows):
            nrowsData = table.row_values(j)

            commissionTime = datetime(*xldate_as_tuple(nrowsData[0], 0)).strftime('%Y-%m-%d')
            commissionTime = datetime.strptime(commissionTime, "%Y-%m-%d", )

            entryTime = datetime(*xldate_as_tuple(nrowsData[3], 0)).strftime('%Y-%m-%d')
            entryTime = datetime.strptime(entryTime, "%Y-%m-%d", )
            timeDifference = entryTime + relativedelta(months=+timeInterval)
            timeDifference = timeDifference - relativedelta(days=+timeInterval)

#            print(entryTime)

            if timeEnd < entryTime < timeStart:
                if entryTime<commissionTime<timeDifference:
                    num.append(nrowsData[1])
                    total +=1


        ll.append(str(timeStart))
        ll.append(str(timeEnd))
        ll.append(len(set(num)))
        ll.append(total)
        print(num)
        if len(set(num)) != 0:
            ll.append(total/len(set(num)))
        else:
            ll.append(0)

        print(ll)
        for n in range(len(ll)):
            worksheet.write(m, n, label=ll[n])
        m += 1
        writebook.save('/home/dataexa/PycharmProjects/fuxing_idea/tool/file/resultTwoM.xlsx')


beginStart = '2020-11-18'
timeInterval = 1
cycle = 10
logic(table, beginStart, timeInterval, cycle)





'''
timeStart = datetime.strptime(timeStart, "%Y-%m-%d", )
print(timeStart)


endtime = timeStart + relativedelta(months=+1)
print(endtime)
'''
