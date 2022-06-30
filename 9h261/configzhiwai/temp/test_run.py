import pytest
import datetime
import sys
import time
import traceback
import hashlib
import requests

from temp import confog_http


# # from function import get_authorization, public_demo
# def implement(url, data, case, *args):  # 校验接口返回内容
#     print(datetime.datetime.now())
#     try:
#         r = requests.post(url, data=data, headers=confog_http.header)
#         # 将字符串格式转换为字典
#         b = eval(r.text)
#         print('==========>>>failed:%s' % b)
#     except Exception as e:
#         # 重新请求
#         time.sleep(20)
#         r = requests.post(url, data=data, headers=confog_http.header)
#         # 将字符串格式转换为字典
#         b = eval(r.text)
#         print('==========>>>failed:%s' % b)
#         print('错误信息', traceback.format_exc())
#     print(datetime.datetime.now())
#     try:
#         print('列表中信息数量:', b['data']['total'])
#         news.append(b['data']['total'])  # 列表中信息数量
#     except Exception:
#         print('不为列表，信息为空')
#         news.append('无')  # 列表中信息数量
#     print(case)
#     print(datetime.datetime.now())
#
# news = []  # 用例存放列表

session_list = []


def test_1(login):
    # sessionID = self.sessionID
    url = confog_http.http_case + '/api/v1/management/questionnaire/page'
    print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    token = login
    # session_list.append(token)
    data = 'current=1&endTime=&keyWord=&listType=0&sessionKey=%s&startTime=&sysTag=S00102' % token
    # print(data)
    print('url:%s' % url)
    print('data:%s' % data)
    # print('headers:%s' % _headers())
    try:
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(30)
        r = requests.post(url, data=data, headers=confog_http.header)
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
    # news.append('发起合同之选择代理方')
    # news.append(url)  # 接口链接
    # news.append(b['msg'])  # 执行结果

@pytest.mark.me
def test_2(login2):
    url = confog_http.http_case + '/api/v1/servicer/business/opportunity/page'
    print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    token = login2
    session_list.append(token)
    # session_list.append(token)
    data = 'current=1&endTime=&keyWord=&listType=1&sessionKey=%s&startTime=&sysTag=S00102' % token
    # print(data)
    print('url:%s' % url)
    print('data:%s' % data)
    # print('headers:%s' % _headers())
    try:
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(30)
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
        print('错误信息', traceback.format_exc())

    assert b['data']['records'][0]['id'] == 32

def test_3():
    url = confog_http.http_case + '/api/v1/servicer/business/opportunity/abnormal/page'
    print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    token = session_list[0]
    # session_list.append(token)
    data = 'current=1&endTime=&keyWord=&listType=1&sessionKey=%s&startTime=&sysTag=S00102' % token
    # print(data)
    print('url:%s' % url)
    print('data:%s' % data)
    # print('headers:%s' % _headers())
    try:
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(30)
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
        print('错误信息', traceback.format_exc())

def test_4():
    url = confog_http.http_case + '/api/v1/servicer/business/opportunity/pag'
    print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    token = session_list[0]
    # session_list.append(token)
    data = 'current=1&endTime=&keyWord=&listType=1&sessionKey=%s&startTime=&sysTag=S00102' % token
    # print(data)
    print('url:%s' % url)
    print('data:%s' % data)
    # print('headers:%s' % _headers())
    try:
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(30)
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
        print('错误信息', traceback.format_exc())


def test_5():
    url = confog_http.http_case + '/api/v1/servicer/customer/page'
    print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    token = session_list[0]
    # session_list.append(token)
    data = 'current=1&endTime=&keyWord=&listType=1&sessionKey=%s&startTime=&sysTag=S00102' % token
    # print(data)
    print('url:%s' % url)
    print('data:%s' % data)
    # print('headers:%s' % _headers())
    try:
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(30)
        r = requests.post(url, data=data, headers=confog_http.header)
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
    # news.append('发起合同之选择代理方')
    # news.append(url)  # 接口链接
    # news.append(b['msg'])  # 执行结果
    assert b['data']['records'][0]['id'] == 32

if __name__ == "__main__":
    # pytest.main(['test_run.py', '-s','-m','me'])
    pytest.main(['test_run.py', '-s'])
    # pytest.close()

