import xlrd
import xlwt
from tools.os import os_tool


def write_excel(file_name,data_title,data_list,encoding='utf-8'):
    # 创建workbook和sheet对象 注意Workbook的开头W要大写
    workbook = xlwt.Workbook(encoding=encoding)
    # 添加一个名为sheet1的表
    sheet1 = workbook.add_sheet('sheet1', cell_overwrite_ok=True)

    # 向表头写入数据
    for i in range(len(data_title)):
        sheet1.write(0, i, data_title[i])

    # 向sheet写入数据
    for i in range(len(data_list)):
        for j in range(4):
            sheet1.write(i + 1, j, data_list[i][j])

    # 保存数据到‘Workbook2.xls’文件中
    workbook.save(file_name)
    print('创建execel完成！')

def _get_excel_dict(file):
    data = []
    wb = xlrd.open_workbook(filename=file)  # 打开文件
    # print(wb.sheet_names())  # 获取所有表格名字

    sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格
    # print(sheet1)
    # print(sheet1.name, sheet1.nrows, sheet1.ncols)

    for i in range(1, sheet1.nrows):
        # l.append(sheet1.row_values(i))
        d = {}
        for j in range(sheet1.ncols):
            d[sheet1.row_values(0)[j]] = sheet1.row_values(i)[j]
        data.append(d)
    # print(l)
    return data


def _get_excel_list(file):
    data = []  # 声明变量
    wb = xlrd.open_workbook(filename=file)  # 打开文件
    sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格sheet
    for i in range(1, sheet1.nrows):  # 循环行
        data.append(sheet1.row_values(i))  # 获取每行内容 并 添加进l
    return data

def _get_excel_ids(excel_list):
    ids_list = []
    for i in range(len(excel_list)):
        # 删除excel_list中每个小list的最后一个元素,并赋值给ids_pop
        ids_pop = excel_list[i].pop(0)
        # 将ids_pop添加到 ids_list 里面
        ids_list.append(ids_pop)
    return ids_list

def get_test_case(file):
    root_path = os_tool.get_root_path()
    data = {}
    case_list=_get_excel_list(root_path+file)
    case_ids=_get_excel_ids(case_list)
    data[0]=case_ids
    data[1]=case_list
    return data

if __name__ == '__main__':
    data = get_test_case("C:/softwareData/PycharmProjects/s00-wuling/documents/user/注册接口sign_up.xlsx")
    print(data[0])
    print(data[1])
