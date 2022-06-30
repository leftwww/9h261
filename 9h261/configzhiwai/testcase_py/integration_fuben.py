import datetime
import hashlib
import random
import re
import sys
import time
import traceback
from decimal import *

import requests
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


# 0 为合同id    1为合同账号CT  2.为发货单号DF  3.发货单ID 4 出货单ID 5为出货单号DO  6 退改申请id
# 7 为再次发起的发货单号DF  8.再次发起发货单ID  9 出货单ID 10为出货单号DO   11 退改申请id
# 12 供应寄票单 id   13 供应寄票编号  # 14 代理寄票id  15 代理寄票编号 16 付款编码 17付款单id
contract_save = []  # ID 编号列表

applySn_list = []  # 用户存放创建合同时的编号 CR

# 0，1 为合同商品ID   2，3 为出货时商品id
goodVOs = []  # 商品id列表
news = []  # 用例存放列表
user_id = []  # 用于存放用户id   0 代理id  1 采购id  2.销售 id
open_id = []  # 用于存放 open id
accountSn_list = []  # 用于存放accountSn
lucky_day = random.randint(3, 10)

signPersonAccount_Id = []


# session_list = []  # sessionKey存放列表 0 供应 1 采购 2 代理

def md5Encode(str_):
    m = hashlib.md5()
    str_ = str(str_)
    m.update(str_.encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()


number1 = random.randint(10, 30)
number2 = random.randint(10, 30)
# c = random.uniform(1, 3)

c = random.randint(10, 30)  # 整数
price1 = round(c, 2)
# d = random.uniform(1, 3)

d = random.randint(1, 3)  # 整数
price2 = round(d, 2)


def goods_iofo():  # 随机金额，数量 商品信息
    # global number2,number1
    e = number1 * price1
    f = number2 * price2
    amount1 = round(e, 2)
    amount2 = round(f, 2)
    totalAmount = amount1 + amount2
    amount_1 = Decimal(str(amount1)).quantize(Decimal('0.00'))
    amount_2 = Decimal(str(amount2)).quantize(Decimal('0.00'))
    total_Amount = Decimal(str(totalAmount)).quantize(Decimal('0.00'))

    return number1, number2, price1, price2, amount_1, amount_2, total_Amount


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
    print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
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
    lucky_day = random.randint(3, 10)
    number1 = random.randint(10, 30)
    number2 = random.randint(2, 3)


class Integration(object):

    # 发起合同之选择代理方
    def a001_agent_page(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/agent/page'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        # session_list.append(token)
        data = 'current=1&sessionKey=%s&sign=8af9f25ad2ed806de5160c29c1044913&size=10' % token
        # print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        try:
            r = requests.post(url, data=data, headers=_headers())
            # 将字符串格式转换为字典
            b = eval(r.text)
            print('==========>>>failed:%s' % b)
        except Exception as e:
            time.sleep(30)
            r = requests.post(url, data=data, headers=_headers())
            # 将字符串格式转换为字典
            b = eval(r.text)
            print('==========>>>failed:%s' % b)
            print('错误信息', traceback.format_exc())
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量
        id = b['data']['records'][0]['id']
        account_sn = b['data']['records'][0]['accountSn']
        print('id', id)
        user_id.append(id)
        accountSn_list.append(account_sn)
        print('运行结果:%s' % b['msg'])
        news.append('发起合同之选择代理方')
        news.append(url)  # 接口链接
        news.append(b['msg'])  # 执行结果

    # 发起合同之选择合作方
    def a002_agent_page(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/partner/list'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        # session_list.append(token)
        data = 'current=1&sessionKey=%s&sign=c3269920a274a414c84a6a35ec9be24b&size=10&type=1' % token
        # print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
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
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量
        id = b['data'][0]['openId']
        print('id', id)
        open_id.append(id)
        print('运行结果:%s' % b['msg'])
        news.append('发起合同之选择合作方')
        news.append(url)  # 接口链接
        news.append(b['msg'])  # 执行结果

    # 发起合同之查看申请信息（获取用户信息）
    def a003_party_info(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/third/party/info'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        # session_list.append(token)
        data = 'firstRole=3&openId=%s&sessionKey=%s&sign=409d21cf025e902a7d55ea94bdea7ae0' % (open_id[0], token)
        # print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
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
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量
        id_1 = b['data']['firstPartyVO']['id']
        id_2 = b['data']['thirdPartyVO']['id']
        # print('id', id)
        user_id.append(id_1)
        user_id.append(id_2)
        print('运行结果:%s' % b['msg'])
        news.append('发起合同之选择合作方')
        news.append(url)  # 接口链接
        news.append(b['msg'])  # 执行结果

    # 提交一份新的合同
    def a004_contract_save(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/save'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        print(token)
        # firstPartyId:甲方采购商企业id
        # secondPartyId：乙方企业id
        # thirdPartyId：丙方企业id
        print(user_id)
        print(goodVOs)
        number1, number2, price1, price2, amount_1, amount_2, total_Amount = goods_iofo()
        print('number1, number2, price1, price2, amount_1, amount_2, total_Amount', number1, number2, price1, price2,
              amount_1, amount_2, total_Amount)
        # data = 'accountPeriodDayNum=' + '%s' % lucky_day + '&accountPeriodId=6&contractNumber=%E5%95%8A%E8%89%B2%E7%9A%84%E6%97%A5%E6%96%B' \
        #                                                    '9%E6%8F%90%E4%BE%9B%E5%90%97&contractPhoto=https%3A%2F%2Fsunawtest.oss-cn-shenzhen.aliyuncs.com%2Fjiue' \
        #                                                    'rliu%2Ftest%2Fe16ecb79bf7912edd740182fc42a9b0d.png&firstPartyId=' + '%s' % user_id[1] + '&firstRole=3&goodDTOs=%5B%7B%22goodId%' \
        #                 '22%3A0%2C%22model%22%3A%22%E5%8F%91%E7%94%B5%22%2C%22name%22%3A%22%E5%8F%91%E7%94%B5%22%2C%22number%22%' \
        #                 '3A1%2C%22totalAmount%22%3A%221.00%22%2C%22unit%22%3A%221%22%2C%22unitPrice%22%3A1%7D%5D&id=&' \
        #                 'secondPartyId=' + '%s' % user_id[0] + '&' + 'sessionKey=' + '%s' % token + '&sign=58c8c06198152525831af3fbc5b590fd&thirdPartyId=' + '%s' % \
        #        user_id[
        #            2] + '&totalAmount=%s' % total_Amount

        data = 'accountPeriodDayNum=' + '%s' % lucky_day + '&accountPeriodId=0&contractNumber=yshtbh333&' \
                                                           'contractPhoto=https%3A%2F%2Fjiuerliu.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Fprod_pre%2F625b4822e90d95601e40dcdf7335b7ac.jpg' \
                                                           '%2Chttps%3A%2F%2Fjiuerliu.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Fprod_pre%2F2720b2e1f847c389f13020cb4d7e9f68.jpg' \
                                                           '%2Chttps%3A%2F%2Fjiuerliu.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Fprod_pre%2F191d99318f24860e5263b84b279f2729.jpg&' \
                                                           'deliveryType=2&firstPartyContacts=%E4%B8%9C%E6%96%B9r&firstPartyId=' + '%s' % \
               user_id[1] + '&' \
                            'firstPartyPhone=%E4%B8%9C%E6%96%B9fs&firstPaymentType=10&firstRole=1&goodDTOs=%5B%7B%22goodId%22%3A0%2C%22model%22%3A%22%22%2C%22name%22%3A%22%E5%8F%91%E7%94%B5%E6%9C%BA%22%2C%22number%22%3A' + '%s' % number1 + '%2C%22' \
                                                                                                                                                                                                                                                'totalAmount%22%3A%22' + '%s' % amount_1 + '%22%2C%22unit%22%3A%22%E4%B8%AA%22%2C%22unitPrice%22%3A' + '%s' % price1 + '%7D%2C%7B%22goodId%22%3A0%2C%22model%22%3A%22' + 'TF-i' + '%22%2C%22' \
                                                                                                                                                                                                                                                                                                                                                                                                                                  'name%22%3A%22%E5%8F%91%E7%94%B5%E6%9C%BA%E6%94%AF%E6%9E%B6%22%2C%22number%22%3A' + '%s' % number2 + '%2C%22totalAmount%22%3A%22' + '%s' % amount_2 + '%22%2C%22' \
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        'unit%22%3A%22%E4%B8%AA%22%2C%22unitPrice%22%3A' + '%s' % price2 + '%7D%5D&' + 'id=&protocolNumber=xybh&protocolSignTimeStr=2019-07-13&receiptTerm=&secondAcceptanceDraftTimeType=&secondPartyId=' + '%s' % \
               user_id[
                   0] + '&secondPaymentType=' + '&sessionKey=' + '%s' % token + '&sign=746f3757a6b374d7423794af71322060&sysTag=S00102&thirdPartyContacts=%E5%A4%A9%E6%B2%B3r&thirdPartyId=' + '%s' % \
               user_id[
                   2] + '&thirdPartyPhone=%E5%A4%A9%E6%B2%B3fs&thirdReceiptTimeNum=&thirdReceiptTimeType=' + '&totalAmount=%s' % total_Amount

        # data = accountPeriodDayNum=' + '%s' % lucky_day + '&accountPeriodId=6&contractNumber=%E5%8E%9F%E5%A7%8B%E5%90%88%E5%90%8C%E7%BC%96
        # %E5%8F%B7&contractPhoto=https%3A%2F%2Fsunawtest.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Ftest%2F6715c6adb51
        # a784158ea98a881951df8.png&deliveryType=2&firstPartyContacts=%E4%B8%9C%E6%96%B9R&firstPartyId=' + '%s' % user_id[1] + '&firstParty
        # Phone=%E4%B8%9C%E6%96%B9FS&firstPaymentType=10&firstRole=3&goodDTOs=%5B%7B%22goodId%22%3A0%2C%22model%22%3A
        # %227%22%2C%22name%22%3A%227%22%2C%22number%22%3A' + '%s' % number1 + '%2C%22totalAmount%22%3A%2249.00%22%2C%22unit%22%3A%227%22%
        # 2C%22unitPrice%22%3A7%7D%5D&id=&protocolNumber=1&protocolSignTimeStr=2019-10-01&receiptTerm=&secondAcceptanceDraftTimeType
        # =&secondPartyId=1&secondPaymentType=&sessionKey=dfb1e52fed3384ee277a4c05e11e67f3&sign=98637803
        # 9490b4c20526643bc14a513d&sysTag=S00102&thirdPartyContacts=%E5%A4%A9%E6%B2%B3R&thirdPartyId=78&thirdPartyPhone
        # =%E5%A4%A9%E6%B2%B3FS&thirdReceiptTimeNum=&thirdReceiptTimeType=&totalAmount=49.00
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '提交一份新的合同')

    # 合同全部列表
    def a005_wait_audit_page(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/wait/audit/page'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=fcf1c92f44e77a87572b2cbe05ff9675&size=10&sortType=2&startTime=' % token
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
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
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量
        if b['data']['records'][0]['state'] == 1:
            id = b['data']['records'][0]['id']
            print('id', id)
            contract_save.append(id)
            print('运行结果:%s' % b['msg'])
            news.append('合同申请全部列表')
            news.append(url)  # 接口链接
            news.append(b['msg'])  # 执行结果
        else:
            print('校验失败，终止程序')
            sys.exit()

    # 获取商品id
    def a006_contract_info(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/info'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        data = 'id=%s&sessionKey=%s&sign=06be63bfe5257dc0e7cc32ecff7b882d' % (contract_save[0], token)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
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
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量

        goodVOs.append(b['data']['goodVOs'][0]['goodId'])
        print('运行结果:%s' % b['msg'])
        news.append('合同申请全部列表,获取商品id')
        news.append(url)  # 接口链接
        news.append(b['msg'])  # 执行结果

    # 获取授权代表id
    def a0071_person_list(self, *args):
        url = http_.http_case + '/api/v1/esign/authentication/account/person/list'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        print(contract_save[0])
        data = 'sessionKey=%s&sign=07bbe171ec358a573a2831490813bf5d&sysTag=S00102' % (token)
        # # print(data)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
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
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量
        for i in b['data']:
            print(i['mobile'])
            if i['mobile'] == '13135654887' or i['mobile'] == '13751799037':
                signPersonAccount_Id.append(i['id'])
        print('运行结果:%s' % b['msg'])
        news.append('合同申请全部列表,获取商品id')
        news.append(url)  # 接口链接
        news.append(b['msg'])  # 执行结果

    # 授权代表签署
    def a0072_representative_sign(self, *args):
        url = http_.http_case + '/api/v1/contract/launch/legal/representative/sign'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        print(contract_save[0])
        data = 'sessionKey=%s&code=qweras&id=%s' % (token, contract_save[0])
        # # print(data)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        implement(url, data, '合同申请 签审新建合同')

    # 签审新建合同
    def a007_contract_examine(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/examine'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        print(contract_save[0])
        data = 'code=666666&id=%s&sessionKey=%s&sign=4d235957be706d7e5a02be73e6057447&sysTag=S00102' % (
            contract_save[0], token)
        # # print(data)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '合同申请 签审新建合同')

    # 合同申请 合作方法定代表签署合同
    def a01991_contract_sign(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/receive/legal/representative/sign'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.purchaser_phone, md5Encode(123456))
        print(signPersonAccount_Id[0])
        data = 'id=%s&sessionKey=%s&sign=4d235957be706d7e5a02be73e6057447&signPersonAccount_Id=%s' % (
            contract_save[0], token, signPersonAccount_Id[0])
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '合同申请 收到方签审合同')

    # 合同申请 收到方签审合同
    def a0199_contract_agree(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/agree'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.purchaser_phone, md5Encode(123456))
        data = 'code=666666&id=%s&sessionKey=%s&sign=4d235957be706d7e5a02be73e6057447&sysTag=S00102' % (
            contract_save[0], token)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '合同申请 收到方签审合同')

    # 合同申请 代理方法定代表签署合同
    def a02001_agent_representative(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/agent/contract/legal/representative/sign'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.agent_phone, md5Encode(123456))
        data = 'id=%s&sessionKey=%s&sign=4d235957be706d7e5a02be73e6057447&signPersonAccount_Id=%s' % (
            contract_save[0], token, signPersonAccount_Id[0])
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '合同申请 代理方法定代表签署合同')

    # 合同申请 代理方签审合同
    def a0200_agent_contract_agree(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/agent/contract/agree'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.agent_phone, md5Encode(123456))
        data = 'code=666666&id=%s&sessionKey=%s&sign=4d235957be706d7e5a02be73e6057447&sysTag=S00102' % (
            contract_save[0], token)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '合同申请 代理方签审合同')

    # 合同申请 代理方查看签审后的合同列表
    def a0201_agent_contract_agree(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/agent/contract/page'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.agent_phone, md5Encode(123456))
        data = 'current=1&endTime=&keyWord=&sessionKey=%s&sign=51d07205dcfce27d6084a87ae528b7d0&size=10&startTime=&state=' % (
            token)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '合同申请 代理方查看签审后的合同列表', 'id', contract_save[0], "state", 8)

    # 合同申请 代理方查看签审后的合同（获取合同编号）详情
    def a0202_agent_contract_info(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/agent/contract/info'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.agent_phone, md5Encode(123456))
        data = 'id=%s&sessionKey=%s&sign=a08b3efeccae80824de7bc158b287768' % (contract_save[0], token)
        print(data)
        print('url:%s' % url)
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
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量
        if b['data']['id'] == contract_save[0]:
            print(b['data']['contractSn'])
            contract_save.append(b['data']['contractSn'])
            goodVOs.pop()
            goodVOs.append(b['data']['goodVOs'][0]['goodId'])
            goodVOs.append(b['data']['goodVOs'][1]['goodId'])
            print('运行结果:%s' % b['msg'])
            news.append('合同申请 代理方查看签审后的合同（获取合同编号）详情')
            news.append(url)  # 接口链接
            news.append(b['msg'])  # 执行结果
        else:
            print('校验失败，终止程序')
            sys.exit()

    # 发货申请 销售方选泽发货单位
    def a0205_partner_page(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/apply/partner/page'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        data = 'current=1&sessionKey=%s&sign=6b3b3e80b00c995f59caf75b0f0a5aee&size=10' % token
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '发货申请 销售方选泽发货单位')

    # 发货申请 销售方选泽合同
    def a0206_contract_page(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/apply/contract/page'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        data = 'companyId=' + '%s' % user_id[
            1] + '&current=1&sessionKey=%s&sign=f3505f4c6160c33bf866a976a250546b&size=10' % token
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '发货申请 销售方选泽发货单位')

    # 发货申请 销售方发起发货申请
    def a0207_invoice_apply_save(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/apply/save'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        number1, number2, price1, price2, amount_1, amount_2, total_Amount = goods_iofo()
        print(number1)
        print(number2)
        # number_1 = number1 - 3
        # number_2 = number2 - 5
        number_1 = number1 - 0
        number_2 = number2 - 0
        print(number_1)
        print(number_2)
        totalAmount1 = price1 * number1 + price2 * number2
        totalAmount = Decimal(str(totalAmount1)).quantize(Decimal('0.00'))
        # TotalAmount = Decimal(str(totalAmount)).quantize(Decimal('0.00'))

        data = 'saveContractApplyDTO=%7B%22id%22%3A0%2C%22supplierServiceChargeCoefficient%22%3A' + '0.3' + \
               '%2C%22saveContractApplyGoodListDTOList%22%3A%5B%7B%22number%22%3A' + '%s' % number_1 + '%2C%22id%22%3A0%2C%22contractGoodId%22%3A' + '%s' % \
               goodVOs[
                   0] + '%7D%2C%7B%22number%22%3A' + '%s' % number_2 + '%2C%22id%22%3A0%2C%22contractGoodId%22%3A' + '%s' % \
               goodVOs[1] + '%7D%5D%2C%22totalAmount%22%3A' + '%s' % totalAmount + '%2C%22contractSn%22%3A%22' + '%s' % \
               contract_save[1] + '%22%7D&' + 'sessionKey=%s&sign=956eddba042c83f4d275c3ae8596f846' % token
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '发货申请 销售方发起发货申请')

    # 发货申请 查看发起发货申请后的发货单（并获取货单号）
    def a021_supplier_page(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/apply/supplier/page'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=522604d757df30904b387261b18cb037&startTime=&state=0' % (
            token)
        print(data)
        print('url:%s' % url)
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
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量
        if contract_save[1] == b['data']['records'][0]['contractSn']:
            contract_save.append(b['data']['records'][0]['invoiceApplySn'])
            contract_save.append(b['data']['records'][0]['id'])
            print('运行结果:%s' % b['msg'])
            news.append('发货申请 查看发起发货申请后的发货单（并获取货单号）')
            news.append(url)  # 接口链接
            news.append(b['msg'])  # 执行结果
        else:
            print('校验失败，终止程序')
            sys.exit()
        # implement(url, data, '合同申请 发起合同之选择代理方', 'contractSn', contract_save[1])

    # 发货申请 采购方同意发货申请
    def a034_purchaser_agree(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/apply/purchaser/agree'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.purchaser_phone, md5Encode(123456))
        data = 'id=%s&sessionKey=%s&sign=b106bd1597f129223891e2776c2b42a3' % (contract_save[3], token)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '发货申请 采购方同意发货申请')

    # # 发货申请 采购方查看预计减少额度
    # def a0351_estimate_quota(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/quota/estimate/quota/change/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.purchaser_phone, md5Encode(123456))
    #     data = 'current=1&listType=2&sessionKey=%s&size=10' % (token)
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '发货申请 采购方查看预计减少额度', 'invoiceApplySn', contract_save[2])

    # 发货申请 代理方同意发货申请
    def a035_agent_agree(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/apply/agent/agree'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.agent_phone, md5Encode(123456))
        data = 'id=%s&sessionKey=%s&sign=78eac00f7ba9da1cd2d2885e0029bbd1' % (contract_save[3], token)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '发货申请 代理方同意发货申请')

    # 销售出货 销售方查看出货单信息（获取出货单id 单号）
    def a082_supplier_page(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/supplier/page'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=9ac74c0be92bc6441de1dc8d7871b7d4&startTime=&state=0' % (
            token)
        print(data)
        print('url:%s' % url)
        # implement(url, data, '合同申请 发起合同之选择代理方', 'invoiceApplySn', contract_save[7], 'state', 1)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
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
        try:
            print('列表中信息数量:', b['data']['total'])
            news.append(b['data']['total'])  # 列表中信息数量
        except Exception:
            print('不为列表，信息为空')
            news.append('无')  # 列表中信息数量
        print('销售出货 销售方查看出货单信息（获取出货单id 单号）')
        # 出货单状态 1.待出货2.待收货（供应商已出货）3.待品检（采购商已收货）4.待入库（采购商已品鉴）5.已入库
        print(b['data']['records'][0]['invoiceApplySn'])
        print(type(b['data']['records'][0]['invoiceApplySn']))
        print(contract_save[2])
        print(b['data']['records'][0]['state'])
        if b['data']['records'][0]['invoiceApplySn'] == contract_save[2] and b['data']['records'][0]['state'] == 1:
            # print('+++++')
            contract_save.append(b['data']['records'][0]['id'])
            contract_save.append(b['data']['records'][0]['invoiceSn'])
            print(contract_save)
            print('运行结果:%s' % b['msg'])
            news.append('销售出货 销售方查看出货单信息（获取出货单id 单号）')
            news.append(url)  # 接口链接
            news.append(b['msg'])  # 执行结果
        else:
            print('校验失败，终止程序')
            sys.exit()

    # 销售出货 销售方出货（物流单）
    def a083_delivery_good(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/supplier/confirm/delivery/good'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.supplier_phone, md5Encode(123456))
        print(contract_save)
        # data = 'confirmDeliveryGoodDTO=%7B%22id%22%3A' + '%s' % contract_save[9] + '%2C%22invoiceSn%22%3A%22' + '%s' %contract_save[5] + \
        #        '%22%2C%22type%22%3A1%7D&' + 'sessionKey=%s&sign=76ab2bcb9817dc4c2dbc2a79168d4802' % token
        data = 'confirmDeliveryGoodDTO=%7B%22id%22%3A' + '%s' % contract_save[4] + '%2C%22invoiceSn%22%3A%22' + '%s' % \
               contract_save[
                   5] + '%22%2C%22type%22%3A2%2C%22addInvoiceLogisticsDTO%22%3A%7B%22logisticsSn%22%3A%2212580%22%2C%22companyName' \
                        '%22%3A%22%E9%BE%99%E9%97%A8%E9%95%96%E5%B1%80%22%2C%22logisticsPhoto%22%3A%22https%3A%2F%2' \
                        'Fjiuerliu.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Fprod%2F3f208131bd12d16ae283596c943dd507.jpg' \
                        '%22%2C%22invoicePhoto%22%3A%22https%3A%2F%2Fjiuerliu.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Fprod' \
                        '%2Fd47b0c57843a9a9087af58b1080b2a2b.jpg%22%7D%7D&' + 'sessionKey=%s&sign=36d582f3b5cadfa9a46ed94a08374e75' % token

        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '销售出货 销售方出货（物流单）')

    # 采购方收货 采购方点击收货
    def a088_collection_good(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/purchaser/confirm/collection/good'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.purchaser_phone, md5Encode(123456))
        data = 'id=%s&sessionKey=%s&sign=d3b53806a5ef825010b7c9fb006362ae' % (contract_save[4], token)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '采购方收货 采购方点击收货')

    # 采购方收货 采购方点击品检
    def a123_confirm_inspection(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/purchaser/confirm/inspection'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.purchaser_phone, md5Encode(123456))
        data = 'id=%s&sessionKey=%s&sign=f5833db7b78ab59f432ecdd7edc75dd1' % (contract_save[4], token)
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '采购方收货 采购方点击品检')

    # 采购方收货 采购方点击入库
    def a127_collection_good(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/invoice/purchaser/confirm/warehousing'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        token = public.get_token(http_.purchaser_phone, md5Encode(123456))
        # data = 'id=%s&sessionKey=%s&sign=f5833db7b78ab59f432ecdd7edc75dd1' % (contract_save[4], token)
        data = 'id=' + '%s' % contract_save[
            4] + '&invoiceWarehousingEnclosureUrlListStr=https%3A%2F%2Fsunawtest.oss-cn-' \
                 'shenzhen.aliyuncs.com%2Fjiuerliu%2Ftest%2Fd03d27e9b037c302fa04819271ced53.jpg' \
                 '%2Chttps%3A%2F%2Fsunawtest.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Ftest%2F853' \
                 '878e80a028eec960c7f09d104549f.jpg&sessionKey=' + '%s' % token + '&sign=b44311f50401492fbc74e53e0a7effbb&sysTag=S00102'
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '采购方收货 采购方点击入库')

    # # 销售寄票 销售方查看寄票列表信息
    # def a131_supplier_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/supplier/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=5d0738fbb9f42b1018ec3ea658562f99&startTime=&state=0' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     try:
    #         r = requests.post(url, data=data, headers=_headers())
    #
    #         # 将字符串格式转换为字典
    #         b = eval(r.text)
    #         print('==========>>>failed:%s' % b)
    #     except Exception as e:
    #         time.sleep(20)
    #         r = requests.post(url, data=data, headers=_headers())
    #         # 将字符串格式转换为字典
    #         b = eval(r.text)
    #         print('==========>>>failed:%s' % b)
    #         print('错误信息', traceback.format_exc())
    #     try:
    #         print('列表中信息数量:', b['data']['total'])
    #         news.append(b['data']['total'])  # 列表中信息数量
    #     except Exception:
    #         print('不为列表，信息为空')
    #         news.append('无')  # 列表中信息数量
    #     # print('销售出货 已收货出货单信息')
    #     # 出货单状态 1.待出货2.待收货（供应商已出货）3.待品检（采购商已收货）4.待入库（采购商已品鉴）5.已入库
    #     if b['data']['records'][0]['invoiceApplySn'] == contract_save[2] and b['data']['records'][0][
    #         'state'] == 1:
    #         contract_save.append(b['data']['records'][0]['id'])
    #         contract_save.append(b['data']['records'][0]['invoiceReceiptSn'])
    #         print('运行结果:%s' % b['msg'])
    #         news.append('销售寄票 销售方查看寄票列表信息')
    #         news.append(url)  # 接口链接
    #         news.append(b['msg'])  # 执行结果
    #     else:
    #         print('校验失败，终止程序')
    #         sys.exit()
    #
    # # 销售寄票 销售方查看 待寄票标签下列表信息
    # def a132_supplier_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/supplier/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=5d0738fbb9f42b1018ec3ea658562f99&startTime=&state=1' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '销售寄票 销售方查看 待寄票标签下列表信息','state', 1)
    #
    # # 代理收票 代理方查看 待寄票标签下列表信息
    # def a133_receive_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/agent/receive/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.agent_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=0ab1d18cb5ca1120af940bf990b46b1b&size=10&startTime=' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '销售寄票 销售方查看 待寄票标签下列表信息',  'state', 1)
    #
    #
    # # 销售寄票 销售方点击寄票
    # def a1351_receipt_confirm(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/supplier/send/receipt/confirm'
    #     # url = http_.http_case + '/api/v1/receipt/bill/enclosure/save'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'id=%s&sessionKey=%s&sign=11aed06acc867ce7789a914e8c83823a' % (contract_save[6], token)
    #     asdf = 123456789012345678901234567890 + args[1]
    #     print(args[1])
    #     # data = 'invoiceReceiptBillId=418&invoiceReceiptBillNo=' + '%s' % asdf + '&invoiceReceiptBillSn=SP190703NEO2T003&invoiceReceiptPhotoUrl=https%3A%2F%2Fsunawtest.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Ftest%2Fcf1a8411a382b2ca3056f15d8ccf4d02.jpg&sessionKey=' + '%s' % token + '&sign=dc58d48e49bb2ee075a7320854c94b8c&sysTag=S00102&taxClassificationCode=123456789%2C123456789%2C123456789%2C123456789%2C12345678901234567890%2C1234567890%2C1234567890%2C1234567890%2C12345678987654321'
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '销售寄票 销售方点击寄票')
    #
    # # 销售寄票 销售方查看全部标签下寄票列表信息
    # def a135_supplier_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/supplier/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=5d0738fbb9f42b1018ec3ea658562f99&startTime=&state=0' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '销售寄票 销售方查看 待寄票标签下列表信息',  'state', 2)
    #
    #
    # # 代理收票 代理方确认收票
    # def a138_receive_receipt(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/agent/confirm/receive/receipt'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.agent_phone, md5Encode(123456))
    #     data = 'id=%s&sessionKey=%s&sign=af7bf9c64e630332023b04ebd4a07da6' % (
    #         contract_save[6], token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '销售寄票 销售方查看 代理方确认收票')
    #
    # # 代理收票 代理方查看 待寄票标签下列表信息
    # def a140_agent_send_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/agent/send/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.agent_phone, md5Encode(123456))
    #     # data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime==' % (
    #     #     token)
    #     data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime=' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     try:
    #         r = requests.post(url, data=data, headers=_headers())
    #
    #         # 将字符串格式转换为字典
    #         b = eval(r.text)
    #         print('==========>>>failed:%s' % b)
    #     except Exception as e:
    #         time.sleep(20)
    #         r = requests.post(url, data=data, headers=_headers())
    #         # 将字符串格式转换为字典
    #         b = eval(r.text)
    #         print('==========>>>failed:%s' % b)
    #         print('错误信息', traceback.format_exc())
    #     try:
    #         print('列表中信息数量:', b['data']['total'])
    #         news.append(b['data']['total'])  # 列表中信息数量
    #     except Exception:
    #         print('不为列表，信息为空')
    #         news.append('无')  # 列表中信息数量
    #     # print('销售出货 已收货出货单信息')
    #     # 出货单状态 1.待出货2.待收货（供应商已出货）3.待品检（采购商已收货）4.待入库（采购商已品鉴）5.已入库
    #     # print(b)
    #     if b['data']['records'][0]['invoiceApplySn'] == contract_save[2] and b['data']['records'][0][
    #         'state'] == 3 :
    #         contract_save.append(b['data']['records'][0]['id'])
    #         contract_save.append(b['data']['records'][0]['receiptSn'])
    #         print('运行结果:%s' % b['msg'])
    #         news.append('代理收票 代理方查看 待寄票标签下列表信息')
    #         news.append(url)  # 接口链接
    #         news.append(b['msg'])  # 执行结果
    #     else:
    #         print('校验失败，终止程序')
    #         sys.exit()
    #
    # # 销售寄票 销售方查看 已收票标签下列表信息
    # def a141_supplier_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/supplier/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=5d0738fbb9f42b1018ec3ea658562f99&startTime=&state=3' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '销售寄票 销售方查看 待寄票标签下列表信息', 'state', 3)
    #
    #
    # # 采购收票 采购方查看 待收票标签下列表信息
    # def a142_purchaser_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/purchaser/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.purchaser_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=86bfcd3a1db1f2b6ee472749c30985eb&startTime=&state=0&sysTag=S00102' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '采购收票 采购方查看 待收票标签下列表信息', 'state', 3)
    #
    # # 代理收款 代理方查看收票后 收款标签下列表信息
    # def a144_receive_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/payment/agent/gathering/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.agent_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=0ab1d18cb5ca1120af940bf990b46b1b&size=10&startTime=' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '代理收款 代理方查看收票后 收款标签下列表信息')
    #
    # # # 采购付款 采购方查看 待付款标签下列表信息(获取付款编号)
    # # def a145_payment_page(self, *args):
    # #     # sessionID = self.sessionID
    # #     url = http_.http_case + '/api/v1/payment/purchaser/page'
    # #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    # #     token = public.get_token(http_.purchaser_phone, md5Encode(123456))
    # #     data = 'current=1&endTime=&keyWord=&listType=0&pageSize=10&sessionKey=%s&sign=1773ea1aff895f05231f4054f5c725fa&startTime=' % (
    # #         token)
    # #     print(data)
    # #     print('url:%s' % url)
    # #     try:
    # #         r = requests.post(url, data=data, headers=_headers())
    # #         # 将字符串格式转换为字典
    # #         b = eval(r.text)
    # #         print('==========>>>failed:%s' % b)
    # #     except Exception as e:
    # #         time.sleep(20)
    # #         r = requests.post(url, data=data, headers=_headers())
    # #         # 将字符串格式转换为字典
    # #         b = eval(r.text)
    # #         print('==========>>>failed:%s' % b)
    # #         print('错误信息', traceback.format_exc())
    # #     try:
    # #         print('列表中信息数量:', b['data']['total'])
    # #         news.append(b['data']['total'])  # 列表中信息数量
    # #     except Exception:
    # #         print('不为列表，信息为空')
    # #         news.append('无')  # 列表中信息数量
    # #     # print('销售出货 已收货出货单信息')
    # #     # 出货单状态 1.待出货2.待收货（供应商已出货）3.待品检（采购商已收货）4.待入库（采购商已品鉴）5.已入库
    # #     # print(b)
    # #     if b['data']['purchaserInvoicePaymentPageVO']['records'][0]['invoiceSn'] == contract_save[4]:
    # #         contract_save.append(b['data']['purchaserInvoicePaymentPageVO']['records'][0]['invoicePaymentSn'])
    # #         contract_save.append(b['data']['purchaserInvoicePaymentPageVO']['records'][0]['id'])
    # #         print('运行结果:%s' % b['msg'])
    # #         news.append('代理收票 代理方查看 待寄票标签下列表信息')
    # #         news.append(url)  # 接口链接
    # #         news.append(b['msg'])  # 执行结果
    # #     else:
    # #         print('校验失败，终止程序')
    # #         sys.exit()
    # #
    # # # 采购付款 采购方在未收票情况下点击付款
    # # def a146_purchaser_payment(self, *args):
    # #     # sessionID = self.sessionID
    # #     url = http_.http_case + '/api/v1/payment/purchaser/confirm/payment'
    # #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    # #     token = public.get_token(http_.purchaser_phone, md5Encode(123456))
    # #     data = 'id=' + '%s' % contract_save[
    # #         9] + '&paymentVoucherUrl=https://sunawtest.oss-cn-shenzhen.aliyuncs.com/jiuerliu/test/c2acba0cb2add' \
    # #              '0d82a94495df17c393.png,https://sunawtest.oss-cn-shenzhen.aliyuncs.com/jiuerliu/test/816de21e75c25c41c' \
    # #              '167fe9889f5f56a.png&' + 'sessionKey=%s' % (token)
    # #     print(data)
    # #     print('url:%s' % url)
    # #     implement(url, data, '采购付款 采购方在未收票情况下点击付款')
    # #
    # # # 代理寄票 代理方发送寄票单
    # # def a147_enclosure_save(self, *args):
    # #     # sessionID = self.sessionID
    # #     # url = http_.http_case + '/api/v1/receipt/agent/confirm/send/receipt'
    # #     url = http_.http_case + '/api/v1/receipt/bill/enclosure/save'
    # #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    # #     token = public.get_token(http_.agent_phone, md5Encode(123456))
    # #     # data = 'id=' + '%s' % contract_save[14] + '&sessionKey=%s&sign=70b369fc6383326105162d78babbe084' % (token)
    # #     asdf = 123456789012345678901234567890 + args[1]
    # #     print(args[1])
    # #     # data = 'invoiceReceiptBillId=427&invoiceReceiptBillNo='+'%s'%asdf+'&invoiceReceiptBillSn=JP190704NEO2T003&invoiceReceiptPhotoUrl=https%3A%2F%2Fsunawtest.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Ftest%2Fdeeb70b64cb7e2d238c38670da76c2ce.gif&sessionKey='+'%s'%token+'&sign=d030abc09915c7ac6e29371d6f8d5f0d&taxClassificationCode=12345678%2C123456789098765432%2C32456787867654546574657%2C1236478659756853425141735%2C846637265324354657984736%2C3264756768574635116375846%2C24736485787634625%2C125364436758%2C321643574687)'
    # #     data = 'invoiceReceiptBillId=226&invoiceReceiptBillNo=' + '%s' % asdf + '&invoiceReceiptBillSn=' + '%s' % contract_save[7] + '&invoiceReceiptPhotoUrl=https%3A%2F%2Fjiuerliu.oss-cn-shenzhen.aliyuncs.com%2Fjiuerliu%2Fprod%2F5d71e56e7fc42181e8664747bbfef6eb.jpg&sessionKey=' + '%s' % token + '=c275c88e51c2f35a483f08cdfcd7d23b&taxClassificationCode=12345%2C123456%2C1234567%2C12345678%2C123456789%2C1234567890'
    # #     print(data)
    # #     print('url:%s' % url)
    # #     implement(url, data, '代理寄票 代理方发送寄票单')
    # #
    # # 代理寄票 代理方点击寄票
    # def a1481_agent_receipt(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/receipt/agent/confirm/send/receipt'
    #     # url = http_.http_case + '/api/v1/receipt/bill/enclosure/save'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.agent_phone, md5Encode(123456))
    #     data = 'id=' + '%s' % contract_save[8] + '&sessionKey=%s&sign=70b369fc6383326105162d78babbe084' % (token)
    #     asdf = 123456789012345678901234567890 + args[1]
    #     print(args[1])
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '代理寄票 代理方点击寄票')
    # #
    # # # 代理寄票 代理方查看已寄票标签下列表信息
    # # def a148_agent_send_page(self, *args):
    # #     url = http_.http_case + '/api/v1/receipt/agent/send/page'
    # #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    # #     token = public.get_token(http_.agent_phone, md5Encode(123456))
    # #     # data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime==' % (
    # #     #     token)
    # #     data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime=' % (
    # #         token)
    # #     print(data)
    # #     print('url:%s' % url)
    # #     implement(url, data, '代理寄票 代理方查看已寄票标签下列表信息', 'invoiceSn', contract_save[6], 'state', 4, )
    # # #
    # # # 采购收票 采购方查看已寄票标签下列表信息
    # # def a149_receipt_purchaser_page(self, *args):
    # #     url = http_.http_case + '/api/v1/receipt/purchaser/page'
    # #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    # #     token = public.get_token(http_.purchaser_phone, md5Encode(123456))
    # #     # data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime==' % (
    # #     #     token)
    # #     data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=f1460d25cc28e967551cd2de27f5363c&startTime=&state=0' % (
    # #         token)
    # #     print(data)
    # #     print('url:%s' % url)
    # #     implement(url, data, '采购收票 采购方查看已寄票标签下列表信息', 'invoiceSn', contract_save[4], 'state', 4)
    # #
    # # 采购收票 采购方点击收票
    # def a150_receipt_confirm(self, *args):
    #     url = http_.http_case + '/api/v1/receipt/purchaser/receive/receipt/confirm'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.purchaser_phone, md5Encode(123456))
    #     # data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime==' % (
    #     #     token)
    #     data = 'id=' + '%s' % contract_save[8] + '&sessionKey=%s&sign=b19c010b58c2eb6a0887a5157412b9cb0' % (
    #         token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '# 采购收票 采购方点击收票')
    # #
    # # # 采购收票 采购方查看已寄票标签下列表信息
    # # def a151_receipt_purchaser_page(self, *args):
    # #     url = http_.http_case + '/api/v1/receipt/purchaser/page'
    # #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    # #     token = public.get_token(http_.purchaser_phone, md5Encode(123456))
    # #     # data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime==' % (
    # #     #     token)
    # #     data = 'current=1&endTime=&keyWord=&pageSize=10&sessionKey=%s&sign=f1460d25cc28e967551cd2de27f5363c&startTime=&state=0' % (
    # #         token)
    # #     print(data)
    # #     print('url:%s' % url)
    # #     implement(url, data, '采购收票 采购方查看已寄票标签下列表信息', 'invoiceSn', contract_save[4], 'state', 5)
    # #
    # # # 代理寄票 代理方查看采购已收票标签下列表信息
    # # def a152_agent_send_page(self, *args):
    # #     url = http_.http_case + '/api/v1/receipt/agent/send/page'
    # #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    # #     token = public.get_token(http_.agent_phone, md5Encode(123456))
    # #     # data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime==' % (
    # #     #     token)
    # #     data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=03d48e36d0e8db40594a5bc57cda2f81&size=10&startTime=' % (
    # #         token)
    # #     print(data)
    # #     print('url:%s' % url)
    # #     implement(url, data, '代理寄票 代理方查看采购已收票标签下列表信息', 'invoiceSn', contract_save[4], 'state', 5, 'receiptSn',
    # #               contract_save[7])
    #
    # # # 采购付款 采购方在账期未到情况下点击付款
    # # def a153_purchaser_payment(self, *args):
    # #     # sessionID = self.sessionID
    # #     url = http_.http_case + '/api/v1/payment/purchaser/confirm/payment'
    # #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    # #     token = public.get_token(http_.purchaser_phone, md5Encode(123456))
    # #     data = 'id=' + '%s' % contract_save[
    # #         17] + '&paymentVoucherUrl=https://sunawtest.oss-cn-shenzhen.aliyuncs.com/jiuerliu/test/c2acba0cb2add' \
    # #               '0d82a94495df17c393.png,https://sunawtest.oss-cn-shenzhen.aliyuncs.com/jiuerliu/test/816de21e75c25c41c' \
    # #               '167fe9889f5f56a.png&' + 'sessionKey=%s' % (token)
    # #     print(data)
    # #     print('url:%s' % url)
    # #     implement(url, data, '采购付款 采购付款 采购方在账期未到情况下点击付款')


    # def a300_(self,*args):
    #     lendingPrice = random.randint(1, 10)
    #     lendingPrice = int(lendingPrice)
    #     url = http_.http_case + '/api/v1/quota/lending/apply/add'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #
    #     data = 'debtorServiceFeePaymentAccount=AP20190725757HOQ&lendingDayNum=1&lendingPrice=%s&lendingPurpose=7&sessionKey=%s&sysTag=S00102'%(lendingPrice,token)
    #     print(data)
    #     print('url:%s' % url)
    #     implement(url, data, '采购付款 采购付款 采购方在账期未到情况下点击付款')


class Sale_Integration(object):

    # 合同处理 全部列表页
    def contract_deal_page(self, *args):
        # sessionID = self.sessionID
        url = http_.http_case + '/api/v1/contract/wait/deal/page'
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        # token = public.get_token(http_.supplier_phone, md5Encode(123456))
        print(args[0])
        data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&sign=1a8776896b05c4fc168c20221d' \
               '98256b&size=10&sortType=2&startTime=' % args[0]
        print(data)
        print('url:%s' % url)
        print('data:%s' % data)
        # print('headers:%s' % _headers())
        implement(url, data, '合同处理 全部列表页')

    # # 合同处理 我方待处理列表页
    # def contract_deal_page2(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/deal/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&listType=1&sessionKey=%s&sign=03eb705f0b15f28d9fceaa27f237c0a0&size=' \
    #            '10&sortType=2&startTime=' % args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同处理 我方待处理列表页')
    #
    # # 合同处理 合作方待处理列表页
    # def contract_deal_page3(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/deal/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&listType=2&sessionKey=%s&sign=03eb705f0b15f28d9fceaa27f237c0a0&size=' \
    #            '10&sortType=2&startTime=' % args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同处理 合作方待处理列表页')
    #
    # # 合同申请页面 名称搜索
    # def contract_audit_page(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/audit/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=TU&listType=0&sessionKey=%s&sign=08fb443f8ff56632d32c276881b230a8&size=10&sortType=2&startTime=' % \
    #            args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请页面 发起方名称搜索')
    #
    # # 合同申请页面 名称搜索
    # def contract_audit_page1(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/audit/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=123&listType=0&sessionKey=%s&sign=08fb443f8ff56632d32c276881b230a8&size=10&sortType=2&startTime=' % \
    #            args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请页面 收到方名称搜索')
    #
    # # 合同申请页面 单号搜索
    # def contract_audit_page2(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/audit/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=CR0079WTLESL&listType=0&sessionKey=%s&sign=08fb443f8ff56632d32c276881b230a8&size=10&sortType=2&startTime=' % \
    #            args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请页面 委托单号搜索')
    #
    # # 合同申请页面 时间搜索
    # def contract_audit_page3(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/audit/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=2019-05-10&keyWord=&listType=0&sessionKey=%s&sign=ea407e8806463a69bda0a13a1c5e3908' \
    #            '&size=10&sortType=2&startTime=2019-05-01' % args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请页面 时间搜索')
    #
    # # 合同申请页面 时间+名称搜索
    # def contract_audit_page4(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/audit/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=2019-05-10&keyWord=123&listType=0&sessionKey=%s&sign=ea407e8806463a69bda0a13a1c5e3908' \
    #            '&size=10&sortType=2&startTime=2019-05-01' % args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请页面 时间+名称搜索')
    #
    # # 合同我方待审批列表
    # def wait_audit_page2(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/audit/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&listType=1&sessionKey=%s&sign=fcf1c92f44e77a87572b2cbe05ff9675&size=10&sortType=2&startTime=' % \
    #            args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同我方待审批列表')
    #
    # # 合同合作方待审批列表
    # def wait_audit_page3(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/audit/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&listType=2&sessionKey=%s&sign=fcf1c92f44e77a87572b2cbe05ff9675&size=10&sortType=2&startTime=' % \
    #            args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同合作方待审批列表')
    #
    # # 合同受托方待审批列表
    # def wait_audit_page4(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/wait/audit/page'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'current=1&endTime=&keyWord=&listType=3&sessionKey=%s&sign=fcf1c92f44e77a87572b2cbe05ff9675&size=10&sortType=2&startTime=' % \
    #            args[0]
    #     print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同受托方待审批列表')
    #
    # # 我方待审签（我为采购）详情接口
    # def contract_info1(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/info'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'id=%s&sessionKey=%s&sign=95aba521786b06b057baa0b52fd93dd2' % (contract_save[0], args[0])
    #     # print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请我方待审签（我为采购）详情接口')
    #
    # # 我方待审签（我为销售）详情接口
    # def contract_info2(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/info'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     print(args[0])
    #     data = 'id=%s&sessionKey=%s&sign=95aba521786b06b057baa0b52fd93dd2' % (contract_save[0], args[0])
    #     # print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请我方待审签（我为销售）详情接口')
    #
    # # 合作方待审签详情接口
    # def contract_info3(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/info'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'id=%s&sessionKey=%s&sign=95aba521786b06b057baa0b52fd93dd2' % (contract_save[0], args[0])
    #     # print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请 合作方待审签详情接口')
    #
    # # 代理方待审签详情接口
    # def contract_info4(self, *args):
    #     # sessionID = self.sessionID
    #     url = http_.http_case + '/api/v1/contract/info'
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     # token = public.get_token(http_.supplier_phone, md5Encode(123456))
    #     data = 'id=%s&sessionKey=%s&sign=95aba521786b06b057baa0b52fd93dd2' % (contract_save[0], args[0])
    #     # print(data)
    #     print('url:%s' % url)
    #     print('data:%s' % data)
    #     # print('headers:%s' % _headers())
    #     implement(url, data, '合同申请 代理方待审签详情接口')


class Purchase_Integration(object):
    def pass_1(self, *args):
        pass


class Agent_Integration(object):
    def pass_1(self, *args):
        pass
