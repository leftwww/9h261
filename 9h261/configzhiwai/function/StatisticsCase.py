import xlrd, sys, os


def statisticsCase(filename):
    """:param filename:要统计的xlsx的路径"""

    chdirUrl = os.getcwd()
    # print(chdirUrl)
    # filename = os.path.join(chdirUrl,"party_building.xlsx")
    # print(filename)
    # filename = "D:\\HDapi-auto-test\\testcase_excel\party_building.xlsx"
    data = xlrd.open_workbook(filename)
    names = data.sheet_names()
    # print(names)
    apiNum = len(names)

    testcaseNum = 0
    actTestcaseNum = 0
    faildNum = 0
    incompleteNum = 0

    for i in names:
        # print(i)
        table = data.sheet_by_name(i)
        value = table.cell_value(3, 1).replace(" ", "")
        if value == "BaseUrl":
            incompleteNum += 1

        ncols = table.ncols  # 列数
        nrows = table.nrows  # 行数
        # print(nrows)
        caseNrows = table.nrows - 5
        testcaseNum += caseNrows
        for k in range(0, ncols):
            if table.cell_value(4, k) == "result":
                resultList = table.col_values(k)
                # print(resultList)
                for j in resultList:
                    if j == "pass":
                        actTestcaseNum += 1
                    if j == "faild":
                        actTestcaseNum += 1
                        faildNum += 1
                        # print(actTestcaseNum)
                break
    coverRate = actTestcaseNum / testcaseNum
    coverRate = format(coverRate, '.1%')

    print("接口数量:%d" % apiNum)
    print("未完成接口数量:%d" % incompleteNum)
    print("测试用例总数:%s" % testcaseNum)
    print("执行用例总数:%s" % actTestcaseNum)
    print("覆盖率:%s" % coverRate)
    print("bug数量:%d" % faildNum)
    print("                     by lcc")
    print("                     2019-4-29")

    os.system("pause")


if __name__ == '__main__':
    statisticsCase("E:\sunaw\\HDapi-auto-test\\testcase_excel\party_building.xlsx")
