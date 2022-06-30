import requests, unittest, os, time, json
from function import public, get_authorization


def test_case(worksheet, workbook, apiname, token):
    print("-" * 50 + "%s" % apiname + "-" * 50)
    pass_num = 0
    faild_num = 0
    ununexecuted_num = 0
    nor, table, nol, url = public.get_case('party_building', apiname)
    Authorization = get_authorization.get_Authorization()
    apiname_list = public.count_apitestcase("E:\sunaw\HDapi-auto-test\\testcase_excel\\party_building.xlsx")
    index = (apiname_list.index(apiname) + 1) * 2 + 1


    param_list = table.row_values(4)
    note_n = param_list.index("notes")
    expect_message_n = param_list.index("expect_message")
    expect_code_n = param_list.index("expect_code")
    param_list = param_list[0:expect_code_n]
    param_list.remove("token")

    # print(param1)
    for i in range(0, nor - 5):  # 行
        data_ = {}
        for j in range(0, nol):  # 列
            key_ = table.cell_value(4, j)
            value_ = table.cell_value(i + 5, j)
            # print(key_)
            if key_ == "token" and value_ == "有效":
                data_[key_] = token
            if key_ in param_list and value_:
                data_[key_] = public.float_2_int(table.cell_value(i + 5, j))
        # print(data_)
        expect_code = table.cell_value(i + 5, expect_code_n)
        expect_message = table.cell_value(i + 5, expect_message_n)
        notes = table.cell_value(i + 5, note_n)

        # 请求头，网站加了登陆验证之后需要在请求头传入Authorization参数
        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': Authorization,
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome74.0.3729.131 Safari537.36',

        }

        # worksheet.write(i + 1, index, notes)
        data = 'id=324&sessionKey=%s&sign=95aba521786b06b057baa0b52fd93dd2' % token
        print(data)
        print("url:%s" % url)
        print("data:%s" % data)
        print("headers:%s" % headers)
        # print(data)
        r = requests.post(url, data=data, headers=headers)
        # 将字符串格式转换为字典
        b = eval(r.text)
        m = b.get('code')
        n = b.get('message')
        k = b.get('data')
        msg = b.get('msg')
        # print(m, n, k,msg)
        red_style = public.set_style("red")
        light_green_style = public.set_style("light_green")
        # 判断接口测试通过与否
        if m == expect_code:
            # print(index,i+2)
            worksheet.write(index, i + 2, 'pass', light_green_style)
            pass_num += 1
            print("==========>>>pass")
        else:
            # print(index,i+2)
            worksheet.write(index, i + 2, 'faild:%s' % b, red_style)
            faild_num += 1
            print("==========>>>failed:%s" % b)
            print(b["msg"])

    # 将通过和失败的数量存入count.txt
    # public.save_2_count(pass_num, faild_num)

    return pass_num, faild_num,ununexecuted_num

#	now = time.strftime('%Y-%m-%d %H_%M_%S')
#	report_dir = 'D:\\person\\learn\\py\\HDapi\\report\\'
#	filename =report_dir + now + 'apiresult.xlsx'
#	workbook.save(filename)
