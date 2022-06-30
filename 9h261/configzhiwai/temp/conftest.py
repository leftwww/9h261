import pytest
from temp import confog_http
import datetime
import requests
import time
import traceback,sys


@pytest.fixture(scope='function')
def login():
    print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    url = confog_http.http_login + '/api/v1/erp/account/mobile'
    data = 'accountSn=&admin=&appKey=S00101&code=1&format=json&openId=&phone=' + '%s' % confog_http.agent_phone + '&sessionKey=' \
                                                                                                '&sign=0bfdf7e4c71e3178867b449658af65db&signMethod=01&sysTag=S00102&timestamp=15879552909&version=1.0'
    print(data)
    print('url:%s' % url)
    print('data:%s' % data)
    print(datetime.datetime.now())
    # todo 登陆云企
    try:
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(20)
        r = requests.post(url, data=data, headers=confog_http.header)
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
        # todo 进入商机库助手
        if confog_http.agent_phone == confog_http.agent_phone:
            print('++++++++++++++++++++++++++++++++++++++++++++++++++')
            url = confog_http.http_case + "/api/v1/management/login"  # agent/login
            data = 'accountSn=18059284&admin=0&appKey=S00101&format=json&openId=' + '%s' % openid + '' \
                                                                                                    '&phone=' + '%s' % confog_http.agent_phone + '&shangwoSessionKey=phone=' + '%s' % token_ + '' \
                                                                                                                                                                             '&sign=5870da5b2a76d7e88ba89cfcaa7330ca&signMethod=01&sysTag=S00102&timestamp=15879584849&version=1.0'

        try:
            r = requests.post(url, data=data, headers=confog_http.header)
            # 将字符串格式转换为字典
            b = eval(r.text)
            print('==========>>>failed:%s' % b)
        except Exception as e:
            time.sleep(20)
            print('错误信息', traceback.format_exc())
            r = requests.post(url, data=data, headers=confog_http.header)
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



@pytest.fixture(scope='function')
def login2():
    print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    url = confog_http.http_login + '/api/v1/erp/account/mobile'
    data = 'accountSn=&admin=&appKey=S00101&code=1&format=json&openId=&phone=' + '%s' % confog_http.launch_phone + '&sessionKey=' \
                                                                                                '&sign=0bfdf7e4c71e3178867b449658af65db&signMethod=01&sysTag=S00102&timestamp=15879552909&version=1.0'
    print(data)
    print('url:%s' % url)
    print('data:%s' % data)
    print(datetime.datetime.now())
    # todo 登陆云企
    try:
        r = requests.post(url, data=data, headers=confog_http.header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(20)
        r = requests.post(url, data=data, headers=confog_http.header)
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
        # todo 进入fudao手
        if confog_http.launch_phone == confog_http.launch_phone:
            print('++++++++++++++++++++++++++++++++++++++++++++++++++')
            url = confog_http.http_case + "/api/v1/servicer/login"  # agent/login
            data = 'accountSn=44024094&admin=1&appKey=S00101&format=json&&openId=' + '%s' % openid + '' \
                                                                                                    '&phone=' + '%s' % confog_http.launch_phone + '&shangwoSessionKey=phone=' + '%s' % token_ + '' \
                                                                                                                                                                             '&sign=4c13f64986d14bcd057d83afba125554&signMethod=01&sysTag=S00102&timestamp=15882172569&version=1.0'

        try:
            r = requests.post(url, data=data, headers=confog_http.header)
            # 将字符串格式转换为字典
            b = eval(r.text)
            print('==========>>>failed:%s' % b)
        except Exception as e:
            time.sleep(20)
            print('错误信息', traceback.format_exc())
            r = requests.post(url, data=data, headers=confog_http.header)
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