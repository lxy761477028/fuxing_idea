import xlwt
import xlrd
import pandas

from matching import mine

z_scope = 2   #z轴浮动次数
z_size = 2  #z轴浮动大小
multiple = 1  #半径放大倍数
percent = 0.4  #匹配率

#读取文件
def read_excle(path,path_answer):
    work_book = xlrd.open_workbook(path)
    work_sheet = work_book.sheets()[0]
    answer_sheet = pandas.read_csv(path_answer)
    nrows = work_sheet.nrows
    ncols = work_sheet.ncols
    answer_nrows = len(answer_sheet)

    return work_sheet,answer_sheet,nrows,ncols,answer_nrows


#创建写入文件对象并写入表头
def write_excel_top(work_sheet,savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('Sheet0', cell_overwrite_ok=True)
    for n in range(len(work_sheet.row_values(0))):
        sheet.write(0, n, work_sheet.row_values(0)[n])
    book.save(savepath)
    return book,sheet


def write_answer(imgDataList,work_list,answer_list,z_scope,z_size,i):
    json_str = "{\"x\":%2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
        float(work_list[4]), float(work_list[5]), float(work_list[3]), float(work_list[6]) * multiple,
        float(work_list[6]) * multiple)

    answer_json_str = "{\"x\":%.2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
        float(answer_list[4]), float(answer_list[3]), float(answer_list[2]), float(answer_list[5]) * multiple,
        float(answer_list[5]) * multiple)
    answer_img_num = int(answer_list[0]) + 100000
    js_answer = {
        "imgNo": answer_img_num,
        "imgData": answer_json_str
    }
    js = {
        "imgNo": i + 1,
        "imgData": json_str
    }
    # print(answer_json_str)
    imgDataList.append(js)
    imgDataList.append(js_answer)
    for g in range(z_scope):
        json_str_less = "{\"x\":%2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
            float(work_list[4]), float(work_list[5]), float(work_list[3]) + (-g - 1) * z_size, float(work_list[6]) * multiple,
            float(work_list[6]) * multiple)
        js_less = {
            "imgNo": -g - 1,
            "imgData": json_str_less
        }
        json_str_than = "{\"x\":%2f,\"y\":%2f,\"z\":%2f,\"mind\":%2f,\"maxd\":%2f,\"direction\":\"{\"x\":0.0,\"y\":0.0,\"z\":0}\"}" % (
            float(work_list[4]), float(work_list[5]), float(work_list[3]) + (g + 1) * z_size, float(work_list[6]) * multiple,
            float(work_list[6]) * multiple)
        js_than = {
            "imgNo": g + 1,
            "imgData": json_str_than
        }
        imgDataList.append(js_less)
        imgDataList.append(js_than)

    return imgDataList,answer_img_num


def cluster_excle(path,path_answer,savepath):
    work_sheet, answer_sheet, nrows, ncols, answer_nrows = read_excle(path,path_answer)
    book,sheet = write_excel_top(work_sheet,savepath)
    for i in range(1, nrows):
        imgDataList = []
        has_answer = 0
        work_list = work_sheet.row_values(i)

        #写入原始数据
        for n in range(len(work_list)):
            sheet.write(i, n, work_list[n])

        #遍历答案，写入结果
        for j in range(1, answer_nrows):
            answer_list = answer_sheet.loc[j]
            if answer_list[1] == work_list[2]:
                has_answer = 1
                #构造请求参数
                imgDataList, answer_img_num= write_answer(imgDataList,work_list,answer_list,z_scope,z_size,i)

                roundness = {
                    "imgDataList": imgDataList,
                    "imgType": "ELLIPSE",
                    "percent": percent
                }
                print(roundness)
                f = mine(roundness)
                info = f['info']["list"][0]
                if answer_img_num in info:
                    for n in range(len(work_list)):
                        sheet.write(i, n, work_list[n])
                    sheet.write(i, len(work_list) - 0, 1)

                    print(f)
                    print(1)
                    print("*" * 50)
                    book.save(savepath)
                    imgDataList = []
                    break
                else:
                    sheet.write(i, len(work_list) - 0, 0)
                    print(f)
                    print(0)
                    print("@" * 50)
                    book.save(savepath)
                    imgDataList = []
                    continue
        if has_answer == 0:
            sheet.write(i, len(work_list) - 0, "无")
            print("无")
            print("#" * 50)

    book.save(savepath)


path1 = r"E:\first\cluster\ccyy\1.xlsx"
path2 = r"E:\first\cluster\ccyy\2.xlsx"
path3 = r"E:\first\cluster\ccyy\3.xlsx"
path4 = r"E:\first\cluster\ccyy\B-待审核-禅医-CT肺结节-运营(2018-08-31--2018-09-28).xlsx"
path_answer = r"E:\first\cluster\ccyy\answer.csv"
path_save1 = r"E:\first\cluster\ccyy\readwrite_1.xls"
path_save2 = r"E:\first\cluster\ccyy\readwrite_2_1.xls"
path_save3 = r"E:\first\cluster\ccyy\readwrite_3_1.xls"
path_save4 = r"E:\first\cluster\ccyy\read_write_B).xls"


cluster_excle(path4,path_answer,path_save4)

