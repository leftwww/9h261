import xlwt


def write_report():
    workbook = xlwt.Workbook(encoding='utf-8')
    # 在excel测试报告表格中xx创建项目页面
    worksheet = workbook.add_sheet('party_building')
    # 设置字体格式为居中对齐
    alignment = xlwt.Alignment()
    alignment.horz = alignment.HORZ_CENTER
    alignment.vert = alignment.VERT_CENTER
    style = xlwt.XFStyle()
    style.alignment = alignment

    # 具体的合并哪些单元格并且写入相应的信息
    worksheet.write_merge(0, 0, 0, 7, '测试报告(housemanage)', style)
    worksheet.write_merge(1, 10, 0, 0, 'house_manage', style)
    worksheet.write_merge(1, 2, 1, 1, 'insethouse', style)
    worksheet.write_merge(3, 4, 1, 1, 'updatehouse', style)
    worksheet.write_merge(5, 6, 1, 1, 'deletehouse', style)
    worksheet.write_merge(7, 8, 1, 1, 'gethouse', style)
    worksheet.write_merge(9, 10, 1, 1, 'updatehouse', style)
    worksheet.write_merge(1, 2, 11, 11, 'total_result', style)
    worksheet.write(1, 2, 'notes')
    worksheet.write(2, 2, 'detail')
    worksheet.write(3, 2, 'notes')
    worksheet.write(4, 2, 'detail')
    worksheet.write(5, 2, 'notes')
    worksheet.write(6, 2, 'detail')
    worksheet.write(7, 2, 'notes')
    worksheet.write(8, 2, 'detail')
    worksheet.write(9, 2, 'notes')
    worksheet.write(10, 2, 'detail')
    worksheet.write(1, 12, 'pass')
    worksheet.write(1, 13, 'faild')
    # 最后返回worksheet,workbook两个参数，因为在测试测试用例和运行文件中需要用到的两个参数
    return worksheet, workbook
