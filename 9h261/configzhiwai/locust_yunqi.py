import datetime
import hashlib
import random
import re
import traceback
from decimal import *

import requests
from xlutils.copy import copy

from config import http_
from function import get_authorization, public
import os,sys
import time
from multiprocessing import Process

from locust import HttpLocust, TaskSet,TaskSequence, task,seq_task
from selenium import webdriver

def md5Encode(str_):
    m = hashlib.md5()
    str_ = str(str_)
    m.update(str_.encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()

header = {
    'Accept': '*/*',
    'Content-Length': '385',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'okhttp/3.12.1',
    # 'Authorization': Authorization,

    # 'User-Agent': 'Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome74.0.3729.131 Safari537.36',

}

yun_sesskey_list = []
yun_openid_list = []
yy_sesskey_list = []
sj_sesskey_list = []

http_yun = 'http://163.177.128.179:63201'
http_yy = 'http://163.177.128.179:63073'


#
# # todo 利用接口进入云启，并获取sessionkey以及openid 。因为登录和应用的host不同
def account_login(*args):
    phone = 13135654887
    # sessionID = self.sessionID
    url = http_yun + '/api/v1/erp/account/login'
    data = 'deviceAppVersion=1.18.3&deviceBundleID=com.sunaw.channel&deviceBundleNumber=16' \
           '&deviceId=msm8953&deviceM=%5Bobject%20Object%5D&deviceModel=Redmi%205%20Plus' \
           '&deviceName=%5Bobject%20Object%5D&deviceSysName=Android' \
           '&deviceUId=5cdff2a9646f21b2&deviceVersion=7.1.2' \
           '&password=e10adc3949ba59abbe56e057f20f883e' \
           '&phone=' + '%s' % phone + '&registerId=18071adc03625834823&sign=0b7cc92f325d4316166bcfc2daf96776'
    print(data)
    print('url:%s' % url)
    print('data:%s' % data)
    # print('headers:%s' % _headers())
    try:
        r = requests.post(url, data=data, headers=header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
    except Exception as e:
        time.sleep(30)
        r = requests.post(url, data=data, headers=header)
        # 将字符串格式转换为字典
        b = eval(r.text)
        print('==========>>>failed:%s' % b)
        print('错误信息', traceback.format_exc())
    try:
        yun_sesskey_list.append(b['data']['sessKey'])  #
        yun_openid_list.append(b['data']['openId'])  #
    except Exception:
        print('不为列表，信息为空')
        yun_sesskey_list.append('无')  # 列表中信息数量
    return yun_sesskey_list, yun_openid_list



# 定义用户行为，继承TaskSet类，用于描述用户行为
# (这个类下面放各种请求，请求是基于requests的，每个方法请求和requests差不多，请求参数、方法、响应对象和requests一样的使用，url这里写的是路径)
# client.get===>requests.get
# client.post===>requests.post
class Test_yunqi(TaskSequence):

    # @seq_task(1)  # 1代表优先执行，2次之，以此类推
    # @task(1)  # 1代表执行一次，2代表2次，以此类推
    # def account_login(self):
    #     # # # todo 接口
    #     # for i in range(100, 1000):
    #     # print(i)
    #     phone = '13135654887'
    #     # 进入云启
    #     r_bill_info = self.client.post('/api/v1/erp/account/login', timeout=30, headers=header,
    #                                    data='deviceAppVersion=1.18.3&deviceBundleID=com.sunaw.channel&deviceBundleNumber=16' \
    #                                         '&deviceId=msm8953&deviceM=%5Bobject%20Object%5D&deviceModel=Redmi%205%20Plus' \
    #                                         '&deviceName=%5Bobject%20Object%5D&deviceSysName=Android' \
    #                                         '&deviceUId=5cdff2a9646f21b2&deviceVersion=7.1.2' \
    #                                         '&password=e10adc3949ba59abbe56e057f20f883e' \
    #                                         '&phone=' + '%s' % phone + '&registerId=18071adc03625834823&sign=0b7cc92f325d4316166bcfc2daf96776')
    #
    #     print(sys._getframe().f_code.co_name+'%s' % r_bill_info.json())
    #     # print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     data1 = r_bill_info.json()
    #     sesskey  = data1['data']['sessKey']
    #     yun_sesskey_list.append(sesskey)
    #     openid = data1['data']['openId']
    #     yun_openid_list.append(openid)
    #     print('openid:%s'%openid)
    #     print('sesskey:%s'%sesskey)


    @seq_task(1)
    @task(1)
    def company_login(self):
        # # # todo 接口
        # print(sesskey_list)
        # 进入调研bao
        yun_sesskey_list, yun_openid_list = account_login()
        r_bill_info = self.client.post('/api/v1/company/login', timeout=30, headers=header,
                                       data='accountSn=43044049&openId=%s&shangwoSessionKey=%s&sign=ff0fb8d3b820c25e613f80d2a0e0496d' %
                                            (yun_openid_list[-1],yun_sesskey_list[-1]))
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        print("r_bill_info:%s" % r_bill_info.json())

        # print('accountSn=43044049&openId=%s&shangwoSessionKey=%s&sign=ff0fb8d3b820c25e613f80d2a0e0496d' %
        #                                     (yun_openid_list[-1],yun_sesskey_list[-1]))
        sesskey2 = r_bill_info.json()['data']['sessionKey']
        yy_sesskey_list.append(sesskey2)

    @seq_task(2)
    @task(1)
    def questionnaire_submit(self):
        # # # todo 接口
        # 提交调研表
        r_bill_info = self.client.post('/api/v1/company/questionnaire/submit', timeout=30, headers=header,
                                       data='aboveCollegeNumber=699&accountSn=43044049&appearanceDesignNumber=1'
                                            '&attritionNumber=6&attritionTime=2020-04-02&attritionTimeStr=1585785600000'
                                            '&businessDifficultiesAttritionNumber=5'
                                            '&certificationQualificationIdListStr=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17'
                                            '&companyName=%E5%A4%A7%E7%A7%91%E6%8A%80&companyProfile=%E5%85%AC%E5%8F%B8%E7%AE%80%E4%BB%8B'
                                            '&contactNumber=18772606900&enterpriseTechnicalFieldIdListStr=2%2C3'
                                            '&exportVolumeInTwoQuarters=1&fixedAssets=8000&id=&importVolumeInTwoQuarters=1'
                                            '&intermediateTitleNumber=80&inventionPatentNumber=3&isCreditFundDemand=1'
                                            '&isEmploymentLegalPlanning=1&isExternalLegalCounsel=1&isInternalLegalDepartment=1'
                                            '&isLawyerFollowUpCollection=1&isLawyerInNegotiation=1&isLawyerReviewContract=1'
                                            '&isLegalSupportForDecision=1&isListingDemand=1&isNeedLegalAidServices=1'
                                            '&isPartnershipWithUniversities=1&mailingAddress=%E9%80%9A%E8%AE%AF%E5%9C%B0%E5%9D%80'
                                            '&mainProducts=%E4%B8%BB%E8%90%A5%E4%BA%A7%E5%93%81&netAssetsOfLastYears=900'
                                            '&netAssetsOfThreeYearsAgo=800&netAssetsOfTwoYearsAgo=850&newRecruitsNumber=7'
                                            '&newRecruitsTime=2020-04-02&newRecruitsTimeStr=1585785600000'
                                            '&openId=ad61ab143223efbc24c7d2583be69251'
                                            '&projectLeader=%E9%A1%B9%E7%9B%AE%E8%B4%9F%E8%B4%A3%E4%BA%BA&qualitys='
                                            '&registeredCapital=3000&registrationTime=2013-04-02'
                                            '&registrationTimeStr=1364860800000&researchEquipment=2000'
                                            '&salesDownInTwoQuarters=1&salesRevenueOfLastYears=666'
                                            '&salesRevenueOfThreeYearsAgo=450&salesRevenueOfTwoYearsAgo=555'
                                            '&seniorTitlesOrAboveNumber=7&sessionKey='+'%s'%(yy_sesskey_list[-1]) + '&sign=8ab5a939b6b8c36550564c6f425a6262&socialInsuranceStaffNumber=9'
                                            '&softwareCopyrightNumber=0&staffNumber=5000&technicals=&totalCostOfPreviousYear=400'
                                            '&unemploymentInsuranceStaffNumber=8&unitPropertyIdListStr=1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10&units=&utilityModelPatentNumber=2' )
        print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
        print("r_bill_info:%s" % r_bill_info.json())
    #
    # @seq_task(3)
    # @task(1)
    # def management_login(self):
    #     # # # todo 接口
    #     # print(sesskey_list)
    #     # 进入商机库助手
    #     yun_sesskey_list, yun_openid_list = account_login()
    #     print('))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))')
    #     r_bill_info = self.client.post('/api/v1/management/login', timeout=30, headers=header,
    #                                    data='accountSn=18059284&admin=0&appKey=S00101&format=json&openId=%s&phone=%s'
    #                                         '&shangwoSessionKey=%s&sign=bf9b97062b54801d6b637da829fbfe4f'
    #                                         '&signMethod=01&sysTag=S00102&timestamp=15858223157&version=1.0' %
    #                                         (yun_openid_list[-1],18772606900,yun_sesskey_list[-1]))
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     print("r_bill_info:%s" % r_bill_info.json())
    #
    #     # print('accountSn=43044049&openId=%s&shangwoSessionKey=%s&sign=ff0fb8d3b820c25e613f80d2a0e0496d' %
    #     #                                     (yun_openid_list[-1],yun_sesskey_list[-1]))
    #     sesskey3 = r_bill_info.json()['data']['sessionKey']
    #     sj_sesskey_list.append(sesskey3)
    #
    # @seq_task(4)
    # @task(1)
    # def opportunity_submit(self):
    #     # # # todo 接口
    #     # print(sesskey_list)
    #     # 提交商机
    #     r_bill_info = self.client.post('/api/v1/management/business/opportunity/submit', timeout=30, headers=header,
    #                                    data='businessOpportunityCategoryId=14&businessOpportunityContent=sjnr'
    #                                         '&companyName=qymc&contact=lxr&contactNumber=lxdh&id=32'
    #                                         '&questionnaireId=302&servicerId=22&sessionKey=%s&sysTag=S00102' %(sj_sesskey_list[-1]))
    #     print('-' * 50 + '%s' % sys._getframe().f_code.co_name + '-' * 50)
    #     print("r_bill_info:%s" % r_bill_info.json())


# 这个类类似设置性能测试，继承HttpLocust
class websitUser(HttpLocust):
    # 指向一个上面定义的用户行为类
    task_set = Test_yunqi
    # 执行事物之间用户等待时间的下界，单位毫秒，相当于lr中的think time
    # host = 'http://163.177.128.179:63095'  #todo 进入云企后的host
    # host = 'http://163.177.128.179:63201' #todo 登陆云企的host
    min_wait = 5000
    max_wait = 9000


def run_os():
    os.system('locust -f locust_yunqi.py --host=%s --web-host="127.0.0.1"' % http_yy)
    print("os子进程执行中>>> pid={0},ppid={1}".format(os.getpid(), os.getppid()))


def open_web():
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:8089')
    print("driver子进程执行中>>> pid={0},ppid={1}".format(os.getpid(), os.getppid()))
    driver.refresh()  # 刷新方法 refresh


if __name__ == '__main__':
    # host = 'http://120.79.223.2:2001'

    # print(yun_sesskey_list,yun_openid_list)
    pro_list = []
    pro1 = Process(target=run_os, args=())
    pro_list.append(pro1)
    pro2 = Process(target=open_web, args=())
    pro_list.append(pro2)
    for i in pro_list:
        i.start()
        time.sleep(5)
