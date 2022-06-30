import os, xlrd, xlwt, time, json, hashlib, traceback, datetime
import requests, re
from function import get_authorization
from xlwt import *
import pymysql
from config import http_


def _headers():
    if http_.a == 0:
        Authorization = get_authorization.get_Authorization()
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Authorization': Authorization,
            'Referer': 'http://926-web-test.926.net.cn/',
            'Origin': 'http://926-web-test.926.net.cn',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            # 'User-Agent': 'Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome74.0.3729.131 Safari537.36',

        }

    elif http_.a == 1:
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Authorization': Authorization,
            'Referer': 'http://pre-web.926.net.cn/',
            'Origin': 'http://pre-web.926.net.cn',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            # 'User-Agent': 'Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome74.0.3729.131 Safari537.36',

        }
    elif http_.a == 2:
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Authorization': Authorization,
            'Referer': 'http://web.926.net.cn/',
            'Origin': 'http://web.926.net.cn',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            # 'User-Agent': 'Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome74.0.3729.131 Safari537.36',

        }

    return headers


def md5Encode(str_):
    m = hashlib.md5()
    str_ = str(str_)
    m.update(str_.encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()


# 连接数据库
def conn_database():
    connect = pymysql.Connect(
        host='192.168.1.245',
        port=3307,
        user='root',
        passwd='123456',
        db='cloud',
        charset='utf8'
    )
    cursor = connect.cursor()
    # sql = "SELECT * from pc_news"
    # cursor.execute(sql)
    # lgc_sn = cursor.fetchone()
    # print(lgc_sn)
    # n = 1
    # for row in cursor.fetchall():
    #     print("No:%d__%s" % (n,row))
    #     n += 1
    # print('共查找出', cursor.rowcount, '条数据')

    return cursor, connect


# conn_database()
# get token存于token.txt
def get_token(phone, password, *args):
    print(phone)
    if http_.a == 2:
        url = http_.http_login + '/api/v1/erp/account/login'
    else:
        url = http_.http_login + '/api/v1/erp/account/mobile'
    print(url)
    data = 'admin=&appKey=S00101&format=json&openId=&password=%s&phone=%s&sessionKey=&sign=ad1cfca383aa909cea7c0' \
           '763c3414462&signMethod=01&sysTag=S00102&timestamp=15577429794&version=1.0' % (password, phone)
    print(data)
    # data = json.dumps(data)
    print(datetime.datetime.now())
    # todo 登陆云企
    try:
        r = requests.post(url, data=data, headers=_headers())
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(20)
        r = requests.post(url, data=data, headers=_headers())
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
        print('错误信息', traceback.format_exc())
    print(datetime.datetime.now())
    if b['ret'] == 0:
        openid = b['data']['openId']
        token_ = b['data']['sessKey']
        account_sn = b['data']['accountSn']
        # print(token_)
        # print(phone)
        # todo 进入云平台 or 代理交易助手
        if phone == http_.agent_phone:
            print('++++++++++++++++++++++++++++++++++++++++++++++++++')
            url = http_.http_case + "/api/v1/agent/login"  # agent/login
            data = 'accountSn=%s&openId=%s&sign=e48213f4e5575cdc66e3ed76372b7097&sysTag=S00102' % (account_sn, openid)
        else:
            url = http_.http_case + "/api/v1/user/login"  # agent/login
            data = 'accountSn=%s&openId=%s&sessionKey=%s&sign=64d6dc7d4d76bc203babf0faad51ae16&sysTag=S00102' % (
                account_sn, openid, token_)

        try:
            r = requests.post(url, data=data, headers=_headers())
            # 将字符串格式转换为字典
            b = eval(r.text)
            print('==========>>>failed:%s' % b)
        except Exception as e:
            time.sleep(20)
            print('错误信息', traceback.format_exc())
            r = requests.post(url, data=data, headers=_headers())
            # 将字符串格式转换为字典
            b = eval(r.text)
            print('==========>>>failed:%s' % b)
        if b['ret'] == 0:
            token = b['data']['sessionKey']
            # print("++++++++++++++++++")
            print("sessionKey为：", token)
            return token
        else:
            print(b['msg'])
    else:
        print(b['msg'])


# 通过配置文件里的接口名称来获取接口url的函数
# def get_url(api_name):
#     fp = open('D:\HDapi-auto-test\config\API_url.text')
#     # 按行读取接口url配置文件
#     api_infos = fp.readlines()
#     fp.close()
#     # 通过for循环来遍历配置文件里的每一个url，并且返回传入的接口名称相应的url
#     for api in api_infos:
#         # 去除因为读取产生的换行空格等
#         api_f = api.strip(' \r\n\t')
#         api_c = api_f.split('=')
#         if api_name == api_c[0]:
#             return api_c[1]


# 通过传入用例名称的文件和excel页面来读取测试用例
def get_case(filename, sheetname):
    """
    :param filename:接口测试用例文件名
    :param sheetname:接口名称
    :return nor:有效行
    :return table:表对象
    :return nol:有效列
    :return url：API地址
    """
    case_dir = 'E:\sunaw\\HDapi-auto-test\\testcase_excel' + '\\' + filename + '.xlsx'

    datas = xlrd.open_workbook(case_dir)
    table = datas.sheet_by_name(sheetname)
    param_list = table.row_values(4)
    param_list = [i for i in param_list if i != '']
    nor = table.nrows  # 获取有效行
    nol = len(param_list)  # 获取有效列
    url = table.cell_value(3, 1)
    url.replace(" ", "")
    # print(url)
    return nor, table, nol, url


# 获取测试模板信息
def get_testcase_info(filename):
    """:param filename:文件路径
    """
    case_dir = 'D:\\HDapi-auto-test\\testcase_excel' + '\\' + filename + '.xlsx'
    datas = xlrd.open_workbook(case_dir)
    sheet_name = datas.sheet_names()  # 获取所有工作表表名列表

    nor, table, nol, url = get_case(filename, 0)
    for i in range(0, nol):  # 行
        data_ = {}
        for j in range(0, nor - 3):  # 列
            key_ = table.cell_value(0, j)
            print(key_)
            data_[key_] = table.cell_value(i + 1, j)
            print("---------------------------")
            print(data_)
            expect_code = table.cell_value(i + 1, nor - 3)
            expect_message = table.cell_value(i + 1, nor - 2)
            notes = table.cell_value(i + 1, nor - 1)


# 获取测试用例中的所有接口名称,存于列表
def count_apitestcase(filename):
    """
    :param filename:测试用例文件路径
    :return name_list:包含所有接口名称的列表
    """
    data = xlrd.open_workbook(filename)
    name_list = data.sheet_names()
    return name_list


# 将浮点数转换为整数
def float_2_int(num):
    if isinstance(num, float):
        return int(num)
    else:
        return num


# 将最新的用例执行情况存于count.txt
def save_2_count(pass_num, failed_num):
    """
    :param pass_num:用例通过数量
    :param failed_num:用例未通过数量
    """
    p_f_num = "%d_%d" % (pass_num, failed_num)
    f = open('D:\\HDapi-auto-test\\config\\p_f_count.txt', 'r+')
    line = f.read()
    # f.close()
    print("line:%s" % line)
    if line:
        old_pass_num = int(line.split("_")[0])
        old_failed_num = int(line.split("_")[1])
        old_pass_num += pass_num
        old_failed_num += failed_num
        p_f_num = "%d_%d" % (old_pass_num, old_failed_num)
        print(p_f_num)
        f.write(p_f_num)
        f.close()
    else:
        f.write(p_f_num)
        f.close()


# 从count.txt读取用例执行情况数据
def read_from_count():
    f = open('D:\\HDapi-auto-test\\config\\p_f_count.txt', 'r+')
    lines = f.readline()
    if lines:
        old_pass_num = int(lines.split("_")[0])
        old_failed_num = int(lines.split("_")[1])
        return old_pass_num, old_failed_num


# 设置单元格格式
def set_style(style):
    # color_list = ["light_green", "red","yellow"]

    if style == "居中对齐":
        # 创建一个样式(字体居中对齐)--------------------------
        alignment = xlwt.Alignment()
        alignment.horz = alignment.HORZ_CENTER
        alignment.vert = alignment.VERT_CENTER
        style_ = xlwt.XFStyle()
        style_.alignment = alignment
        return style_

    # if style in ["light_green", "red", "ice_blue","gray25"]:
    # 创建一个样式(背景色为[],居中对齐)
    style_ = XFStyle()
    pattern = Pattern()
    alignment = xlwt.Alignment()
    alignment.horz = alignment.HORZ_CENTER
    alignment.vert = alignment.VERT_CENTER
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map[style]  # 设置单元格背景色
    style_.pattern = pattern
    style_.alignment = alignment
    return style_


# 通过xlwt库来设计测试报告并写入excel里面
def write_report():
    # print("-" * 20 + "开始编写测试报告模板" + "-" * 20)
    start_time = time.time()
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('party_building')

    style = set_style("居中对齐")
    light_green_style = set_style("light_green")
    red_style1 = set_style("red")
    ice_blue_style = set_style("ice_blue")
    gray25_style = set_style("gray25")

    # 具体的合并单元格并且写入相应的信息
    name_list = count_apitestcase("E:\sunaw\\HDapi-auto-test\\testcase_excel\party_building.xlsx")
    worksheet.write_merge(0, 1, 0, 7, '测试报告(party_building)', style)
    worksheet.write_merge(0, 2, 12, 12, 'total_result', ice_blue_style)
    worksheet.write(0, 13, "pass", light_green_style)
    worksheet.write(1, 13, "fail", red_style1)
    worksheet.write(2, 13, "unexecuted", gray25_style)
    n = 2
    for i in name_list:
        # print(i)
        N = 2
        # print(n)
        nor, table, nol, url = get_case('party_building', i)
        worksheet.write_merge(n, n + 1, 0, 0, i, style)
        worksheet.write(n, 1, 'notes')
        worksheet.write(n + 1, 1, 'detail')
        n += 2
        param_list = table.row_values(4)
        note_n = param_list.index("notes")
        note_list = table.col_values(note_n)
        # print(note_list)
        note_list = [i for i in note_list if i != '']
        del note_list[0]
        # print(note_list)
        # print(len(note_list))
        for j in note_list:  # 写入用例名称
            # print(n - 2, N, j)
            worksheet.write(n - 2, N, j)
            N += 1

    # report_dir = 'D:\\HDapi-auto-test\\report\\'
    # now = time.strftime('%Y-%m-%d %H:%M:%S')
    # filename = report_dir + now + '_API_test_report.xlsx'
    # filename = report_dir + 'API_test_report.xlsx'
    # workbook.save(filename)
    end_time = time.time()
    spend = (end_time - start_time)
    print("-" * 20 + "编写完毕,耗时%.2fs" % spend + "-" * 20)

    return worksheet, workbook
