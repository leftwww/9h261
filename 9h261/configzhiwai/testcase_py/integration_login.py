from decimal import *

import datetime
import hashlib
import random
import re
import requests
import sys
import time
import traceback
from xlrd import open_workbook
from xlutils.copy import copy

from config import http_
from function import get_authorization, public


def _headers():
    if re.findall('163.177.128.179', http_.http_case):
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

    else:
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

    return headers



def md5Encode(str_):
    m = hashlib.md5()
    str_ = str(str_)
    m.update(str_.encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()


number1 = random.randint(1, 2)
number2 = random.randint(1, 2)
c = random.uniform(1, 3)
price1 = round(c, 2)
d = random.uniform(1, 3)
price2 = round(d, 2)



def implement(url, data, case, *args):
    print(datetime.datetime.now())
    try:
        r = requests.post(url, data=data, headers=_headers())
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        # 重新请求
        time.sleep(20)
        r = requests.post(url, data=data, headers=_headers())
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
        print('错误信息', traceback.format_exc())
    print(datetime.datetime.now())
    try:
        print('列表中信息数量:', b['data']['total'])
        news.append(b['data']['total'])  # 列表中信息数量
    except Exception:
        print('不为列表，信息为空')
        news.append('无')  # 列表中信息数量
    print(case)
    print('contract_save:', contract_save)
    try:
        if len(args) / 2 == 1:
            if b['data']['records'][0][args[0]] == args[1]:
                print('args == 2')
                print('运行结果:%s' % b['msg'])
                news.append(case)
                news.append(url)  # 接口链接
                news.append(b['msg'])  # 执行结果
            else:
                print('校验失败，终止程序')
                sys.exit()
        elif len(args) / 2 == 2:
            if b['data']['records'][0][args[0]] == args[1] and b['data']['records'][0][args[2]] == args[3]:
                print('args == 4')
                print('运行结果:%s' % b['msg'])
                news.append(case)
                news.append(url)  # 接口链接
                news.append(b['msg'])  # 执行结果
            else:
                print('校验失败，终止程序')
                sys.exit()
        elif len(args) / 2 == 3:
            if b['data']['records'][0][args[0]] == args[1] and b['data']['records'][0][args[2]] == args[3] and \
                    b['data']['records'][0][args[4]] == args[5]:
                print('args == 4')
                print('运行结果:%s' % b['msg'])
                news.append(case)
                news.append(url)  # 接口链接
                news.append(b['msg'])  # 执行结果
            else:
                print('校验失败，终止程序')
                sys.exit()
        else:
            print('运行结果:%s' % b['msg'])
            news.append(case)
            news.append(url)  # 接口链接
            news.append(b['msg'])  # 执行结果
    except Exception as e:  # 若相应缓慢，获取信息失败，则重新校验
        print('若相应缓慢，获取信息失败，则重新校验')
        time.sleep(1)
        if len(args) / 2 == 1:
            if b['data']['records'][0][args[0]] == args[1]:
                print('args == 2')
                print('运行结果:%s' % b['msg'])
                news.append(case)
                news.append(url)  # 接口链接
                news.append(b['msg'])  # 执行结果
            else:
                print('校验失败，终止程序')
                sys.exit()
        elif len(args) / 2 == 2:
            if b['data']['records'][0][args[0]] == args[1] and b['data']['records'][0][args[2]] == args[3]:
                print('args == 4')
                print('运行结果:%s' % b['msg'])
                news.append(case)
                news.append(url)  # 接口链接
                news.append(b['msg'])  # 执行结果
            else:
                print('校验失败，终止程序')
                sys.exit()
        elif len(args) / 2 == 3:
            if b['data']['records'][0][args[0]] == args[1] and b['data']['records'][0][args[2]] == args[3] and \
                    b['data']['records'][0][args[4]] == args[5]:
                print('args == 4')
                print('运行结果:%s' % b['msg'])
                news.append(case)
                news.append(url)  # 接口链接
                news.append(b['msg'])  # 执行结果
            else:
                print('校验失败，终止程序')
                sys.exit()
        else:
            print('运行结果:%s' % b['msg'])
            news.append(case)
            news.append(url)  # 接口链接
            news.append(b['msg'])  # 执行结果
    print(datetime.datetime.now())


def file_save(*args):
    # # 4.输出测试报告
    global news, contract_save, goodVOs
    # print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    print(news)
    # news.append(args[0])  # 接口链接
    # news.append(args[1])  # 执行结果
    book = open_workbook('C:\\Users\Zuow\Desktop\\test_file.xlsx')
    wb = copy(book)
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    report_dir = 'E:\sunaw\\HDapi-auto-test\\report\\'
    filename = report_dir + now + 'result.xlsx'
    # 选取表单
    s = wb.get_sheet(0)
    a = 0
    # 写入数据
    while a <= int(len(news) / 4):
        a += 1
        s.write((a + 1), 1, a)  # ID
        s.write((a + 1), 2, news[(a - 1) * 4 - 1])  # 接口名称
        s.write((a + 1), 3, news[(a - 1) * 4 - 2])  # 接口链接
        s.write((a + 1), 4, news[(a - 1) * 4 - 3])  # 执行结果
        s.write((a + 1), 5, news[(a - 1) * 4 - 4])  # 列表中信息数量
        # s.write((a + 1), 13, news[(a - 1) * 5 - 3])  # 备注
        # s.write((a + 1), 22, current_time())  # 时间
        # print(a)
        wb.save(filename)
    news.clear()
    contract_save.clear()
    goodVOs.clear()
    global lucky_day, number1, number2
    lucky_day = random.randint(17, 25)
    number1 = random.randint(5, 10)
    number2 = random.randint(1, 2)




http_login = 'http://163.177.128.179:63201'
http_case = 'http://163.177.128.179:63095'


start_url = 'http://926-web-test.926.net.cn/#/'  # 测试
# start_url = 'http://10.10.1.62:3002/#/'  # 测试


class Integration(object):

    def register(self,*args):
        for i in range(10, 100):
            # print(i)
            phone = '187726079' + str(i)
            print(phone)
            url = http_login + '/api/v1/sms/verify' # 点击注册
            print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
            data = 'action=register&code=1233&phone=%s&sign=89e58d7ad522ea015ee50ae27efb8679'%phone
            try:
                r = requests.post(url, data=data, headers=_headers())
                # 将字符串格式转换为字典
                b = eval(r.text)
                print('==========>>>failed:%s' % b)

                url = http_login + '/api/v1/user/register' # 校验密码
                print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
                data = '&password=e10adc3949ba59abbe56e057f20f883e' \
                       '&phone=' + '%s' % phone + '&registerId=18071adc03625834823&sign=32d9a40b39c8cc6699728b69575b3f27'
                try:
                    r = requests.post(url, data=data, headers=_headers())
                    # 将字符串格式转换为字典
                    b = eval(r.text)
                    print('----------->>>failed:%s' % b)
                except Exception as e:
                    time.sleep(30)
                    r = requests.post(url, data=data, headers=_headers())
                    # 将字符串格式转换为字典
                    b = eval(r.text)
                    print('==========>>>failed:%s' % b)
                    print('错误信息', traceback.format_exc())
            except Exception as e:
                time.sleep(30)
                r = requests.post(url, data=data, headers=_headers())
                # 将字符串格式转换为字典
                b = eval(r.text)
                print('==========>>>failed:%s' % b)
                print('错误信息', traceback.format_exc())
            # try:
            #     print('列表中信息数量:', b['data']['total'])
            #     news.append(b['data']['total'])  # 列表中信息数量
            # except Exception:
            #     print('不为列表，信息为空')
            #     news.append('无')  # 列表中信息数量


def main():

    start_time = datetime.datetime.now()
    print(start_time)

    inte = Integration()
    inte.register()

if __name__ == "__main__":
    main()
