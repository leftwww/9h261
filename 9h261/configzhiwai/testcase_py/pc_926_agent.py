# -- coding: utf-8 -- 
# @Author : Zw
# @File : pc_926_agent.py


import time
from config.config_agent import Config_pc_agent as Ca, Logger
import config.globalvar as gl
import sys
import os
import re
import xlrd, xlutils, xlwt
from xlrd import open_workbook
from xlutils.copy import copy


def current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "-代理方-"
    return current_time


def re_int1(test):
    global re_int2
    if re.findall("\.00", test):
        # print("0.0")
        re_int2 = re.findall(r'(\d+)\.\d', test)[0]
        # print(re_int)
    elif re.findall("\.", test):
        # print("252")
        re_int2 = re.findall(r'(\d+\.\d)', test)[0]
        # print(re_int)
    else:
        # print("111")
        it = re.finditer(r"\d+", test)
        for match in it:
            re_int2 = match.group()
            # print(re_int)
    return int(re_int2)


def re_sub_(test):  # 获取有小数点值为.00的整数值
    global re_int_
    if re.findall("\.", test):
        # print("0.0")
        re_int_ = re.sub(r'\D', "", test)[0:-2]
        # print(re_int)
    else:
        # print("111")
        it = re.finditer(r"\d+", test)
        for match in it:
            re_int_ = match.group()
            # print(re_int)
    return re_int_


count = 0


# 获取新的页面信息
def new_execute_script(test):
    global count
    count += 1  # 调用一次则加一
    # print("count : %d" % count)
    driver = Ca().driver
    # 打开一个新页面
    driver.execute_script('window.open()')
    # 定位到新的页面
    driver.switch_to.window(driver.window_handles[count])  # 新的页面则用最新的索引
    driver.get(test)
    time.sleep(2.5)
    print("切换跳转至另一页面")
    # 定位回原来的页面
    # driver.switch_to.window(driver.window_handles[0])


def tes1t_time():
    test_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return test_time


path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('log_pc.txt')

start_url = Ca.start_url
if re.findall('test', start_url) or re.findall('b.926.net', start_url) :
    xpath_front = '//*[@id="root"]/div/section/div[2]/section/main/div/div/div/div[2]'
    xpath_front_1 = '//*[@id="root"]/div/section/div[2]/section/main/div/div/div/div[1]'
    xpath_main = '//main[@class="ant-layout-content"]'
else:
    xpath_front = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div[2]'
    xpath_front_1 = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div[1]'
    xpath_main = '//*[@id="root"]/div/div/div[2]/div[2]/div'


class PC_926_agent:
    start_url = Ca().start_url
    driver = Ca().driver
    # book = open_workbook("C:\\Users\Zuow\Desktop\\test_case.xlsx")
    # news = []
    gl._init()
    a = 0

    def check_information_if(self, Check_value, capture, Check_contents, process):
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if Check_value == capture:
            Ca().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % Check_value)
            Ca().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)

    def check_information_re(self, Check_value, capture, Check_contents, process):
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if re.findall(Check_value, capture):
            Ca().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % Check_value)
            Ca().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)

    def check_information_time(self, capture, Check_contents, process):
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if re.findall(tes1t_time(), capture):
            Ca().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % tes1t_time())
            Ca().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)

    # 校验委托操作记录
    def Operation_record(self, driver, information, information_user, step, check_info, check_time, check_user):
        time.sleep(1.5)
        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[1]')
        self.check_information_if(information, record_state1, check_info, step)  # information"发起方修改合同申请"  step"修改合同"
        # Ca().is_toast_exist("获取发起合同后的操作状态", "修改合同",  "云平台‘代理方’",sys._getframe().f_lineno)
        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[3]')
        self.check_information_time(record_time1, check_time, step)
        # Ca().is_toast_exist("获取发起合同后的操作时间", "修改合同",  "云平台‘代理方’",sys._getframe().f_lineno)
        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[2]')
        self.check_information_if(information_user, record_operator1, check_user, step)

    # 校验发货申请详情操作记录
    def Operation_record_2(self, driver, information, information_user, step, check_info, check_time, check_user):
        time.sleep(1.5)

        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[1]')
        self.check_information_if(information, record_state1, check_info, step)  # information"发起方修改合同申请"  step"修改合同"
        # Ca().is_toast_exist("获取发起合同后的操作状态", "修改合同",  "云平台‘代理方’",sys._getframe().f_lineno)
        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[3]')
        self.check_information_time(record_time1, check_time, step)
        # Ca().is_toast_exist("获取发起合同后的操作时间", "修改合同",  "云平台‘代理方’",sys._getframe().f_lineno)
        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[2]')
        self.check_information_if(information_user, record_operator1, check_user, step)

    # 校验weituo申请详情被拒绝后的操作记录
    def Operation_record_refuse(self, driver, information, information_user, step, check_info, check_time, check_user,
                                check_reason, check_details):
        time.sleep(1.5)
        agent_refuse_details = gl.get_value('agent_refuse_details')
        agent_refuse_reason = gl.get_value('agent_refuse_reason')
        # print('agent_refuse_reason=%s' % agent_refuse_details)
        # print('agent_refuse_reason=%s' % agent_refuse_reason)
        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[1]')
        self.check_information_if(information, record_state1, check_info, step)

        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[5]')
        self.check_information_time(record_time1, check_time, step)

        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[2]')
        self.check_information_if(information_user, record_operator1, check_user, step)

        refuse_reason1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[3]')
        self.check_information_re(agent_refuse_reason, refuse_reason1, check_reason, step)

        refuse_details1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[4]')
        self.check_information_re(agent_refuse_details, refuse_details1, check_details, step)

    # 校验发货申请详情被拒绝后的操作记录
    def Operation_record_refuse_2(self, driver, information, information_user, step, check_info, check_time, check_user,
                                  check_reason, check_details):
        time.sleep(1.5)
        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[1]')
        self.check_information_if(information, record_state1, check_info, step)

        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[5]')
        self.check_information_time(record_time1, check_time, step)

        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[2]')
        self.check_information_if(information_user, record_operator1, check_user, step)

        refuse_reason1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[3]')
        self.check_information_re('原始合同出错', refuse_reason1, check_reason, step)

        refuse_details1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div[2]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[4]')
        self.check_information_re('fkl', refuse_details1, check_details, step)

    # 获取并校验导航信息（导航有两步）
    def navigation_two(self, driver, information_1, information_2, step, check_info_1, check_info_2):

        navigation_1 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div[1]/div[3]/div')
        self.check_information_if(information_1, navigation_1, check_info_1, step)
        navigation_2 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div[2]/div[3]/div')
        self.check_information_if(information_2, navigation_2, check_info_2, step)

    # 获取并校验导航信息（导航有三步）
    def navigation_three(self, driver, information_1, information_2, information_3, step,
                         check_info_1, check_info_2, check_info_3):

        navigation_1 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[1]/div[3]/div')
        self.check_information_if(information_1, navigation_1, check_info_1, step)
        navigation_2 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[2]/div[3]/div')
        self.check_information_if(information_2, navigation_2, check_info_2, step)
        navigation_3 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[3]/div[3]/div')
        self.check_information_if(information_3, navigation_3, check_info_3, step)

    # 获取并校验页面目录信息（导航有两步）
    def catalog_two(self, driver, information_1, information_2, step, check_info_1, check_info_2):
        catalog_1 = Ca().xpath_text_(xpath_front_1 + '/div/span[1]/span[1]//span')
        self.check_information_if(information_1, catalog_1, check_info_1, step)
        catalog_2 = Ca().xpath_text_(xpath_front_1 + '/div/span[2]/span[1]//span')
        self.check_information_if(information_2, catalog_2, check_info_2, step)

    # 获取并校验页面目录信息（导航有三步）
    def catalog_three(self, driver, information_1, information_2, information_3, step,
                      check_info_1, check_info_2, check_info_3):
        catalog_1 = Ca().xpath_text_(xpath_front_1 + '/div/span[1]/span[1]//span')
        self.check_information_if(information_1, catalog_1, check_info_1, step)
        catalog_2 = Ca().xpath_text_(xpath_front_1 + '/div/span[2]/span[1]//span')
        self.check_information_if(information_2, catalog_2, check_info_2, step)
        catalog_3 = Ca().xpath_text_(xpath_front_1 + '/div/span[3]/span[1]//span')
        self.check_information_if(information_3, catalog_3, check_info_3, step)

    # 获取并校验页面分类列表信息（列表有三类）
    def list_three(self, driver, information_1, information_2, information_3, step,
                   check_info_1, check_info_2, check_info_3):
        classification_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

    # 获取并校验页面分类列表信息（列表有四类）
    def list_four(self, driver, information_1, information_2, information_3, information_4, step,
                  check_info_1, check_info_2, check_info_3, check_info_4):
        classification_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

    # 获取并校验页面分类列表信息（列表有五类）
    def list_five(self, driver, information_1, information_2, information_3, information_4, information_5, step,
                  check_info_1, check_info_2, check_info_3, check_info_4, check_info_5):
        classification_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

        classification_5 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]')
        self.check_information_if(information_5, classification_5, check_info_5, step)

    # 获取并校验页面分类列表信息（列表有六类）
    def list_six(self, driver, information_1, information_2, information_3, information_4, information_5, information_6,
                 step,
                 check_info_1, check_info_2, check_info_3, check_info_4, check_info_5, check_info_6):
        classification_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

        classification_5 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]')
        self.check_information_if(information_5, classification_5, check_info_5, step)

        classification_6 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]')
        self.check_information_if(information_6, classification_6, check_info_6, step)

    # 获取并校验委托详情页面信息
    def details_information(self, driver, step):
        contract_mark = gl.get_value('contract_mark')
        settlement_date = gl.get_value('settlement_date')
        apply_number = gl.get_value('apply_number')
        purchaser_name = gl.get_value('purchaser_name')
        supplier_name = gl.get_value('supplier_name')
        supplier_audit_time = gl.get_value('supplier_audit_time')
        price_sum_check_all_2 = gl.get_value('price_sum_check_all_2')

        apply_number_details = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[1]/div[2]')
        self.check_information_if(apply_number, apply_number_details, "委托创建单号", step)

        contract_mark_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[2]/div[2]')
        self.check_information_if(contract_mark, contract_mark_1, "原始合同编号", step)

        purchaser_name_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[3]/div[2]/a')
        self.check_information_if(purchaser_name, purchaser_name_1, "采购方名称", step)

        supplier_name_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[4]/div[2]/a')
        self.check_information_if(supplier_name, supplier_name_1, "销售方名称", step)

        settlement_date_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[5]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "结算方式", step)

        supplier_audit_time_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[6]/div[2]')
        self.check_information_time(supplier_audit_time_1, "发起方审核时间", step)

        full_price_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[7]/div[2]')
        self.check_information_re('10,000.00', full_price_1, "商品总金额", step)

        procurement_audit_time_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[8]/div[2]')
        self.check_information_time(procurement_audit_time_1, "合作方审核时间", step)
        if re.findall("通过", step):
            agent_audit_time_1 = Ca().xpath_text_(
                xpath_front + '/div/div[1]/div[2]/div[1]/div[9]/div[2]')
            self.check_information_time(agent_audit_time_1, "代理方审核时间", step)
        else:
            pass

        if re.findall("拒绝后", step):
            agent_refuse_reason = Ca().xpath_text_(
                xpath_front + '/div/div[1]/div[2]/div[1]/div[10]/div[2]')
            self.check_information_if('其他 金额部分', agent_refuse_reason, "代理方拒绝理由", step)
            agent_refuse_details = Ca().xpath_text_(
                xpath_front + '/div/div[1]/div[2]/div[1]/div[11]/div[2]')
            self.check_information_if('fkl', agent_refuse_details, "代理方拒绝详情", step)
            gl.set_value('agent_refuse_reason', agent_refuse_reason)
            gl.set_value('agent_refuse_details', agent_refuse_details)
            # print('agent_refuse_reason=%s' % agent_refuse_details)
            # print('agent_refuse_reason=%s' % agent_refuse_reason)

    # 获取并校验fahuo详情页面信息
    def details_information_2(self, driver, step):
        contractnumber = gl.get_value('contractnumber')
        their_service_charge = gl.get_value('their_service_charge')
        invoiceApplySn = gl.get_value('invoiceApplySn')
        purchaser_name = gl.get_value('purchaser_name')
        supplier_name = gl.get_value('supplier_name')
        our_service_charge = gl.get_value('our_service_charge')
        price_sum_check_all_2 = gl.get_value('price_sum_check_all_2')

        invoiceApplySn_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[1]/div[2]')
        self.check_information_if(invoiceApplySn, invoiceApplySn_1, "发货申请单号", step)

        contractnumber_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[2]/div[2]')
        self.check_information_if(contractnumber, contractnumber_1, "委托申请单号", step)

        purchaser_name_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[3]/div[2]/a')
        self.check_information_if(purchaser_name, purchaser_name_1, "采购方名称", step)

        supplier_name_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[4]/div[2]/a')
        self.check_information_if(supplier_name, supplier_name_1, "销售方名称", step)

        our_service_charge_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[5]/div[2]')
        self.check_information_re(our_service_charge, our_service_charge_1, "我方服务费", step)

        their_service_charge_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[6]/div[2]')
        self.check_information_re(their_service_charge, their_service_charge_1, "他方服务费", step)

        full_price_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[7]/div[2]')
        self.check_information_re(price_sum_check_all_2, full_price_1, "商品总金额", step)

        procurement_audit_time_1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[2]/div[1]/div[8]/div[2]')
        self.check_information_time(procurement_audit_time_1, "合作方审核时间", step)

        if re.findall("通过", step) or re.findall("拒绝后", step):
            agent_audit_time_1 = Ca().xpath_text_(
                xpath_front + '/div/div[1]/div[2]/div[1]/div[9]/div[2]')
            self.check_information_time(agent_audit_time_1, "代理方审核时间", step)
            if re.findall("test", self.start_url):
                agent_refuse_reason = Ca().xpath_text_(
                    xpath_front + '/div/div[1]/div[2]/div[1]/div[10]/div[2]')
                self.check_information_if('13245678999_s', agent_refuse_reason, "代理商审核人员", step)
            else:
                agent_refuse_reason = Ca().xpath_text_(
                    xpath_front + '/div/div[1]/div[2]/div[1]/div[10]/div[2]')
                self.check_information_if('18373847538_s', agent_refuse_reason, "代理商审核人员", step)

    # 获取并校验合同详情页的合同内容
    def contract_content(self, driver, step):
        # 获取并校验iframe合同中的内容
        # 使用iframe
        # driver.switch_to_frame('SWIframeId')

        # apply_number 发起申请编号   price_sum_check_all_1=4000  price_single_1 = 4000 price_sum_check_all_2 =10000,
        # price_many_2 = 6000
        purchaser_name = gl.get_value('purchaser_name')
        purchaser_926 = gl.get_value('purchaser_926')
        purchaser_email = gl.get_value('purchaser_email')
        # purchaser_phone = gl.get_value('purchaser_phone')
        purchaser_address = gl.get_value('purchaser_address')  # 获取采购方地址
        purchaser_email = gl.get_value('purchaser_email')  # 获取采购方邮箱
        purchaser_bank = gl.get_value('purchaser_bank')  # 获取采购方开户银行
        purchaser_account = gl.get_value('purchaser_account')  # 获取采购方银行账号

        agent_name = gl.get_value('agent_name')
        agent_926 = gl.get_value('agent_926')
        agent_email = gl.get_value('agent_email')
        agent_phone = gl.get_value('agent_phone')

        supplier_name = gl.get_value('supplier_name')
        supplier_926 = gl.get_value('supplier_926')
        supplier_email = gl.get_value('supplier_email')
        # supplier_phone = gl.get_value('supplier_phone')
        supplier_address = gl.get_value('supplier_address')  # 获取供应方地址
        supplier_email = gl.get_value('supplier_email')  # 获取供应方邮箱
        supplier_bank = gl.get_value('supplier_bank')  # 获取供应方开户银行
        supplier_account = gl.get_value('supplier_account')  # 获取供应方银行账号

        price_single_1 = gl.get_value('price_single_1')
        price_sum_check_all_1 = gl.get_value('price_sum_check_all_1')
        price_sum_check_all_2 = gl.get_value('price_sum_check_all_2')
        price_many_2 = gl.get_value('price_many_2')
        apply_number = gl.get_value('apply_number')

        x = 2
        purchaser_name_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (39 + x))
        print(purchaser_name_1)
        self.check_information_if(purchaser_name, purchaser_name_1, "合同内容中采购（甲）方公司名称", step)
        purchaser_926_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (43 + x))
        self.check_information_if(purchaser_926, purchaser_926_1, "合同内容中采购（甲）方公司926链号", step)
        purchaser_contacts_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (47 + x))
        self.check_information_if('东方联系人', purchaser_contacts_1, "合同内容中采购（甲）方联系人", step)
        purchaser_phone_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (50 + x))
        self.check_information_if('东方联系号码', purchaser_phone_1, "合同内容中采购（甲）方号码", step)
        purchaser_email_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (54 + x))
        self.check_information_if(purchaser_email, purchaser_email_1, "合同内容中采购（甲）方邮箱", step)
        purchaser_address_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (58 + x))
        self.check_information_if(purchaser_address, purchaser_address_1, "合同内容中采购（甲）方地址", step)
        purchaser_bank_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (62 + x))
        self.check_information_if(purchaser_bank, purchaser_bank_1, "合同内容中采购（甲）方开户行", step)
        purchaser_account_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (66 + x))
        self.check_information_if(purchaser_account, purchaser_account_1, "合同内容中采购（甲）方账号", step)

        agent_name_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (40 + x))
        self.check_information_if(agent_name, agent_name_1, "合同内容中代理（乙）方公司名称", step)
        agent_926_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (44 + x))
        self.check_information_if(agent_926, agent_926_1, "合同内容中代理（乙）方公司926链号", step)
        # agent_contacts_1 = Ca().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (48+x) ).text
        # self.check_information_if('天河联系人', agent_contacts_1, "合同内容中代理（乙）方联系人", step)
        agent_phone_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (51 + x))
        self.check_information_if('18823772926', agent_phone_1, "合同内容中代理（乙）方号码", step)
        agent_email_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (55 + x))
        self.check_information_if('926@926.net.cn', agent_email_1, "合同内容中代理（乙）方邮箱", step)
        # agent_address_1 = Ca().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (59+x) ).text
        # self.check_information_if(agent_address, agent_address_1, "合同内容中代理（乙）方地址", step)
        agent_bank_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (63 + x))
        self.check_information_if('招商银行股份有限公司深圳科发支行', agent_bank_1, "合同内容中代理（乙）方开户行", step)
        agent_account_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (67 + x))
        self.check_information_if('755940017210601', agent_account_1, "合同内容中代理（乙）方账号", step)

        supplier_name_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (41 + x))
        self.check_information_if(supplier_name, supplier_name_1, "合同内容中销售（丙）方公司名称", step)
        supplier_926_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (45 + x))
        self.check_information_if(supplier_926, supplier_926_1, "合同内容中销售（丙）方公司926链号", step)
        supplier_contacts_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (48 + x))
        self.check_information_if('天河联系人', supplier_contacts_1, "合同内容中销售（丙）方联系人", step)
        supplier_phone_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (52 + x))
        self.check_information_if('天河联系号码', supplier_phone_1, "合同内容中销售（丙）方号码", step)
        supplier_email_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (56 + x))
        self.check_information_if(supplier_email, supplier_email_1, "合同内容中销售（丙）方邮箱", step)
        supplier_address_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (60 + x))
        self.check_information_re(supplier_address_1, supplier_address, "合同内容中销售（丙）方地址", step)
        supplier_bank_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (64 + x))
        self.check_information_if(supplier_bank, supplier_bank_1, "合同内容中销售（丙）方开户行", step)
        supplier_account_1 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (68 + x))
        self.check_information_if(supplier_account, supplier_account_1, "合同内容中销售（丙）方账号", step)

        contractnumber = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (1))

        number1 = gl.get_value('number1')
        number2 = gl.get_value('number2')
        price1 = gl.get_value('price1')
        price2 = gl.get_value('price2')
        amount_1 = gl.get_value('amount_1')
        amount_2 = gl.get_value('amount_2')
        total_Amount = gl.get_value('total_Amount')
        goods_name = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (77 + x))
        self.check_information_if("接线盒盖毛坯", goods_name, "合同内容中一类商品名称", step)

        # specifications = Ca().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (78+x) ).text
        # self.check_information_if("", specifications, "合同内容中商品规格", step)

        number = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (78 + x))
        self.check_information_if("%s(件)" % number1, number, "合同内容中一类商品数量", step)

        unit_price = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (79 + x))
        self.check_information_if(str(price1), unit_price, "合同内容中一类商品单价", step)

        total_price = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (80 + x))
        self.check_information_if(amount_1, total_price, "合同内容中一类商品总价", step)

        goods_name = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (82 + x))
        self.check_information_if("接线盒盖", goods_name, "合同内容中二类商品名称", step)

        specifications = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (83 + x))
        self.check_information_if("TF", specifications, "二类合同内容中二类商品规格", step)

        number222 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (84 + x))
        self.check_information_if("%s(件)" % number2, number222, "合同内容中二类商品数量", step)

        unit_price2 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (85 + x))
        self.check_information_if(str(price2), unit_price2, "合同内容中二类商品单价", step)

        total_price2 = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (86 + x))
        self.check_information_if(amount_2, total_price2, "合同内容中二类商品总价", step)

        full_price = Ca().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (100))
        self.check_information_if(str(total_Amount), full_price, "合同内容中商品总价", step)

        zufs = Ca().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (25 + x))
        self.check_information_re("货到开银行承兑汇票", zufs, "合同内容中支付方式", step)

        # 释放iframe
        # driver.switch_to_default_content()

        # Ca().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[3]', "点击查看申请信息",
        #                   step, "云平台‘发起方’", sys._getframe().f_lineno)
        # time.sleep(1)
        # purchaser_name_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]')
        # self.check_information_if(purchaser_name, purchaser_name_2, "采购（甲）方公司名称", step)
        #
        # purchaser_926_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]')
        # self.check_information_if(purchaser_926, purchaser_926_2, "采购（甲）方公司926链号", step)
        # purchaser_email_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[2]')
        # self.check_information_if(purchaser_email, purchaser_email_2, "采购（甲）方邮箱", step)
        # purchaser_contacts_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[4]/div/div[2]')
        # self.check_information_if('东方联系人', purchaser_contacts_2, "采购（甲）方联系人", step)
        # purchaser_phone_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[5]/div/div[2]')
        # self.check_information_if('东方联系号码', purchaser_phone_2, "采购（甲）方联系号码", step)
        #
        # agent_name_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[2]')
        # self.check_information_if(agent_name, agent_name_2, "代理（乙）方公司名称", step)
        # agent_926_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[2]')
        # self.check_information_if(agent_926, agent_926_2, "代理（乙）方公司名称", step)
        # agent_email_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[3]/div/div[2]')
        # self.check_information_if(agent_email_1, agent_email_2, "代理（乙）方邮箱", step)
        #
        # # agent_contacts_2 = Ca().xpath_text_(
        # #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[4]/div/div[2]')
        # # self.check_information_if('朱丹', agent_contacts_2, "代理（乙）方联系人", step)
        #
        # agent_phone = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[5]/div/div[2]')
        # self.check_information_if(agent_phone_1, agent_phone, "代理（乙）方联系电话", step)
        #
        # supplier_name_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[1]/div/div[2]')
        # self.check_information_if("(发起方)%s" % supplier_name, supplier_name_2, "销售方（丙）方公司名称", step)
        #
        # supplier_926_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[2]/div/div[2]')
        # self.check_information_if(supplier_926, supplier_926_2, "销售方（丙）方公司926链号", step)
        #
        # supplier_email_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[3]/div/div[2]')
        # self.check_information_if(supplier_email, supplier_email_2, "销售方（丙）方邮箱", step)
        #
        # supplier_contacts_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[4]/div/div[2]')
        # self.check_information_if('天河联系人', supplier_contacts_2, "销售方（丙）方联系人", step)
        #
        # supplier_phone_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[5]/div/div[2]')
        # self.check_information_if('天河联系号码', supplier_phone_2, "销售方（丙）方电话", step)
        #
        # Ca().slide_("500")
        # picture_1 = Ca().xpath_href_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]'
        #                   '/div[2]/div[1]/span/div[1]/div/div/span/a[1]')
        #
        # self.check_information_re("625b4822e90d95601e40dcdf7335b7ac.jpg", picture_1, "合同图片信息", step)
        #
        # protocolSignTimeStr = gl.get_value('protocolSignTimeStr')
        # protocolNumber = gl.get_value('protocolNumber')
        # deliveryTypeName = gl.get_value('deliveryTypeName')
        # secondPaymentTypeName = gl.get_value('secondPaymentTypeName')
        # receiptTerm = gl.get_value('receiptTerm')
        # secondAcceptanceDraftTimeTypeName = gl.get_value('secondAcceptanceDraftTimeTypeName')
        # thirdReceiptTimeTypeName = gl.get_value('thirdReceiptTimeTypeName')
        # thirdReceiptTimeNum = gl.get_value('thirdReceiptTimeNum')
        # contract_mark = gl.get_value('contract_mark')
        # contract_mark = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[2]')
        # self.check_information_if("62284844935", contract_mark, "原始合同编号", step)
        # gl.set_value('contract_mark', contract_mark)
        # # price_sum = Ca().xpath_text_(
        # #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div/div[2]')
        # # self.check_information_re(total_Amount, price_sum, "商品总价", step)
        #
        # protocolSignTimeStr = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[1]/div')
        # self.check_information_re('20', protocolSignTimeStr, "协议签订日期", step)
        # protocolNumber = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]')
        # self.check_information_re('xybh', protocolNumber, "协议编号", step)
        # deliveryTypeName = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[3]/div/div[2]')
        # self.check_information_re('甲方自提', deliveryTypeName, "交货方式", step)
        # secondPaymentTypeName = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[4]/div/div[2]')
        # self.check_information_re('银行承兑汇票', secondPaymentTypeName, "乙方付款方式:", step)
        # receiptTerm = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[1]/div/div[2]')
        # self.check_information_re('5个月', receiptTerm, "汇票期限:", step)
        # secondAcceptanceDraftTimeTypeName = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[2]/div/div[2]')
        # self.check_information_re('货到开银行承兑汇票', secondAcceptanceDraftTimeTypeName, "乙方开承兑汇票时间:", step)
        # thirdReceiptTimeTypeName = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[3]/div/div[2]')
        # self.check_information_re('乙方开银行承兑汇票前', thirdReceiptTimeTypeName, "*丙方开发票时间:", step)
        # thirdReceiptTimeNum = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[4]/div/div[2]')
        # self.check_information_re('150天', thirdReceiptTimeNum, "乙方开银行承兑汇票前:", step)
        # Ca().slide_('750')
        # price_sum = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[4]/div/div[2]')
        # self.check_information_re(str(total_Amount), price_sum, "商品总价", step)
        #
        # cooperation_time = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[3]/div/div[2]')
        # self.check_information_time(cooperation_time, "合作方审签时间", step)
        # contractnumber_2 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[4]/div/div[2]')
        # self.check_information_if(contractnumber, contractnumber_2, "合同编号", step)
        #
        # Ca().slide_("0")
        # Ca().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[2]', "点击查看附件信息",
        #                   step, "云平台‘采购方’", sys._getframe().f_lineno)
        # picture_2 = Ca().xpath_href_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]/span'
        #                   '/div[1]/div/div/span/a[1]')
        # self.check_information_re(picture_1, picture_2, "原始合同图片", step)
        #
        # contract_mark_1 = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[2]')
        # self.check_information_if("62284844935", contract_mark_1, "原始合同编号", step)
        # settlement_date = gl.get_value('settlement_date')
        # settlement = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[3]/div/div[2]')
        # self.check_information_if(settlement_date, settlement, "结算方式", step)

    def login(self):
        driver = self.driver
        start_url = self.start_url
        driver.get(start_url)
        Ca().name_click_("ant-menu-item", "点击密码登录", "登录", "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().id_clear_("手机号")
        if re.findall('test', start_url):
            Ca().id_send_("手机号", "13245678900")  # 测试
            Ca().is_toast_exist("输入正确的手机号", "登录", "云平台‘代理方’", sys._getframe().f_lineno)
        elif re.findall('10.', start_url):  # 开发
            Ca().id_send_("手机号", "13245678999")  # 开发
            Ca().is_toast_exist("输入正确的手机号", "登录", "云平台‘代理方’", sys._getframe().f_lineno)
        elif re.findall('pre', start_url):  # 预生产
            Ca().id_send_("手机号", "13245678999")  # 生产测试账号 18373847538   生产通用账号 13245678999
            Ca().is_toast_exist("输入正确的手机号", "登录", "云平台‘代理方’", sys._getframe().f_lineno)
        else:  #生产
            Ca().id_send_("手机号", "18373847538")  # 生产测试账号 18373847538
            Ca().is_toast_exist("输入正确的手机号", "登录", "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().id_clear_("密码")
        Ca().id_send_("密码", "123456")
        Ca().is_toast_exist("输入正确的密码", "登录", "云平台‘代理方’", sys._getframe().f_lineno)
        # 登陆
        Ca().xpath_click_("//button[@class='ant-btn login-form-button ant-btn-primary']", "点击登录", "登录",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(1.5)
        Ca().text_click_("代理交易助手", "进入代理交易助手", "登录", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        catalog = Ca().xpath_text_('//*[@id="0$Menu"]/li[1]', sys._getframe().f_lineno)
        self.check_information_if("业务认证", catalog, "成功进入代理交易助手", "进入代理交易助手")

    def customer_management(self):
        print("*****代理方查看客户信息*****")
        driver = Ca().driver
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方企业名
        Ca().xpath_click_('//*[@id="8$Menu"]/li', "点击进入客户列表", "代理方查看客户信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)
        print('supplier_name %s' % supplier_name)
        driver.find_element_by_xpath('//*[@id="keywords"]').clear()
        Ca().xpath_send_('//*[@id="keywords"]','天河软件', "搜索销售方", "代理方查看客户信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front +'/div/div/div[1]/form/div[2]/div[2]/button', "点击搜索", "代理方查看客户信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front +'/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[5]/a/button',
                                     "点击进入丙（销售)  方企业", "进入通过签审后的丙（销售)  方客户信息", "云平台‘代理方’", sys._getframe().f_lineno)
        # customer_number = Ca().xpath_text_(
        #     xpath_front + '/div/div/div[2]/div/div/ul/li[1]')  # 获取列表中的企业总数
        # customer_number = re_int1(customer_number)
        # for i in range(1, customer_number):  # 遍历页面，获取相应的企业名
        #     if i < 11:
        #         name_1 = Ca().xpath_text_(
        #             xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr[%s]/td[1]' % i)  # 获取列表中的企业名
        #         # print(name_1)
        purchaser_email = gl.get_value('purchaser_email')  # 甲（采购）方邮箱
        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaser_926 = gl.get_value('purchaser_926')  # 甲（采购）方926链号
        purchaser_bank = gl.get_value('purchaser_bank')  # 采购（甲）方开户行
        purchaser_account = gl.get_value('purchaser_account', )  # 采购（甲）方账号
        supplier_926 = gl.get_value('supplier_926')  # 丙（销售)  #方926链号
        supplier_email = gl.get_value('supplier_email')  # 丙（销售)  #方邮箱
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方企业名
        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)方电话
        supplier_bank = gl.get_value('supplier_bank')  # 销售方（丙）开户行
        supplier_account = gl.get_value('supplier_account')  # 销售方（丙）方账号
        # Ca().xpath_click_(
        #     xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr[%s]/td[5]/a/button' % i,
        #     "点击进入丙（销售)  方企业", "进入通过签审后的丙（销售)  方客户信息", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(3)
        name_2 = Ca().xpath_text_('//*[@id="name"]')
        self.check_information_if(supplier_name, name_2, "企业名-详情页", "进入通过签审后的丙（销售)  方客户信息")
        supplier_926_1 = Ca().xpath_text_('//*[@id="accountSn"]')
        self.check_information_if(supplier_926, supplier_926_1, "企业926链号-详情页", "进入通过签审后的丙（销售)  方客户信息")
        industry = Ca().xpath_text_('//*[@id="industry"]')
        self.check_information_if('制造加工', industry, "企业所属行业-详情页", "进入通过签审后的丙（销售)  方客户信息")
        region = Ca().xpath_text_('//*[@id="region"]')
        self.check_information_if('浙江省杭州市余杭区', region, "企业所在地区详情页", "进入通过签审后的丙（销售)  方客户信息")
        phone = Ca().xpath_text_('//*[@id="phone"]')
        self.check_information_if(supplier_phone, phone, "企业电话", "进入通过签审后的丙（销售)  方客户信息")
        email = Ca().xpath_text_('//*[@id="email"]')
        self.check_information_if(supplier_email, email, "企业email", "进入通过签审后的丙（销售)  方客户信息")
        bankAccountName = Ca().xpath_text_('//*[@id="bankAccountName"]')
        self.check_information_if("哼1", bankAccountName, "企业开户名称", "进入通过签审后的丙（销售)  方客户信息")
        depositBank = Ca().xpath_text_('//*[@id="depositBank"]')
        self.check_information_if(supplier_bank, depositBank, "企业开户行", "进入通过签审后的丙（销售)  方客户信息")
        bankRegion = Ca().xpath_text_('//*[@id="bankRegion"]')
        self.check_information_if('甘肃省定西市陇西县', bankRegion, "企业开户行", "进入通过签审后的丙（销售)  方客户信息")
        bankAccount = Ca().xpath_text_('//*[@id="bankAccount"]')
        self.check_information_if(supplier_account, bankAccount, "企业开户账号", "进入通过签审后的丙（销售)  方客户信息")

        totalCreditQuota_supplier_1 = Ca().xpath_text_('//*[@id="totalCreditQuota"]/div/span')
        totalCreditQuota_supplier = re_sub_(totalCreditQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        totalCirculationQuota_supplier_1 = Ca().xpath_text_(
            '//*[@id="totalCirculationQuota"]/div/span')
        totalCirculationQuota_supplier = re_sub_(totalCirculationQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        totalQuota_supplier_1 = Ca().xpath_text_('//*[@id="totalQuota"]/div')
        totalQuota_supplier = re_sub_(totalQuota_supplier_1)  # 显示为xx,xxx.00 正则筛
        totalOccupyCreditQuota_supplier_1 = Ca().xpath_text_(
            '//*[@id="totalOccupyCreditQuota"]/div/span')
        totalOccupyCreditQuota_supplier = re_sub_(totalOccupyCreditQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        totalOccupyCirculationQuota_supplier_1 = Ca().xpath_text_(
            '//*[@id="totalOccupyCirculationQuota"]/div/span')
        totalOccupyCirculationQuota_supplier = re_sub_(
            totalOccupyCirculationQuota_supplier_1)  # 显示为xx,xxx.00 正则筛

        totalFrozenCreditQuota_supplier_1 = Ca().xpath_text_(
            '//*[@id="totalFrozenCreditQuota"]/div/span')
        totalFrozenCreditQuota_supplier = re_sub_(totalFrozenCreditQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选

        totalFrozenCirculationQuota_supplier_1 = Ca().xpath_text_(
            '//*[@id="totalFrozenCirculationQuota"]/div/span')
        totalFrozenCirculationQuota_supplier = re_sub_(
            totalFrozenCirculationQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选

        totalOccupancyCreditQuota_supplier_1 = Ca().xpath_text_(
            '//*[@id="totalOccupancyCreditQuota"]/div')
        totalOccupancyCreditQuota_supplier = re_sub_(
            totalOccupancyCreditQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选

        totalOccupancyCirculationQuota_supplier_1 = Ca().xpath_text_(
            '//*[@id="totalOccupancyCirculationQuota"]/div')
        totalOccupancyCirculationQuota_supplier = re_sub_(
            totalOccupancyCirculationQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        contactEffectiveNum_supplier_1 = Ca().xpath_text_('//*[@id="contactEffectiveNum"]/div')
        contactEffectiveNum_supplier = re_sub_(contactEffectiveNum_supplier_1)  # 显示为xx,xxx.00 正则筛选

        loanHistoryNum_supplier_1 = Ca().xpath_text_('//*[@id="loanHistoryNum"]/div')
        loanHistoryNum_supplier = re_sub_(loanHistoryNum_supplier_1)  # 显示为xx,xxx.00 正则筛选

        gl.set_value('totalCreditQuota_supplier', totalCreditQuota_supplier)  # 丙 总授信云票"
        gl.set_value('totalCirculationQuota_supplier', totalCirculationQuota_supplier)  # 丙 总流转云票"
        gl.set_value('totalQuota_supplier', totalQuota_supplier)  # 丙 总云票 （授信+流转）
        gl.set_value('totalOccupyCreditQuota_supplier', totalOccupyCreditQuota_supplier)  # 丙 已占用授信云票
        gl.set_value('totalOccupyCirculationQuota_supplier',
                     totalOccupyCirculationQuota_supplier)  # 丙 已占用流转云票
        gl.set_value('totalFrozenCreditQuota_supplier', totalFrozenCreditQuota_supplier)  # 丙 获取已冻结授信云票
        gl.set_value('totalFrozenCirculationQuota_supplier',
                     totalFrozenCirculationQuota_supplier)  # 丙 已冻结流转云票
        gl.set_value('totalOccupancyCreditQuota_supplier',
                     totalOccupancyCreditQuota_supplier)  # 丙 可用总授信(总-已用)
        gl.set_value('totalOccupancyCirculationQuota_supplier',
                     totalOccupancyCirculationQuota_supplier)  # 丙 余总流转(总-已用
        gl.set_value('contactEffectiveNum_supplier', contactEffectiveNum_supplier)  # 生效委托申请单
        gl.set_value('loanHistoryNum_supplier', loanHistoryNum_supplier)  # 贷现历史次数

        print('丙 总授信云票：%s' % totalCreditQuota_supplier)
        print('丙 总流转云票：%s' % totalCirculationQuota_supplier)
        print('丙 总云票 （授信+流转）：%s' % totalQuota_supplier)
        print('丙 已占用授信云票：%s' % totalOccupyCreditQuota_supplier)
        print('丙 已占用流转云票：%s' % totalOccupyCirculationQuota_supplier)
        print('丙 获取已冻结授信云票：%s' % totalFrozenCreditQuota_supplier)
        print('丙 已冻结流转云票：%s' % totalFrozenCirculationQuota_supplier)
        print('丙 可用总授信(总-已用)：%s' % totalOccupancyCreditQuota_supplier)
        print('丙 余总流转(总-已用：%s' % totalOccupancyCirculationQuota_supplier)
        print('丙 生效委托申请单：%s' % contactEffectiveNum_supplier)
        print('丙 贷现历史次数：%s' % loanHistoryNum_supplier)

        Ca().xpath_click_('//*[@id="8$Menu"]/li', "点击进入客户列表", "查看通过签审后的客户信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)

        driver.find_element_by_xpath('//*[@id="keywords"]').clear()
        Ca().xpath_send_('//*[@id="keywords"]', '新东方', "搜索采购方", "代理方查看客户信息", "云平台‘代理方’",
                                    sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front + '/div/div/div[1]/form/div[2]/div[2]/button', "点击搜索", "代理方查看客户信息",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[5]/a/button',
                                     "点击进入丙（销售)  方企业", "进入通过签审后的丙（采购)  方客户信息", "云平台‘代理方’", sys._getframe().f_lineno)
        print('purchaser_name %s ' % purchaser_name)
        time.sleep(3)
        name_2 = Ca().xpath_text_('//*[@id="name"]')
        self.check_information_if(purchaser_name, name_2, "企业名-详情页", "进入通过签审后的甲（采购）方企业信息")
        purchaser_926_1 = Ca().xpath_text_('//*[@id="accountSn"]')
        self.check_information_if(purchaser_926, purchaser_926_1, "企业926链号-详情页", "进入通过签审后的甲（采购）方企业信息")
        industry = Ca().xpath_text_('//*[@id="industry"]')
        self.check_information_if('家具/室内设计/装饰装潢', industry, "企业所属行业-详情页", "进入通过签审后的甲（采购）方企业信息")
        region = Ca().xpath_text_('//*[@id="region"]')
        self.check_information_if('北京市北京市东城区', region, "企业所在地区详情页", "进入通过签审后的甲（采购）方企业信息")
        phone = Ca().xpath_text_('//*[@id="phone"]')
        self.check_information_if(purchaser_phone, phone, "企业电话", "进入通过签审后的甲（采购）方企业信息")
        email = Ca().xpath_text_('//*[@id="email"]')
        self.check_information_if(purchaser_email, email, "企业email", "进入通过签审后的甲（采购）方企业信息")
        bankAccountName = Ca().xpath_text_('//*[@id="bankAccountName"]')
        self.check_information_if("3761", bankAccountName, "企业开户名称", "进入通过签审后的甲（采购）方企业信息")
        depositBank = Ca().xpath_text_('//*[@id="depositBank"]')
        self.check_information_if(purchaser_bank, depositBank, "企业开户行", "进入通过签审后的甲（采购）方企业信息")
        bankRegion = Ca().xpath_text_('//*[@id="bankRegion"]')
        self.check_information_if('北京市北京市东城区', bankRegion, "企业开户行", "进入通过签审后的甲（采购）方企业信息")
        bankAccount = Ca().xpath_text_('//*[@id="bankAccount"]')
        self.check_information_if(purchaser_account, bankAccount, "企业开户账号", "进入通过签审后的甲（采购）方企业信息")

        totalCreditQuota_purchaser_1 = Ca().xpath_text_('//*[@id="totalCreditQuota"]/div/span')
        totalCreditQuota_purchaser = re_sub_(totalCreditQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        totalCirculationQuota_purchaser_1 = Ca().xpath_text_(
            '//*[@id="totalCirculationQuota"]/div/span')
        totalCirculationQuota_purchaser = re_sub_(totalCirculationQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        totalQuota_purchaser_1 = Ca().xpath_text_('//*[@id="totalQuota"]/div')
        totalQuota_purchaser = re_sub_(totalQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛

        totalOccupyCreditQuota_purchaser_1 = Ca().xpath_text_(
            '//*[@id="totalOccupyCreditQuota"]/div/span')
        totalOccupyCreditQuota_purchaser = re_sub_(totalOccupyCreditQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        totalOccupyCirculationQuota_purchaser_1 = Ca().xpath_text_(
            '//*[@id="totalOccupyCirculationQuota"]/div/span')
        totalOccupyCirculationQuota_purchaser = re_sub_(
            totalOccupyCirculationQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        totalFrozenCreditQuota_purchaser_1 = Ca().xpath_text_(
            '//*[@id="totalFrozenCreditQuota"]/div/span')
        totalFrozenCreditQuota_purchaser = re_sub_(totalFrozenCreditQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        totalFrozenCirculationQuota_purchaser_1 = Ca().xpath_text_(
            '//*[@id="totalFrozenCirculationQuota"]/div/span')
        totalFrozenCirculationQuota_purchaser = re_sub_(
            totalFrozenCirculationQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        totalOccupancyCreditQuota_purchaser_1 = Ca().xpath_text_(
            '//*[@id="totalOccupancyCreditQuota"]/div')
        totalOccupancyCreditQuota_purchaser = re_sub_(
            totalOccupancyCreditQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        totalOccupancyCirculationQuota_purchaser_1 = Ca().xpath_text_(
            '//*[@id="totalOccupancyCirculationQuota"]/div')
        totalOccupancyCirculationQuota_purchaser = re_sub_(
            totalOccupancyCirculationQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        contactEffectiveNum_purchaser_1 = Ca().xpath_text_('//*[@id="contactEffectiveNum"]/div')
        contactEffectiveNum_purchaser = re_sub_(contactEffectiveNum_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        loanHistoryNum_purchaser_1 = Ca().xpath_text_('//*[@id="loanHistoryNum"]/div')
        loanHistoryNum_purchaser = re_sub_(loanHistoryNum_purchaser_1)  # 显示为xx,xxx.00 正则筛选

        gl.set_value('totalCreditQuota_purchaser', totalCreditQuota_purchaser)  # 甲 采购总授信云票"
        gl.set_value('totalCirculationQuota_purchaser', totalCirculationQuota_purchaser)  # 甲 采购总流转云票"
        gl.set_value('totalQuota_purchaser', totalQuota_purchaser)  # 甲 总云票 （授信+流转）
        gl.set_value('totalOccupyCreditQuota_purchaser', totalOccupyCreditQuota_purchaser)  # jia 已占用授信云票
        gl.set_value('totalOccupyCirculationQuota_purchaser',
                     totalOccupyCirculationQuota_purchaser)  # jia 已占用流转云票
        gl.set_value('totalFrozenCreditQuota_purchaser', totalFrozenCreditQuota_purchaser)  # jia 获取已冻结授信云票
        gl.set_value('totalFrozenCirculationQuota_purchaser',
                     totalFrozenCirculationQuota_purchaser)  # jia 已冻结流转云票
        gl.set_value('totalOccupancyCreditQuota_purchaser',
                     totalOccupancyCreditQuota_purchaser)  # jia 可用总授信(总-已用)
        gl.set_value('totalOccupancyCirculationQuota_purchaser',
                     totalOccupancyCirculationQuota_purchaser)  # jia 余总流转(总-已用
        gl.set_value('contactEffectiveNum_purchaser', contactEffectiveNum_purchaser)  # 生效委托申请单
        gl.set_value('loanHistoryNum_purchaser', loanHistoryNum_purchaser)  # 贷现历史次数

        print('甲 总授信云票：%s' % totalCreditQuota_purchaser)
        print('甲 总流转云票：%s' % totalCirculationQuota_purchaser)
        print('甲 总云票 （授信+流转）：%s' % totalQuota_purchaser)
        print('甲 已占用授信云票：%s' % totalOccupyCreditQuota_purchaser)
        print('甲 已占用流转云票：%s' % totalOccupyCirculationQuota_purchaser)
        print('甲 获取已冻结授信云票：%s' % totalFrozenCreditQuota_purchaser)
        print('甲 已冻结流转云票：%s' % totalFrozenCirculationQuota_purchaser)
        print('甲 可用总授信(总-已用)：%s' % totalOccupancyCreditQuota_purchaser)
        print('甲 余总流转(总-已用：%s' % totalOccupancyCirculationQuota_purchaser)
        print('甲 生效委托申请单：%s' % contactEffectiveNum_purchaser)
        print('甲 贷现历史次数：%s' % loanHistoryNum_purchaser)

        Ca().xpath_click_('//*[@id="8$Menu"]/li', "点击进入客户列表", "查看通过签审后的客户信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)

    def refuse_entrust(self):  # 代理方拒绝委托
        driver = Ca().driver

        Ca().slide_("0")
        print("*****代理方查看拒绝前已收到的合同*****")
        Ca().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击进入委托申请", "查看拒绝前已收到的合同", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)
        self.list_four(driver, "全部", "待审核", "已审核", "未通过", "查看拒绝前已收到的合同", "委托申请-全部列表",
                       "委托申请-待审核列表", "委托申请-已审核列表", "委托申请-未通过列表")

        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击进入待审核",
                                     "查看拒绝前已收到的合同", "云平台‘代理方’", sys._getframe().f_lineno)

        apply_number = gl.get_value('apply_number')
        apply_number_2 = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘待审批列表’创建编号", "查看拒绝前已收到的合同")
        a_time_2 = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_time(a_time_2, "‘待审批列表’提交时间", "查看拒绝前已收到的合同")
        agent_list_state = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/b')
        self.check_information_if("待审核", agent_list_state, "‘待审批列表’状态", "查看拒绝前已收到的合同")
        gl.set_value('agent_list_state', agent_list_state)
        time.sleep(2.5)
        Ca().xpath_click_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击操作", "查看拒绝前已收到的合同",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_two(driver, "委托申请", "委托申请详情", "查看拒绝前已收到的合同", "合同详情一级目录", "合同详情二级目录")
        # 校验详情页面信息
        print("*****查看拒绝前页面详情信息****")
        self.details_information(driver, "查看拒绝前已收到的合同")
        Ca().slide_("100")
        # 校验合同内容信息
        print("*****查看拒绝前合同内容信息****")
        self.contract_content(driver, "查看拒绝前已收到的合同")
        time.sleep(1.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[3]/div/div[1]/div/div/div/div/div[1]/div[4]',
                                     "点击操作记录", "查看拒绝前已收到的合同", "云平台‘代理方’", sys._getframe().f_lineno)
        purchaser_name = gl.get_value('purchaser_name')
        start_url = self.start_url
        if re.findall('test', start_url):
            self.Operation_record(driver, "合作方同意合同申请", "%s 18474793371_s"%purchaser_name, "查看拒绝前已收到的合同",
                                  "查看拒绝前已收到的合同的操作状态", "查看拒绝前已收到的合同的操作时间", "拒绝前已收到的合同的操作者信息")
        else:
            self.Operation_record(driver, "合作方同意合同申请", "%s 18474793371_s"%purchaser_name, "查看拒绝前已收到的合同",
                                  "查看拒绝前已收到的合同的操作状态", "查看拒绝前已收到的合同的操作时间", "拒绝前已收到的合同的操作者信息")

        print("****代理方拒绝签审合同*****")
        Ca().xpath_click_('//*[@id="RightRouteDiv"]/div/div/div/div[2]/div/div[1]/div[2]/div[2]/span/button[2]', "点击拒绝", "查看拒绝前已收到的合同",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2)
        Ca().xpath_click_('//div[@class="ant-modal-body"]/div/div[1]/div/div/button[2]',
                          "选择拒绝标签1", "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)

        Ca().xpath_click_('//div[@class="ant-modal-body"]/div/div[1]/div/div/button[3]'
                          , "选择拒绝标签2", "代采方拒绝发货申请", "云平台‘采购方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Ca().xpath_click_('//textarea[@class="ant-input"]', "点击拒绝理由", "查看拒绝前已收到的合同", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(0.5)
        Ca().xpath_send_('//textarea[@class="ant-input"]', "fkl")
        Ca().is_toast_exist("输入拒绝理由", "查看拒绝前已收到的合同", "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_click_('//div[@class="ant-modal-footer"]/span/button[2]', "点击确认",
                                     "查看拒绝前已收到的合同", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(1)
        Ca().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认",
                                     "查看拒绝前已收到的合同", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(3)
        print("*****代理方查看拒绝后的合同信息*****")

        Ca().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击进入委托申请", "查看拒绝后的合同信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        #
        self.list_four(driver, "全部", "待审核", "已审核", "未通过", "查看拒绝后的合同信息", "委托申请-全部列表",
                       "委托申请-待审核列表", "委托申请-已审核列表", "委托申请-未通过列表")
        #
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]', "点击进入未通过",
                                     "查看拒绝后的合同信息", "云平台‘代理方’", sys._getframe().f_lineno)

        apply_number = gl.get_value('apply_number')
        apply_number_2 = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘未通过’创建编号", "查看拒绝后的合同信息")
        a_time_2 = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_time(a_time_2, "‘未通过’提交时间", "查看拒绝后的合同信息")
        state_2 = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/b')
        self.check_information_if("未通过", state_2, "‘我方待处理列表’状态", "查看拒绝后的合同信息")
        Ca().xpath_click_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击操作", "查看拒绝后的合同信息",
            "云平台‘代理方’", sys._getframe().f_lineno)

        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_two(driver, "委托申请", "委托申请详情", "查看拒绝后的合同信息", "合同详情一级目录", "合同详情二级目录")
        # 校验详情页面信息
        self.details_information(driver, "查看拒绝后的合同信息")
        Ca().slide_("100")
        self.contract_content(driver, "查看拒绝后的合同信息")
        time.sleep(1.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[3]/div/div[1]/div/div/div/div/div[1]/div[4]',
                                     "点击操作记录", "查看拒绝后的合同信息", "云平台‘代理方’", sys._getframe().f_lineno)
        if re.findall("test", self.start_url):
            self.Operation_record_refuse(driver, "代理商拒绝合同申请", "深圳市九二六供应链网络有限公司代采分公司1 13245678999_s", "查看拒绝后的合同信息",
                                         "查看拒绝后已收到的合同的操作状态", "查看拒绝后已收到的合同的操作时间", "拒绝后已收到的合同的操作者信息"
                                         , '查看拒绝后已收到的合同的拒绝原因', '查看拒绝后已收到的合同的拒绝详情')
        else:
            self.Operation_record_refuse(driver, "代理商拒绝合同申请", "深圳市九二六供应链网络有限公司 18373847538_s", "查看拒绝后的合同信息",
                                         "查看拒绝后已收到的合同的操作状态", "查看拒绝后已收到的合同的操作时间", "拒绝后已收到的合同的操作者信息"
                                         , '查看拒绝后已收到的合同的拒绝原因', '查看拒绝后已收到的合同的拒绝详情')

    def agent_agree_contract(self):  # 代理方同意委托
        driver = self.driver
        print("*****代理方同意委托*****")
        Ca().slide_("0")
        Ca().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击进入委托申请", "同意已收到的合同", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击进入待审核",
                                     "同意已收到的合同", "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button',
                                     "点击我方待审签-操作", "同意已收到的合同", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[2]/div[2]/span/button[1]', "点击同意", "同意已收到的合同",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        Ca().xpath_keys_("//input[@class='ant-checkbox-input']",
                                     "点击已阅读合同", "同意已收到的合同", "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_keys_('//div[@class="ant-modal-body"]/div/button', "点击确认审签", "同意已收到的合同",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(1)
        Ca().xpath_send_('//div[@class="ant-col ant-col-17"]/input', "48152")
        Ca().is_toast_exist("输入验证码", "签审合同", "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_keys_('//div[@class="ant-modal-footer"]/button[2]', "点击确定",
                         "签审合同", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(3)
        print("*****代理方查看通过签审后的客户信息*****")
        driver = Ca().driver
        Ca().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击进入委托申请", "查看通过签审后的合同信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击进入已审核",
                                     "查看通过签审后的合同信息", "云平台‘代理方’", sys._getframe().f_lineno)

        apply_number = gl.get_value('apply_number')
        apply_number_2 = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘已审批’创建编号", "查看通过签审后的合同信息")
        a_time_2 = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_time(a_time_2, "‘已审批’提交时间", "查看通过签审后的合同信息")
        state_2 = Ca().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/b')
        self.check_information_if("已审核", state_2, "‘已审签’状态", "查看通过签审后的合同信息")
        Ca().xpath_click_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击操作", "查看通过签审后的合同信息",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_two(driver, "委托申请", "委托申请详情", "查看通过签审后的合同信息", "合同详情一级目录", "合同详情二级目录")
        # 校验详情页面信息
        self.details_information(driver, "查看通过签审后的合同信息")
        Ca().slide_("100")
        # 校验详情合同信息
        self.contract_content(driver, "查看通过签审后的合同信息")
        time.sleep(1.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[3]/div/div[1]/div/div/div/div/div[1]/div[4]',
                                     "点击操作记录", "查看通过签审后的合同信息", "云平台‘代理方’", sys._getframe().f_lineno)
        self.Operation_record(driver, "代理商已审签", "深圳市九二六供应链网络有限公司代采分公司1 13245678999_s", "查看通过签审后的合同信息",
                              "查看签审后已收到的合同的操作状态", "查看签审后已收到的合同的操作时间", "签审后已收到的合同的操作者信息")
        time.sleep(3)
        # print("*****代理方查看通过签审后的客户信息*****")
        # driver = Ca().driver
        # purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        # supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方企业名
        # Ca().xpath_click_('//*[@id="8$Menu"]/li', "点击进入客户列表", "查看通过签审后的客户信息", "云平台‘代理方’",
        #                              sys._getframe().f_lineno)
        # print('supplier_name %s' % supplier_name)
        # driver.find_element_by_xpath('//*[@id="keywords"]').clear()
        # Ca().xpath_send_('//*[@id="keywords"]', '天河软件', "搜索销售方", "代理方查看客户信息", "云平台‘代理方’",
        #                  sys._getframe().f_lineno)
        # Ca().xpath_click_(xpath_front + '/div/div/div[1]/form/div[2]/div[2]/button', "点击搜索", "代理方查看客户信息", "云平台‘代理方’",
        #                   sys._getframe().f_lineno)
        # Ca().xpath_click_(xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[5]/a/button',
        #                   "点击进入丙（销售)  方企业", "进入通过签审后的丙（销售)  方客户信息", "云平台‘代理方’", sys._getframe().f_lineno)
        # # print(name_1)
        # purchaser_email = gl.get_value('purchaser_email')  # 甲（采购）方邮箱
        # purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        # purchaser_926 = gl.get_value('purchaser_926')  # 甲（采购）方926链号
        # purchaser_bank = gl.get_value('purchaser_bank')  # 采购（甲）方开户行
        # purchaser_account = gl.get_value('purchaser_account', )  # 采购（甲）方账号
        # supplier_926 = gl.get_value('supplier_926')  # 丙（销售)  #方926链号
        # supplier_email = gl.get_value('supplier_email')  # 丙（销售)  #方邮箱
        # supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方企业名
        # supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)  #方电话
        # supplier_bank = gl.get_value('supplier_bank')  # 销售方（丙）开户行
        # supplier_account = gl.get_value('supplier_account')  # 销售方（丙）方账号
        # Ca().xpath_click_(
        #     xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr[%s]/td[5]/a/button' % i,
        #     "点击进入丙（销售)  方企业", "进入通过签审后的丙（销售)  方客户信息", "云平台‘代理方’", sys._getframe().f_lineno)
        # time.sleep(3)
        # name_2 = Ca().xpath_text_('//*[@id="name"]')
        # self.check_information_if(supplier_name, name_2, "企业名-详情页", "进入通过签审后的丙（销售)  方客户信息")
        # supplier_926_1 = Ca().xpath_text_('//*[@id="accountSn"]')
        # self.check_information_if(supplier_926, supplier_926_1, "企业926链号-详情页", "进入通过签审后的丙（销售)  方客户信息")
        # industry = Ca().xpath_text_('//*[@id="industry"]')
        # self.check_information_if('家具/室内设计/装饰装潢', industry, "企业所属行业-详情页", "进入通过签审后的丙（销售)  方客户信息")
        # region = Ca().xpath_text_('//*[@id="region"]')
        # self.check_information_if('北京市北京市朝阳区', region, "企业所在地区详情页", "进入通过签审后的丙（销售)  方客户信息")
        # phone = Ca().xpath_text_('//*[@id="phone"]')
        # self.check_information_if(supplier_phone, phone, "企业电话", "进入通过签审后的丙（销售)  方客户信息")
        # email = Ca().xpath_text_('//*[@id="email"]')
        # self.check_information_if(supplier_email, email, "企业email", "进入通过签审后的丙（销售)  方客户信息")
        # bankAccountName = Ca().xpath_text_('//*[@id="bankAccountName"]')
        # self.check_information_if("哼1", bankAccountName, "企业开户名称", "进入通过签审后的丙（销售)  方客户信息")
        # depositBank = Ca().xpath_text_('//*[@id="depositBank"]')
        # self.check_information_if(supplier_bank, depositBank, "企业开户行", "进入通过签审后的丙（销售)  方客户信息")
        # bankRegion = Ca().xpath_text_('//*[@id="bankRegion"]')
        # self.check_information_if('甘肃省定西市陇西县', bankRegion, "企业开户行", "进入通过签审后的丙（销售)  方客户信息")
        # bankAccount = Ca().xpath_text_('//*[@id="bankAccount"]')
        # self.check_information_if(supplier_account, bankAccount, "企业开户账号", "进入通过签审后的丙（销售)  方客户信息")
        #
        # totalCreditQuota_supplier = gl.get_value('totalCreditQuota_supplier', )  # 丙 总授信云票"
        # totalCirculationQuota_supplier = gl.get_value('totalCirculationQuota_supplier')  # 丙 总流转云票"
        # totalQuota_supplier = gl.get_value('totalQuota_supplier')  # 丙 总云票 （授信+流转）
        # totalOccupyCreditQuota_supplier = gl.get_value('totalOccupyCreditQuota_supplier')  # 丙 已占用授信云票
        # totalOccupyCirculationQuota_supplier = gl.get_value(
        #     'totalOccupyCirculationQuota_supplier')  # 丙 已占用流转云票
        # totalFrozenCreditQuota_supplier = gl.get_value('totalFrozenCreditQuota_supplier')  # 丙 获取已冻结授信云票
        # totalFrozenCirculationQuota_supplier = gl.get_value(
        #     'totalFrozenCirculationQuota_supplier')  # 丙 已冻结流转云票
        # totalOccupancyCreditQuota_supplier = gl.get_value(
        #     'totalOccupancyCreditQuota_supplier')  # 丙 可用总授信(总-已用)
        # totalOccupancyCirculationQuota_supplier = gl.get_value(
        #     'totalOccupancyCirculationQuota_supplier')  # 丙 余总流转(总-已用
        # contactEffectiveNum_supplier = gl.get_value('contactEffectiveNum_supplier')  # 生效委托申请单
        # loanHistoryNum_supplier = gl.get_value('loanHistoryNum_supplier')  # 贷现历史次数
        #
        # totalCreditQuota_supplier_1 = Ca().xpath_text_('//*[@id="totalCreditQuota"]/div/span')
        # totalCreditQuota_supplier_1 = re_sub_(totalCreditQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalCreditQuota_supplier, totalCreditQuota_supplier_1, "采购总授信云票",
        #                           "进入通过签审后的丙（销售)  方客户信息")
        # totalCirculationQuota_supplier_1 = Ca().xpath_text_(
        #     '//*[@id="totalCirculationQuota"]/div/span')
        # totalCirculationQuota_supplier_1 = re_sub_(
        #     totalCirculationQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalCirculationQuota_supplier, totalCirculationQuota_supplier_1,
        #                           "采购总流转云票",
        #                           "进入通过签审后的丙（销售)  方客户信息")
        #
        # totalQuota_supplier_1 = Ca().xpath_text_('//*[@id="totalQuota"]/div')
        # totalQuota_supplier_1 = re_sub_(totalQuota_supplier_1)  # 显示为xx,xxx.00 正则筛
        # self.check_information_if(totalQuota_supplier, totalQuota_supplier_1, "总云票 （授信+流转）",
        #                           "进入通过签审后的丙（销售)  方客户信息")
        #
        # totalOccupyCreditQuota_supplier_1 = Ca().xpath_text_(
        #     '//*[@id="totalOccupyCreditQuota"]/div/span')
        # totalOccupyCreditQuota_supplier_1 = re_sub_(
        #     totalOccupyCreditQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalOccupyCreditQuota_supplier, totalOccupyCreditQuota_supplier_1,
        #                           "已占用授信云票", "进入通过签审后的丙（销售)  方客户信息")
        # totalOccupyCirculationQuota_supplier_1 = Ca().xpath_text_(
        #     '//*[@id="totalOccupyCirculationQuota"]/div/span')
        # totalOccupyCirculationQuota_supplier_1 = re_sub_(
        #     totalOccupyCirculationQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalOccupyCirculationQuota_supplier,
        #                           totalOccupyCirculationQuota_supplier_1,
        #                           "已占用流转云票", "进入通过签审后的丙（销售)  方客户信息")
        #
        # totalFrozenCreditQuota_supplier_1 = Ca().xpath_text_(
        #     '//*[@id="totalFrozenCreditQuota"]/div/span')
        # totalFrozenCreditQuota_supplier_1 = re_sub_(
        #     totalFrozenCreditQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalFrozenCreditQuota_supplier, totalFrozenCreditQuota_supplier_1,
        #                           "获取已冻结授信云票", "进入通过签审后的丙（销售)  方客户信息")
        #
        # totalFrozenCirculationQuota_supplier_1 = Ca().xpath_text_(
        #     '//*[@id="totalFrozenCirculationQuota"]/div/span')
        # totalFrozenCirculationQuota_supplier_1 = re_sub_(
        #     totalFrozenCirculationQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalFrozenCirculationQuota_supplier,
        #                           totalFrozenCirculationQuota_supplier_1,
        #                           "获取已冻结流转云票", "进入通过签审后的丙（销售)  方客户信息")
        #
        # totalOccupancyCreditQuota_supplier_1 = Ca().xpath_text_(
        #     '//*[@id="totalOccupancyCreditQuota"]/div')
        # totalOccupancyCreditQuota_supplier_1 = re_sub_(
        #     totalOccupancyCreditQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalOccupancyCreditQuota_supplier, totalOccupancyCreditQuota_supplier_1,
        #                           "可用总授信(总-已用)", "进入通过签审后的丙（销售)  方客户信息")
        #
        # totalOccupancyCirculationQuota_supplier_1 = Ca().xpath_text_(
        #     '//*[@id="totalOccupancyCirculationQuota"]/div')
        # totalOccupancyCirculationQuota_supplier_1 = re_sub_(
        #     totalOccupancyCirculationQuota_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalOccupancyCirculationQuota_supplier,
        #                           totalOccupancyCirculationQuota_supplier_1,
        #                           "可用总流转(总-已用)", "进入通过签审后的丙（销售)  方客户信息")
        # contactEffectiveNum_supplier_1 = Ca().xpath_text_('//*[@id="contactEffectiveNum"]/div')
        # contactEffectiveNum_supplier_1 = re_sub_(contactEffectiveNum_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # contactEffectiveNum_supplier_check = int(contactEffectiveNum_supplier) + 1
        # self.check_information_if(str(contactEffectiveNum_supplier_check), contactEffectiveNum_supplier_1,
        #                           "校验生效委托申请单", "进入通过签审后的丙（销售)  方客户信息")
        #
        # loanHistoryNum_supplier_1 = Ca().xpath_text_('//*[@id="loanHistoryNum"]/div')
        # loanHistoryNum_supplier_1 = re_sub_(loanHistoryNum_supplier_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(loanHistoryNum_supplier, loanHistoryNum_supplier_1,
        #                           "贷现申请次数", "进入通过签审后的丙（销售)方客户信息")
        # Ca().xpath_click_('//*[@id="8$Menu"]/li', "点击进入客户列表", "查看通过签审后的客户信息", "云平台‘代理方’",
        #                              sys._getframe().f_lineno)
        # time.sleep(2.5)
        # gl.set_value('totalCreditQuota_supplier', totalCreditQuota_supplier)  # 丙 总授信云票"
        # gl.set_value('totalCirculationQuota_supplier', totalCirculationQuota_supplier)  # 丙 总流转云票"
        # gl.set_value('totalQuota_supplier', totalQuota_supplier)  # 丙 总云票 （授信+流转）
        # gl.set_value('totalOccupyCreditQuota_supplier', totalOccupyCreditQuota_supplier)  # 丙 已占用授信云票
        # gl.set_value('totalOccupyCirculationQuota_supplier',
        #              totalOccupyCirculationQuota_supplier)  # 丙 已占用流转云票
        # gl.set_value('totalFrozenCreditQuota_supplier', totalFrozenCreditQuota_supplier)  # 丙 获取已冻结授信云票
        # gl.set_value('totalFrozenCirculationQuota_supplier',
        #              totalFrozenCirculationQuota_supplier)  # 丙 已冻结流转云票
        # gl.set_value('totalOccupancyCreditQuota_supplier',
        #              totalOccupancyCreditQuota_supplier)  # 丙 可用总授信(总-已用)
        # gl.set_value('totalOccupancyCirculationQuota_supplier',
        #              totalOccupancyCirculationQuota_supplier)  # 丙 余总流转(总-已用
        # gl.set_value('contactEffectiveNum_supplier', contactEffectiveNum_supplier)  # 生效委托申请单
        # gl.set_value('loanHistoryNum_supplier', loanHistoryNum_supplier)  # 贷现历史次数
        #
        # print('丙 总授信云票：%s' % totalCreditQuota_supplier)
        # print('丙 总流转云票：%s' % totalCirculationQuota_supplier)
        # print('丙 总云票 （授信+流转）：%s' % totalQuota_supplier)
        # print('丙 已占用授信云票：%s' % totalOccupyCreditQuota_supplier)
        # print('丙 已占用流转云票：%s' % totalOccupyCirculationQuota_supplier)
        # print('丙 获取已冻结授信云票：%s' % totalFrozenCreditQuota_supplier)
        # print('丙 已冻结流转云票：%s' % totalFrozenCirculationQuota_supplier)
        # print('丙 可用总授信(总-已用)：%s' % totalOccupancyCreditQuota_supplier)
        # print('丙 余总流转(总-已用：%s' % totalOccupancyCirculationQuota_supplier)
        # print('丙 生效委托申请单：%s' % contactEffectiveNum_supplier)
        # print('丙 贷现历史次数：%s' % loanHistoryNum_supplier)
        #
        # Ca().xpath_click_(
        #     xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr[%s]/td[5]/a/button' % i,
        #     "点击进入甲（采购）  方企业", "进入通过签审后的甲（采购）方企业信息", "云平台‘代理方’", sys._getframe().f_lineno)
        # time.sleep(3)
        # name_2 = Ca().xpath_text_('//*[@id="name"]')
        # self.check_information_if(purchaser_name, name_2, "企业名-详情页", "进入通过签审后的甲（采购）方企业信息")
        # purchaser_926_1 = Ca().xpath_text_('//*[@id="accountSn"]')
        # self.check_information_if(purchaser_926, purchaser_926_1, "企业926链号-详情页", "进入通过签审后的甲（采购）方企业信息")
        # industry = Ca().xpath_text_('//*[@id="industry"]')
        # self.check_information_if('家具/室内设计/装饰装潢', industry, "企业所属行业-详情页", "进入通过签审后的甲（采购）方企业信息")
        # region = Ca().xpath_text_('//*[@id="region"]')
        # self.check_information_if('北京市北京市东城区', region, "企业所在地区详情页", "进入通过签审后的甲（采购）方企业信息")
        # phone = Ca().xpath_text_('//*[@id="phone"]')
        # self.check_information_if(purchaser_phone, phone, "企业电话", "进入通过签审后的甲（采购）方企业信息")
        # email = Ca().xpath_text_('//*[@id="email"]')
        # self.check_information_if(purchaser_email, email, "企业email", "进入通过签审后的甲（采购）方企业信息")
        # bankAccountName = Ca().xpath_text_('//*[@id="bankAccountName"]')
        # self.check_information_if("3761", bankAccountName, "企业开户名称", "进入通过签审后的甲（采购）方企业信息")
        # depositBank = Ca().xpath_text_('//*[@id="depositBank"]')
        # self.check_information_if(purchaser_bank, depositBank, "企业开户行", "进入通过签审后的甲（采购）方企业信息")
        # bankRegion = Ca().xpath_text_('//*[@id="bankRegion"]')
        # self.check_information_if('北京市北京市东城区', bankRegion, "企业开户行", "进入通过签审后的甲（采购）方企业信息")
        # bankAccount = Ca().xpath_text_('//*[@id="bankAccount"]')
        # self.check_information_if(purchaser_account, bankAccount, "企业开户账号", "进入通过签审后的甲（采购）方企业信息")
        #
        # totalCreditQuota_purchaser = gl.get_value('totalCreditQuota_purchaser')  # 丙 采购总授信云票"
        # totalCirculationQuota_purchaser = gl.get_value('totalCirculationQuota_purchaser')  # 丙 采购总流转云票"
        # totalQuota_purchaser = gl.get_value('totalQuota_purchaser')  # 丙 总云票 （授信+流转）
        # totalOccupyCreditQuota_purchaser = gl.get_value('totalOccupyCreditQuota_purchaser')  # 丙 已占用授信云票
        # totalOccupyCirculationQuota_purchaser = gl.get_value(
        #     'totalOccupyCirculationQuota_purchaser')  # 丙 已占用流转云票
        # totalFrozenCreditQuota_purchaser = gl.get_value('totalFrozenCreditQuota_purchaser')  # 丙 获取已冻结授信云票
        # totalFrozenCirculationQuota_purchaser = gl.get_value(
        #     'totalFrozenCirculationQuota_purchaser')  # 丙 已冻结流转云票
        # totalOccupancyCreditQuota_purchaser = gl.get_value(
        #     'totalOccupancyCreditQuota_purchaser')  # 丙 可用总授信(总-已用)
        # totalOccupancyCirculationQuota_purchaser = gl.get_value(
        #     'totalOccupancyCirculationQuota_purchaser')  # 丙 余总流转(总-已用
        # contactEffectiveNum_purchaser = gl.get_value('contactEffectiveNum_purchaser')  # 生效委托申请单
        # loanHistoryNum_purchaser = gl.get_value('loanHistoryNum_purchaser')  # 贷现历史次数
        #
        # totalCreditQuota_purchaser_1 = Ca().xpath_text_('//*[@id="totalCreditQuota"]/div/span')
        # totalCreditQuota_purchaser_1 = re_sub_(totalCreditQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalCreditQuota_purchaser, totalCreditQuota_purchaser_1, "采购总授信云票",
        #                           "进入通过签审后的甲（采购）方客户信息")
        # totalCirculationQuota_purchaser_1 = Ca().xpath_text_(
        #     '//*[@id="totalCirculationQuota"]/div/span')
        # totalCirculationQuota_purchaser_1 = re_sub_(totalCirculationQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalCirculationQuota_purchaser, totalCirculationQuota_purchaser_1,
        #                           "采购总流转云票",
        #                           "进入通过签审后的甲（采购）方客户信息")
        #
        # totalQuota_purchaser_1 = Ca().xpath_text_('//*[@id="totalQuota"]/div')
        # totalQuota_purchaser_1 = re_sub_(totalQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛
        # self.check_information_if(totalQuota_purchaser, totalQuota_purchaser_1, "总云票 （授信+流转）",
        #                           "进入通过签审后的甲（采购）方客户信息")
        #
        # totalOccupyCreditQuota_purchaser_1 = Ca().xpath_text_(
        #     '//*[@id="totalOccupyCreditQuota"]/div/span')
        # totalOccupyCreditQuota_purchaser_1 = re_sub_(
        #     totalOccupyCreditQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalOccupyCreditQuota_purchaser, totalOccupyCreditQuota_purchaser_1,
        #                           "已占用授信云票",
        #                           "进入通过签审后的甲（采购）方客户信息")
        # totalOccupyCirculationQuota_purchaser_1 = Ca().xpath_text_(
        #     '//*[@id="totalOccupyCirculationQuota"]/div/span')
        # totalOccupyCirculationQuota_purchaser_1 = re_sub_(
        #     totalOccupyCirculationQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalOccupyCirculationQuota_purchaser,
        #                           totalOccupyCirculationQuota_purchaser_1,
        #                           "已占用流转云票", "进入通过签审后的甲（采购）方客户信息")
        #
        # totalFrozenCreditQuota_purchaser_1 = Ca().xpath_text_(
        #     '//*[@id="totalFrozenCreditQuota"]/div/span')
        # totalFrozenCreditQuota_purchaser_1 = re_sub_(
        #     totalFrozenCreditQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalFrozenCreditQuota_purchaser, totalFrozenCreditQuota_purchaser_1,
        #                           "获取已冻结授信云票", "进入通过签审后的甲（采购）方客户信息")
        #
        # totalFrozenCirculationQuota_purchaser_1 = Ca().xpath_text_(
        #     '//*[@id="totalFrozenCirculationQuota"]/div/span')
        # totalFrozenCirculationQuota_purchaser_1 = re_sub_(
        #     totalFrozenCirculationQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalFrozenCirculationQuota_purchaser,
        #                           totalFrozenCirculationQuota_purchaser_1,
        #                           "获取已冻结流转云票", "进入通过签审后的甲（采购）方客户信息")
        #
        # totalOccupancyCreditQuota_purchaser_1 = Ca().xpath_text_(
        #     '//*[@id="totalOccupancyCreditQuota"]/div')
        # totalOccupancyCreditQuota_purchaser_1 = re_sub_(
        #     totalOccupancyCreditQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalOccupancyCreditQuota_purchaser,
        #                           totalOccupancyCreditQuota_purchaser_1, "可用总授信(总-已用)",
        #                           "进入通过签审后的甲（采购）方客户信息")
        #
        # totalOccupancyCirculationQuota_purchaser_1 = Ca().xpath_text_(
        #     '//*[@id="totalOccupancyCirculationQuota"]/div')
        # totalOccupancyCirculationQuota_purchaser_1 = re_sub_(
        #     totalOccupancyCirculationQuota_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(totalOccupancyCirculationQuota_purchaser,
        #                           totalOccupancyCirculationQuota_purchaser_1,
        #                           "可用总流转(总-已用)", "进入通过签审后的甲（采购）方客户信息")
        #
        # contactEffectiveNum_purchaser_1 = Ca().xpath_text_('//*[@id="contactEffectiveNum"]/div')
        # contactEffectiveNum_purchaser_1 = re_sub_(contactEffectiveNum_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # contactEffectiveNum_purchaser_check = int(contactEffectiveNum_purchaser) + 1
        # self.check_information_if(str(contactEffectiveNum_purchaser_check), contactEffectiveNum_purchaser_1,
        #                           "校验生效委托申请单", "进入通过签审后的甲（采购）方客户信息")
        #
        # loanHistoryNum_purchaser_1 = Ca().xpath_text_('//*[@id="loanHistoryNum"]/div')
        # loanHistoryNum_purchaser_1 = re_sub_(loanHistoryNum_purchaser_1)  # 显示为xx,xxx.00 正则筛选
        # self.check_information_if(loanHistoryNum_purchaser, loanHistoryNum_purchaser_1,
        #                           "贷现申请次数", "进入通过签审后的甲（采购）方客户信息")
        # Ca().xpath_click_('//*[@id="8$Menu"]/li', "点击进入客户列表", "查看通过签审后的客户信息", "云平台‘代理方’",
        #                              sys._getframe().f_lineno)
        # time.sleep(2.5)
        # gl.set_value('totalCreditQuota_purchaser', totalCreditQuota_purchaser)  # 甲 采购总授信云票"
        # gl.set_value('totalCirculationQuota_purchaser', totalCirculationQuota_purchaser)  # 甲 采购总流转云票"
        # gl.set_value('totalQuota_purchaser', totalQuota_purchaser)  # 甲 总云票 （授信+流转）
        # gl.set_value('totalOccupyCreditQuota_purchaser', totalOccupyCreditQuota_purchaser)  # jia 已占用授信云票
        # gl.set_value('totalOccupyCirculationQuota_purchaser',
        #              totalOccupyCirculationQuota_purchaser)  # jia 已占用流转云票
        # gl.set_value('totalFrozenCreditQuota_purchaser', totalFrozenCreditQuota_purchaser)  # jia 获取已冻结授信云票
        # gl.set_value('totalFrozenCirculationQuota_purchaser',
        #              totalFrozenCirculationQuota_purchaser)  # jia 已冻结流转云票
        # gl.set_value('totalOccupancyCreditQuota_purchaser',
        #              totalOccupancyCreditQuota_purchaser)  # jia 可用总授信(总-已用)
        # gl.set_value('totalOccupancyCirculationQuota_purchaser',
        #              totalOccupancyCirculationQuota_purchaser)  # jia 余总流转(总-已用
        # gl.set_value('contactEffectiveNum_purchaser', contactEffectiveNum_purchaser)  # 生效委托申请单
        # gl.set_value('loanHistoryNum_purchaser', loanHistoryNum_purchaser)  # 贷现历史次数
        #
        # print('甲 总授信云票：%s' % totalCreditQuota_purchaser)
        # print('甲 总流转云票：%s' % totalCirculationQuota_purchaser)
        # print('甲 总云票 （授信+流转）：%s' % totalQuota_purchaser)
        # print('甲 已占用授信云票：%s' % totalOccupyCreditQuota_purchaser)
        # print('甲 已占用流转云票：%s' % totalOccupyCirculationQuota_purchaser)
        # print('甲 获取已冻结授信云票：%s' % totalFrozenCreditQuota_purchaser)
        # print('甲 已冻结流转云票：%s' % totalFrozenCirculationQuota_purchaser)
        # print('甲 可用总授信(总-已用)：%s' % totalOccupancyCreditQuota_purchaser)
        # print('甲 余总流转(总-已用：%s' % totalOccupancyCirculationQuota_purchaser)
        # print('甲 生效委托申请单：%s' % contactEffectiveNum_purchaser)
        # print('甲 贷现历史次数：%s' % loanHistoryNum_purchaser)

    def Delivery_application(self):  # 代理方通过发货申请
        driver = self.driver
        time.sleep(1)
        print("*****代理方通过发货申请*****")
        Ca().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入发货申请", "通过发货申请", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击进入待办",
                                     "通过发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button',
                                     "点击进入待办-操作", "通过发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[2]/div[2]/span/button[1]', "点击确认通过", "通过发货申请",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_click_(
            '//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认通过", "通过发货申请",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(3)

        print("*****代理方查看通过后的发货申请*****")
        Ca().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入委托申请", "查看通过后的发货申请", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(3)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击进入已通过",
                                     "查看通过后的发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(3)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        invoiceApplySn_2 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(invoiceApplySn, invoiceApplySn_2, "‘已通过’创建编号", "查看通过后的发货申请")
        a_time_2 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_time(a_time_2, "‘已通过’提交时间", "查看通过后的发货申请")
        state_3 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/b')
        self.check_information_if("代理通过", state_3, "‘已通过’状态", "查看通过后的发货申请")
        Ca().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button', "点击操作", "查看通过后的发货申请",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        state_4 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[1]/span')
        self.check_information_if("代理通过", state_4, "‘发货详情页面’状态", "查看通过后的发货申请")
        # 校验目录、导航
        self.catalog_two(driver, "发货申请", "发货详情", "查看通过后的发货申请", "一级目录", "二级目录")
        # 校验详情页面信息
        self.details_information_2(driver, "查看通过后的发货申请")
        Ca().slide_("100")
        time.sleep(1.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[3]/div/div[1]/div/div/div/div/div[1]/div[2]',
                                     "点击操作记录", "查看通过后的发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        if re.findall("test", self.start_url):
            self.Operation_record_2(driver, "代理通过", "13245678999_s", "查看通过后的发货申请",
                                    "查看通过后的操作状态", "查看通过后的发货申请", "通过后的操作者信息")
        else:
            self.Operation_record_2(driver, "代理通过", "18373847538_s", "查看通过后的发货申请",
                                    "查看通过后的操作状态", "查看通过后的发货申请", "通过后的操作者信息")

    def refuse_delivery_application(self):  # 代理方拒绝发货申请
        driver = Ca().driver
        Ca().slide_("0")
        print("*****代理方查看拒绝前已收到的发货申请*****")
        Ca().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入发货申请", "查看拒绝前已收到的发货申请", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(3)
        # self.catalog_two(driver, "代销管理", "出货单列表", "代销方出货", "出货单列表页一级目录", "出货单列表页二级目录")
        self.list_four(driver, "全部", "待办", "已通过", "已拒绝", "查看拒绝前已收到的发货申请", "发货申请-全部列表",
                       "发货申请-待办列表", "发货申请-已通过列表", "发货申请-已拒绝列表")
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击进入待办",
                                     "查看拒绝前已收到的发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(3)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        invoiceApplySn_2 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[1]')
        self.check_information_if(invoiceApplySn, invoiceApplySn_2, "‘待办列表’创建编号", "查看拒绝前已收到的发货申请")
        a_time_2 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_time(a_time_2, "‘待审批列表’提交时间", "查看拒绝前已收到的发货申请")
        agent_list_state = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/b')
        self.check_information_if("采购商已同意", agent_list_state, "‘待审批列表’状态", "查看拒绝前已收到的发货申请")
        Ca().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button', "点击操作", "查看拒绝前已收到的发货申请",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        state_4 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[1]/span')
        self.check_information_if("待代理批复", state_4, "‘发货详情页面’状态", "查看拒绝前已收到的发货申请")
        # 校验目录、导航
        self.catalog_two(driver, "发货申请", "发货详情", "查看拒绝前已收到的发货申请", "一级目录", "二级目录")
        # 校验详情页面信息
        print("*****查看拒绝前页面详情信息****")
        self.details_information_2(driver, "查看拒绝前已收到的发货申请")
        Ca().slide_("100")
        # 校验合同内容信息
        time.sleep(1.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[3]/div/div[1]/div/div/div/div/div[1]/div[2]',
                                     "点击操作记录", "查看拒绝前已收到的发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        if re.findall("test", self.start_url):
            self.Operation_record_2(driver, "采购商已同意", "18474793371_s", "查看拒绝前已收到的发货申请",
                                    "查看拒绝前已收到的发货申请的操作状态", "查看拒绝前已收到的发货申请的操作时间", "拒绝前已收到的发货申请的操作者信息")
        else:
            self.Operation_record_2(driver, "采购商已同意", "18390552449_s", "查看拒绝前已收到的发货申请",
                                    "查看拒绝前已收到的发货申请的操作状态", "查看拒绝前已收到的发货申请的操作时间", "拒绝前已收到的发货申请的操作者信息")

        print("****代理方拒绝发货申请*****")
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[2]/div[2]/span/button[2]', "点击拒绝", "代理方拒绝发货申请",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2)
        Ca().xpath_click_('//div[@class="ant-modal-body"]/div/div[2]/div/button[1]',
                          "选择拒绝标签1", "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)

        Ca().xpath_click_('//div[@class="ant-modal-body"]/div/div[2]/div/button[4]'
                          '', "选择拒绝标签2", "代采方拒绝发货申请", "云平台‘采购方’",
                          sys._getframe().f_lineno)
        Ca().xpath_click_('//textarea[@class="ant-input"]', "点击拒绝理由", "代理方拒绝发货申请", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        Ca().xpath_send_('//textarea[@class="ant-input"]', "fkl")
        Ca().is_toast_exist("输入拒绝理由", "代理方拒绝发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(0.5)
        Ca().xpath_click_('//div[@class="ant-modal-footer"]/span/button[2]', "点击确认",
                                     "代理方拒绝发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(1)
        Ca().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认",
                                     "代理方拒绝发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(3)
        print("*****代理方查看拒绝后的合同信息*****")

        Ca().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入委托申请", "查看拒绝后的发货申请", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]', "点击进入已拒绝",
                                     "查看拒绝后的发货申请", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        invoiceApplySn_2 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(invoiceApplySn, invoiceApplySn_2, "‘未通过’创建编号", "查看拒绝后的发货申请")
        a_time_2 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_time(a_time_2, "‘未通过’提交时间", "查看拒绝后的发货申请")
        state_3 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/b')
        self.check_information_if("代理驳回", state_3, "‘我方待处理列表’状态", "查看拒绝后的发货申请")
        Ca().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button', "点击操作", "查看拒绝后的发货申请",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        state_4 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[1]/span')
        self.check_information_if("代理驳回", state_4, "‘发货详情页面’状态", "查看拒绝后的发货申请")
        # 校验目录、导航
        self.catalog_two(driver, "发货申请", "发货详情", "查看拒绝后的发货申请", "一级目录", "二级目录")
        # 校验详情页面信息
        self.details_information_2(driver, "查看拒绝后的详情页面信息")
        Ca().slide_("100")
        time.sleep(1.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div[3]/div/div[1]/div/div/div/div/div[1]/div[2]',
                                     "点击操作记录", "查看拒绝后的合同信息", "云平台‘代理方’", sys._getframe().f_lineno)
        self.Operation_record_refuse_2(driver, "代理驳回", "13245678999_s", "查看拒绝后的合同信息",
                                       "查看拒绝后已收到的合同的操作状态", "查看拒绝后已收到的合同的操作时间", "拒绝后的操作者信息"
                                       , '查看拒绝后的拒绝原因', '查看的合同的拒绝详情')

    def supplier_deliver_goods(self):
        driver = self.driver
        print("*****代理方查看销售出货后的出货信息*****")

        Ca().slide_("0")

        Ca().xpath_click_('//*[@id="2$Menu"]/li[3]', "点击进入出货跟踪", "代理方查看销售出货后的出货信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        self.catalog_two(driver, "货物管理", "出货跟踪列表", "代理方查看销售出货后的出货信息", "出货单列表页一级目录", "出货单列表页二级目录")
        invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
        invoiceSn_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody/'
                                                                'tr[1]/td[1]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "出货单编号", "代理方查看销售出货后的出货信息")

        invoiceApplySn = gl.get_value('invoiceApplySn')  # 出货单编号 DO
        invoiceApplySn_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[2]', sys._getframe().f_lineno)
        self.check_information_if(invoiceApplySn, invoiceApplySn_1, "发货单编号", "代理方查看销售出货后的出货信息")

        supplier_name = gl.get_value('supplier_name')
        supplier_name_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                    '/tr[1]/td[3]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_1, "发货单位", "代理方查看销售出货后的出货信息")

        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[4]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位", "代理方查看销售出货后的出货信息")

        total_Amount = gl.get_value('total_Amount')  # 发货总金额
        total_Amount_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                  '/tr[1]/td[5]', sys._getframe().f_lineno)
        total_Amount_1 = re_sub_(total_Amount_1)
        self.check_information_if(str(total_Amount), total_Amount_1, "发货总金额", "代理方查看销售出货后的出货信息")

        shipment_time_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                    '/tr[1]/td[6]', sys._getframe().f_lineno)
        self.check_information_time(shipment_time_1, "出货时间", "代理方查看销售出货后的出货信息")

        shipment_state_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[7]', sys._getframe().f_lineno)
        self.check_information_if('正常', shipment_state_1, "出货状态", "代理方查看销售出货后的出货信息")

        goods_state_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                  '/tr[1]/td[8]', sys._getframe().f_lineno)
        self.check_information_if('待收货', goods_state_1, "货物状态", "代理方查看销售出货后的出货信息")

        Ca().xpath_click_(
            xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[9]/a/button', "点击查看进入详情页", "代理方查"
                                                                                                               "看出货后的出货信息",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "货物管理", "出货跟踪列表", "出货跟踪详情", "代理方查看采购品检后的出货信息",
                           "出货单列表页一级目录", "出货单列表页二级目录", '出货单列表页三级目录')

        goods_state_2 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/h3/span',
                                                    sys._getframe().f_lineno)
        self.check_information_if(goods_state_1, goods_state_2, "详情页货物状态", "代理方查看销售出货后的出货信息")

        invoiceSn_2 = Ca().xpath_text_('//*[@id="invoiceSn"]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_2, "详情页货物状态", "代理方查看销售出货后的出货信息")

        invoiceApplySn_2 = Ca().xpath_text_('//*[@id="invoiceApplySn"]', sys._getframe().f_lineno)
        self.check_information_if(invoiceApplySn, invoiceApplySn_2, "详情页发货申请单号", "代理方查看销售出货后的出货信息")

        contractnumber = gl.get_value('contractnumber')
        contractnumber_2 = Ca().xpath_text_('//*[@id="contractSn"]', sys._getframe().f_lineno)
        self.check_information_if(contractnumber, contractnumber_2, "详情页委托单号", "代理方查看销售出货后的出货信息")

        supplier_name_2 = Ca().xpath_text_('//*[@id="supplierName"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "详情页发货单位", "代理方查看销售出货后的出货信息")

        supplier_details_page = Ca().xpath_href_('//*[@id="supplierName"]/a', sys._getframe().f_lineno)
        new_execute_script(supplier_details_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方查看销售出货后的出货方企业信息",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_3, "新页面中名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_name_2 = Ca().xpath_text_('//*[@id="purchaserName"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "详情页收货单位", "代理方查看销售出货后的出货信息")

        purchaser_details_page = Ca().xpath_href_('//*[@id="purchaserName"]/a', sys._getframe().f_lineno)
        new_execute_script(purchaser_details_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方查看销售出货后的出货方企业信息",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        total_Amount_2 = Ca().xpath_text_('//*[@id="a"]', sys._getframe().f_lineno)
        total_Amount_2 = re_sub_(total_Amount_2)
        self.check_information_if(str(total_Amount), total_Amount_2, "详情页货单金额", "代理方查看销售出货后的出货信息")

        shipment_time_2 = Ca().xpath_text_('//*[@id="deliveryGoodTime"]', sys._getframe().f_lineno)
        self.check_information_time(shipment_time_2, "详情页出货时间", "代理方查看销售出货后的出货信息")

        total_Amount_3 = Ca().xpath_text_(xpath_front + '/div/div/div[4]/div[3]/div[1]/div[2]/div[2]/span',
                                                    sys._getframe().f_lineno)
        total_Amount_3 = re_sub_(total_Amount_3)
        self.check_information_if(str(total_Amount), total_Amount_3, "发货明细中货单金额", "代理方查看销售出货后的出货信息")

        Ca().xpath_click_(
            xpath_front + '/div/div/div[4]/div[1]/div/div/div/div/div[1]/div[3]', "点击查看进入操作记录", "代理方查看出货后的出货信息",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)

        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[1]',
            sys._getframe().f_lineno)
        self.check_information_if('采购商待收货', record_state1, "操作记录中出货状态", '代理方查看销售出货后的出货信息')

        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[2]',
            sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '代理方查看销售出货后的出货信息')

        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[3]',
            sys._getframe().f_lineno)
        self.check_information_time(record_time1, "操作记录中发起申请时间", '代理方查看销售出货后的出货信息')

    def purchaser_collect(self):
        driver = self.driver
        print("*****代理方查看采购收货后的出货信息*****")

        Ca().slide_("0")

        Ca().xpath_click_('//*[@id="2$Menu"]/li[3]', "点击进入出货跟踪", "代理方查看采购收货后的出货信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        self.catalog_two(driver, "货物管理", "出货跟踪列表", "代理方查看采购收货后的出货信息", "出货单列表页一级目录", "出货单列表页二级目录")
        invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
        invoiceSn_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody/'
                                                                'tr[1]/td[1]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "出货单编号", "代理方查看采购收货后的出货信息")

        invoiceApplySn = gl.get_value('invoiceApplySn')  # 出货单编号 DO
        invoiceApplySn_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[2]', sys._getframe().f_lineno)
        self.check_information_if(invoiceApplySn, invoiceApplySn_1, "发货单编号", "代理方查看采购收货后的出货信息")

        supplier_name = gl.get_value('supplier_name')
        supplier_name_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                    '/tr[1]/td[3]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_1, "发货单位", "代理方查看采购收货后的出货信息")

        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[4]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位", "代理方查看采购收货后的出货信息")

        total_Amount = gl.get_value('total_Amount')  # 发货总金额
        total_Amount_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                  '/tr[1]/td[5]', sys._getframe().f_lineno)
        total_Amount_1 = re_sub_(total_Amount_1)
        self.check_information_if(str(total_Amount), total_Amount_1, "发货总金额", "代理方查看采购收货后的出货信息")

        shipment_time_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                    '/tr[1]/td[6]', sys._getframe().f_lineno)
        self.check_information_time(shipment_time_1, "出货时间", "代理方查看采购收货后的出货信息")

        shipment_state_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[7]', sys._getframe().f_lineno)
        self.check_information_if('正常', shipment_state_1, "出货状态", "代理方查看采购收货后的出货信息")

        goods_state_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                  '/tr[1]/td[8]', sys._getframe().f_lineno)
        self.check_information_if('待品检', goods_state_1, "货物状态", "代理方查看采购收货后的出货信息")

        Ca().xpath_click_(
            xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[9]/a/button', "点击查看进入详情页", "代理方查"
                                                                                                               "看出货后的出货信息",
            "云平台‘代理方’", sys._getframe().f_lineno)

        time.sleep(2.5)
        self.catalog_three(driver, "货物管理", "出货跟踪列表", "出货跟踪详情", "代理方查看采购品检后的出货信息",
                           "出货单列表页一级目录", "出货单列表页二级目录", '出货单列表页三级目录')

        goods_state_2 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/h3/span',
                                                    sys._getframe().f_lineno)
        self.check_information_if(goods_state_1, goods_state_2, "详情页货物状态", "代理方查看采购收货后的出货信息")

        invoiceSn_2 = Ca().xpath_text_('//*[@id="invoiceSn"]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_2, "详情页货物状态", "代理方查看采购收货后的出货信息")

        invoiceApplySn_2 = Ca().xpath_text_('//*[@id="invoiceApplySn"]', sys._getframe().f_lineno)
        self.check_information_if(invoiceApplySn, invoiceApplySn_2, "详情页发货申请单号", "代理方查看采购收货后的出货信息")

        contractnumber = gl.get_value('contractnumber')
        contractnumber_2 = Ca().xpath_text_('//*[@id="contractSn"]', sys._getframe().f_lineno)
        self.check_information_if(contractnumber, contractnumber_2, "详情页委托单号", "代理方查看采购收货后的出货信息")

        supplier_name_2 = Ca().xpath_text_('//*[@id="supplierName"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "详情页发货单位", "代理方查看采购收货后的出货信息")
        supplier_name_2 = Ca().xpath_text_('//*[@id="supplierName"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "详情页发货单位", "代理方查看销售出货后的出货信息")

        supplier_details_page = Ca().xpath_href_('//*[@id="supplierName"]/a', sys._getframe().f_lineno)
        new_execute_script(supplier_details_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方查看销售出货后的出货信息",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_3, "新页面中名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_name_2 = Ca().xpath_text_('//*[@id="purchaserName"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "详情页收货单位", "代理方查看销售出货后的出货信息")

        purchaser_details_page = Ca().xpath_href_('//*[@id="purchaserName"]/a', sys._getframe().f_lineno)
        new_execute_script(purchaser_details_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方查看销售出货后的出货信息",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        total_Amount_2 = Ca().xpath_text_('//*[@id="a"]', sys._getframe().f_lineno)
        total_Amount_2 = re_sub_(total_Amount_2)
        self.check_information_if(str(total_Amount), total_Amount_2, "详情页货单金额", "代理方查看采购收货后的出货信息")

        shipment_time_2 = Ca().xpath_text_('//*[@id="deliveryGoodTime"]', sys._getframe().f_lineno)
        self.check_information_time(shipment_time_2, "详情页出货时间", "代理方查看销售出货后的出货信息")

        total_Amount_3 = Ca().xpath_text_(xpath_front + '/div/div/div[4]/div[3]/div[1]/div[2]/div[2]/span',
                                                    sys._getframe().f_lineno)
        total_Amount_3 = re_sub_(total_Amount_3)
        self.check_information_if(str(total_Amount), total_Amount_3, "发货明细中货单金额", "代理方查看销售出货后的出货信息")

        Ca().xpath_click_(
            xpath_front + '/div/div/div[4]/div[1]/div/div/div/div/div[1]/div[3]', "点击查看进入操作记录", "代理方查看出货后的出货信息",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)

        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[1]',
            sys._getframe().f_lineno)
        self.check_information_if('采购商已收货', record_state1, "操作记录中出货状态", '代理方查看采购收货后的出货信息')

        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[2]',
            sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '代理方查看采购收货后的出货信息')

        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[3]',
            sys._getframe().f_lineno)
        self.check_information_time(record_time1, "操作记录中发起申请时间", '代理方查看采购收货后的出货信息')

    def purchaser_inspection(self):
        driver = self.driver
        print("*****代理方查看采购品检后的出货信息*****")

        Ca().slide_("0")

        Ca().xpath_click_('//*[@id="2$Menu"]/li[3]', "点击进入出货跟踪", "代理方查看采购品检后的出货信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        self.catalog_two(driver, "货物管理", "出货跟踪列表", "代理方查看采购品检后的出货信息", "出货单列表页一级目录", "出货单列表页二级目录")
        invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
        invoiceSn_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody/'
                                                                'tr[1]/td[1]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "出货单编号", "代理方查看采购品检后的出货信息")

        invoiceApplySn = gl.get_value('invoiceApplySn')  # 出货单编号 DO
        invoiceApplySn_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[2]', sys._getframe().f_lineno)
        self.check_information_if(invoiceApplySn, invoiceApplySn_1, "发货单编号", "代理方查看采购品检后的出货信息")

        supplier_name = gl.get_value('supplier_name')
        supplier_name_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                    '/tr[1]/td[3]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_1, "发货单位", "代理方查看采购品检后的出货信息")

        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[4]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位", "代理方查看采购品检后的出货信息")

        total_Amount = gl.get_value('total_Amount')  # 发货总金额
        total_Amount_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                  '/tr[1]/td[5]', sys._getframe().f_lineno)
        total_Amount_1 = re_sub_(total_Amount_1)
        self.check_information_if(str(total_Amount), total_Amount_1, "发货总金额", "代理方查看采购品检后的出货信息")

        shipment_time_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                    '/tr[1]/td[6]', sys._getframe().f_lineno)
        self.check_information_time(shipment_time_1, "出货时间", "代理方查看采购品检后的出货信息")

        shipment_state_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[7]', sys._getframe().f_lineno)
        self.check_information_if('正常', shipment_state_1, "出货状态", "代理方查看采购品检后的出货信息")

        goods_state_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                  '/tr[1]/td[8]', sys._getframe().f_lineno)
        self.check_information_if('待入库', goods_state_1, "货物状态", "代理方查看采购品检后的出货信息")

        Ca().xpath_click_(
            xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[9]/a/button', "点击查看进入详情页", "代理方查"
                                                                                                               "看出货后的出货信息",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "货物管理", "出货跟踪列表", "出货跟踪详情", "代理方查看采购品检后的出货信息",
                           "出货单列表页一级目录", "出货单列表页二级目录", '出货单列表页三级目录')

        goods_state_2 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/h3/span',
                                                    sys._getframe().f_lineno)
        self.check_information_if(goods_state_1, goods_state_2, "详情页货物状态", "代理方查看采购品检后的出货信息")

        invoiceSn_2 = Ca().xpath_text_('//*[@id="invoiceSn"]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_2, "详情页货物状态", "代理方查看采购品检后的出货信息")

        invoiceApplySn_2 = Ca().xpath_text_('//*[@id="invoiceApplySn"]', sys._getframe().f_lineno)
        self.check_information_if(invoiceApplySn, invoiceApplySn_2, "详情页发货申请单号", "代理方查看采购品检后的出货信息")

        contractnumber = gl.get_value('contractnumber')
        contractnumber_2 = Ca().xpath_text_('//*[@id="contractSn"]', sys._getframe().f_lineno)
        self.check_information_if(contractnumber, contractnumber_2, "详情页委托单号", "代理方查看采购品检后的出货信息")

        supplier_name_2 = Ca().xpath_text_('//*[@id="supplierName"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "详情页发货单位", "代理方查看采购品检后的出货信息")

        supplier_name_2 = Ca().xpath_text_('//*[@id="supplierName"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "详情页发货单位", "代理方查看销售出货后的出货信息")

        supplier_details_page = Ca().xpath_href_('//*[@id="supplierName"]/a', sys._getframe().f_lineno)
        new_execute_script(supplier_details_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方查看销售出货后的出货信息",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_3, "新页面中名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_name_2 = Ca().xpath_text_('//*[@id="purchaserName"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "详情页收货单位", "代理方查看销售出货后的出货信息")

        purchaser_details_page = Ca().xpath_href_('//*[@id="purchaserName"]/a', sys._getframe().f_lineno)
        new_execute_script(purchaser_details_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方查看销售出货后的出货信息",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        total_Amount_2 = Ca().xpath_text_('//*[@id="a"]', sys._getframe().f_lineno)
        total_Amount_2 = re_sub_(total_Amount_2)
        self.check_information_if(str(total_Amount), total_Amount_2, "详情页货单金额", "代理方查看采购品检后的出货信息")

        shipment_time_2 = Ca().xpath_text_('//*[@id="deliveryGoodTime"]', sys._getframe().f_lineno)
        self.check_information_time(shipment_time_2, "详情页出货时间", "代理方查看销售出货后的出货信息")

        total_Amount_3 = Ca().xpath_text_(xpath_front + '/div/div/div[4]/div[3]/div[1]/div[2]/div[2]/span',
                                                    sys._getframe().f_lineno)
        total_Amount_3 = re_sub_(total_Amount_3)
        self.check_information_if(str(total_Amount), total_Amount_3, "发货明细中货单金额", "代理方查看销售出货后的出货信息")

        Ca().xpath_click_(
            xpath_front + '/div/div/div[4]/div[1]/div/div/div/div/div[1]/div[3]', "点击查看进入操作记录", "代理方查看出货后的出货信息",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)

        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[1]',
            sys._getframe().f_lineno)
        self.check_information_if('采购商已品鉴', record_state1, "操作记录中出货状态", '代理方查看采购品检后的出货信息')

        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[2]',
            sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '代理方查看采购品检后的出货信息')

        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[3]',
            sys._getframe().f_lineno)
        self.check_information_time(record_time1, "操作记录中发起申请时间", '代理方查看采购品检后的出货信息')

    def purchaser_warehousing(self):
        driver = self.driver
        print("*****代理方查看采购入库后的出货信息*****")

        Ca().slide_("0")

        Ca().xpath_click_('//*[@id="2$Menu"]/li[3]', "点击进入出货跟踪", "代理方查看采购入库后的出货信息", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        self.catalog_two(driver, "货物管理", "出货跟踪列表", "代理方查看采购入库后的出货信息", "出货单列表页一级目录", "出货单列表页二级目录")
        invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
        invoiceSn_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody/'
                                                                'tr[1]/td[1]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "出货单编号", "代理方查看采购入库后的出货信息")

        invoiceApplySn = gl.get_value('invoiceApplySn')  # 出货单编号 DO
        invoiceApplySn_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[2]', sys._getframe().f_lineno)
        self.check_information_if(invoiceApplySn, invoiceApplySn_1, "发货单编号", "代理方查看采购入库后的出货信息")

        supplier_name = gl.get_value('supplier_name')
        supplier_name_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                    '/tr[1]/td[3]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_1, "发货单位", "代理方查看采购入库后的出货信息")

        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[4]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位", "代理方查看采购入库后的出货信息")

        total_Amount = gl.get_value('total_Amount')  # 发货总金额
        total_Amount_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                  '/tr[1]/td[5]', sys._getframe().f_lineno)
        total_Amount_1 = re_sub_(total_Amount_1)
        self.check_information_if(str(total_Amount), total_Amount_1, "发货总金额", "代理方查看采购入库后的出货信息")

        shipment_time_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                    '/tr[1]/td[6]', sys._getframe().f_lineno)
        self.check_information_time(shipment_time_1, "出货时间", "代理方查看采购入库后的出货信息")

        shipment_state_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                     '/tr[1]/td[7]', sys._getframe().f_lineno)
        self.check_information_if('正常', shipment_state_1, "出货状态", "代理方查看采购入库后的出货信息")

        goods_state_1 = Ca().xpath_text_(xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody'
                                                                  '/tr[1]/td[8]', sys._getframe().f_lineno)
        self.check_information_if('已入库', goods_state_1, "货物状态", "代理方查看采购入库后的出货信息")

        Ca().xpath_click_(
            xpath_front + '/div/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[9]/a/button', "点击查看进入详情页", "代理方查"
                                                                                                               "看出货后的出货信息",
            "云平台‘代理方’", sys._getframe().f_lineno)

        time.sleep(2.5)
        self.catalog_three(driver, "货物管理", "出货跟踪列表", "出货跟踪详情", "代理方查看采购品检后的出货信息",
                           "出货单列表页一级目录", "出货单列表页二级目录", '出货单列表页三级目录')

        goods_state_2 = Ca().xpath_text_(xpath_front + '/div/div/div[1]/div/h3/span',
                                                    sys._getframe().f_lineno)
        self.check_information_if(goods_state_1, goods_state_2, "详情页货物状态", "代理方查看采购入库后的出货信息")

        invoiceSn_2 = Ca().xpath_text_('//*[@id="invoiceSn"]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_2, "详情页货物状态", "代理方查看采购入库后的出货信息")

        invoiceApplySn_2 = Ca().xpath_text_('//*[@id="invoiceApplySn"]', sys._getframe().f_lineno)
        self.check_information_if(invoiceApplySn, invoiceApplySn_2, "详情页发货申请单号", "代理方查看采购入库后的出货信息")

        contractnumber = gl.get_value('contractnumber')
        contractnumber_2 = Ca().xpath_text_('//*[@id="contractSn"]', sys._getframe().f_lineno)
        self.check_information_if(contractnumber, contractnumber_2, "详情页委托单号", "代理方查看采购入库后的出货信息")

        supplier_name_2 = Ca().xpath_text_('//*[@id="supplierName"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "详情页发货单位", "代理方查看采购入库后的出货信息")

        supplier_name_2 = Ca().xpath_text_('//*[@id="supplierName"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "详情页发货单位", "代理方查看销售出货后的出货信息")

        supplier_details_page = Ca().xpath_href_('//*[@id="supplierName"]/a', sys._getframe().f_lineno)
        new_execute_script(supplier_details_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方查看销售出货后的出货信息",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_3, "新页面中名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_name_2 = Ca().xpath_text_('//*[@id="purchaserName"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "详情页收货单位", "代理方查看销售出货后的出货信息")

        purchaser_details_page = Ca().xpath_href_('//*[@id="purchaserName"]/a', sys._getframe().f_lineno)
        new_execute_script(purchaser_details_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方查看销售出货后的出货信息",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        total_Amount_2 = Ca().xpath_text_('//*[@id="a"]', sys._getframe().f_lineno)
        total_Amount_2 = re_sub_(total_Amount_2)
        self.check_information_if(str(total_Amount), total_Amount_2, "详情页货单金额", "代理方查看采购入库后的出货信息")

        shipment_time_2 = Ca().xpath_text_('//*[@id="deliveryGoodTime"]', sys._getframe().f_lineno)
        self.check_information_time(shipment_time_2, "详情页出货时间", "代理方查看销售出货后的出货信息")

        total_Amount_3 = Ca().xpath_text_(xpath_front + '/div/div/div[4]/div[3]/div[1]/div[2]/div[2]/span',
                                                    sys._getframe().f_lineno)
        total_Amount_3 = re_sub_(total_Amount_3)
        self.check_information_if(str(total_Amount), total_Amount_3, "发货明细中货单金额", "代理方查看销售出货后的出货信息")

        Ca().xpath_click_(
            xpath_front + '/div/div/div[4]/div[1]/div/div/div/div/div[1]/div[3]', "点击查看进入操作记录", "代理方查看出货后的出货信息",
            "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)

        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[1]',
            sys._getframe().f_lineno)
        self.check_information_if('采购商待收货', record_state1, "操作记录中出货状态", '代理方查看采购入库后的出货信息')

        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[2]',
            sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '代理方查看采购入库后的出货信息')

        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div/div[4]/div[3]/div[3]/div[2]/div[2]/div/ul/li[1]/div[3]/div/div[3]',
            sys._getframe().f_lineno)
        self.check_information_time(record_time1, "操作记录中发起申请时间", '代理方查看采购入库后的出货信息')

    def receive_invoice(self):  # 代理方收票
        print("*****代理方收票*****")
        driver = self.driver
        Ca().slide_("0")
        Ca().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入收票列表", "代理方收票", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击进入待收票",
                                     "代理方收票", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)

        self.list_three(driver, "全部", "未收票", "已收票", "代理方收票", "代理收票-全部列表",
                        "代理收票-未收票列表", "代理收票-已收票列表")
        receiptSn = gl.get_value('receiptSn')
        invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方企业名
        total_Amount = gl.get_value('total_Amount')  # # 货品总价 10000
        receiptSn_1 = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                                '/tbody/tr[1]/td[1]', sys._getframe().f_lineno)
        self.check_information_if(receiptSn, receiptSn_1, "收票单号", '代理方收票')
        invoiceSn_1 = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                                '/tbody/tr[1]/td[2]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "出货单号", '代理方收票')
        sendReceiptName_1 = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                                      '/tbody/tr[1]/td[3]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, sendReceiptName_1, "寄票单位", '代理方收票')
        totalAmount = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                                '/tbody/tr[1]/td[4]')
        self.check_information_if(str(total_Amount), totalAmount, "寄票金额", '代理方收票')
        supplierSendReceiptTime = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                                            '/tbody/tr[1]/td[5]')
        self.check_information_time(supplierSendReceiptTime, "寄票时间", '代理方收票')
        state_1 = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                            '/tbody/tr[1]/td[6]')
        self.check_information_if('代理商待收票', state_1, "寄票状态", '代理方收票')

        Ca().xpath_click_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button',
                                     "点击进入待收票-操作", "代理方收票", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_two(driver, "收票列表", "收票详情", "代理方收票", "收票详情页一级目录", "收票详情页二级目录")

        state_2 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[1]/span')
        self.check_information_if(state_2, state_1, "详情页寄票状态", '代理方收票')

        receiptSn_2 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[5]/div[2]',
                                                  sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, receiptSn_2, "详情页寄票单号", '代理方收票')

        sendReceiptName_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[6]/div[2]',
                                                        sys._getframe().f_lineno)
        self.check_information_if(supplier_name, sendReceiptName_1, "详情页寄票单位", '代理方收票')
        supplierSendReceiptTime = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[7]/div[2]',
                                                              sys._getframe().f_lineno)
        self.check_information_time(supplierSendReceiptTime, "详情页寄票时间", '代理方收票')
        totalAmount_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[8]/div[2]',
                                                    sys._getframe().f_lineno)
        self.check_information_if(str(total_Amount), totalAmount_1, "详情页寄票金额", '代理方收票')
        invoiceSn_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[10]/div[2]',
                                                  sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "详情页出货单号", '代理方收票')

        purchaser_name = gl.get_value('purchaser_name')
        purchaserName_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[11]/div[2]/a',
                                                      sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaserName_1, "详情页出收货方", '代理方收票')
        purchaserName_page = Ca().xpath_href_(xpath_front + '/div/div[1]/div[2]/div[1]/div[11]/div[2]/a',
                                                         sys._getframe().f_lineno)
        new_execute_script(purchaserName_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方收票",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中名称信息", "代理方收票")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        supplier_name_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[12]/div[2]/a',
                                                      sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_1, "详情页出发货方", '代理方收票')
        supplierName_page = Ca().xpath_href_(xpath_front + '/div/div[1]/div[2]/div[1]/div[12]/div[2]/a',
                                                        sys._getframe().f_lineno)
        new_execute_script(supplierName_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方收票",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, purchaser_name_3, "新页面中名称信息", "代理方收票")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        record_state1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div/div[2]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if('供应商已寄票', record_state1, '操作记录状态', '代理方收票')  # information"发起方修改合同申请"  step"修改合同"
        record_operator1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div/div[2]/div[2]/div/ul/li/div[3]/div/div[2]')
        self.check_information_if('18216482019_s', record_operator1, '操作记录操作人', '代理方收票')
        record_time1 = Ca().xpath_text_(
            xpath_front + '/div/div[1]/div[3]/div/div[3]/div/div[2]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time1, '操作记录时间', '代理方收票')

        Ca().xpath_click_(xpath_front + '/div/div[1]/div[2]/div[2]/span/button', "点击确认收票", "代理方收票",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]',
                                     "再次确认收票", "代理方收票", "云平台‘代理方’", sys._getframe().f_lineno)

        time.sleep(3)
        state_3 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[1]/span')
        self.check_information_if('代理商已收票', state_3, "详情页寄票状态", '代理方收票')

        agentReceiveReceiptTime = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[2]/div[2]',
                                                              sys._getframe().f_lineno)
        self.check_information_time(agentReceiveReceiptTime, "详情页寄票单号", '代理方收票')
        operatorName = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[3]/div[2]',
                                                   sys._getframe().f_lineno)
        self.check_information_if('13245678999_s', operatorName, "详情页寄票单号", '代理方收票')
        Ca().slide_("0", sys._getframe().f_lineno)
        Ca().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入收票列表", "代理方收票", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击进入已收票",
                                     "代理方收票", "云平台‘代理方’", sys._getframe().f_lineno)
        receiptSn = gl.get_value('receiptSn')
        receiptSn_ = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                               '/tbody/tr[1]/td[1]', sys._getframe().f_lineno)
        self.check_information_if(receiptSn, receiptSn_, "收票单号", '代理方收票')
        state_5 = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                            '/tbody/tr[1]/td[6]')
        self.check_information_if('代理商已收票', state_5, "寄票状态", '代理方收票')

    def send_invoice(self):  # 代理方寄票
        print("*****代理方寄票*****")
        driver = self.driver
        Ca().slide_("0")
        Ca().xpath_click_('//*[@id="3$Menu"]/li[2]', "点击进入收票列表", "代理方寄票", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击进入待寄票",
                                     "代理方寄票", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.list_three(driver, "全部", "未寄票", "已寄票", "代理方寄票", "代理寄票-全部列表",
                        "代理寄票-未寄票列表", "代理收票-已寄票列表")

        invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方企业名
        total_Amount = gl.get_value('total_Amount')  # # 货品总价 10000
        send_receiptSn = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[1]', sys._getframe().f_lineno)
        self.check_information_re('JP', send_receiptSn, "寄票单号", '代理方寄票')
        gl.set_value('send_receiptSn', send_receiptSn)  # 寄票单号
        invoiceSn_1 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[2]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "出货单号", '代理方寄票')
        purchaser_name = gl.get_value('purchaser_name')
        receiveReceiptName_1 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, receiveReceiptName_1, "收票单位", '代理方寄票')
        totalAmount = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                                '/tbody/tr[1]/td[4]')
        self.check_information_if(str(total_Amount), totalAmount, "寄票金额", '代理方寄票')
        state_1 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_if('代理商待寄票', state_1, "寄票状态", '代理方寄票')

        Ca().xpath_click_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/button',
                                     "点击进入待寄票-操作", "代理方寄票", "云平台‘代理方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_two(driver, "寄票列表", "寄票详情", "代理方寄票", "寄票详情页一级目录", "寄票详情页二级目录")

        state_2 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[1]/span')
        self.check_information_if(state_2, state_1, "详情页寄票状态", '代理方寄票')

        send_receiptSn_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[7]/div[2]',
                                                       sys._getframe().f_lineno)
        self.check_information_if(send_receiptSn, send_receiptSn_1, "详情页寄票单号", '代理方寄票')

        sendReceiptName_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[8]/div[2]',
                                                        sys._getframe().f_lineno)
        self.check_information_if(supplier_name, sendReceiptName_1, "详情页寄票单位", '代理方寄票')
        supplierSendReceiptTime = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[9]/div[2]',
                                                              sys._getframe().f_lineno)
        self.check_information_time(supplierSendReceiptTime, "详情页寄票时间", '代理方寄票')
        totalAmount_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[10]/div[2]',
                                                    sys._getframe().f_lineno)
        self.check_information_if(str(total_Amount), totalAmount_1, "详情页寄票金额", '代理方寄票')
        invoiceSn_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[12]/div[2]',
                                                  sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "详情页出货单号", '代理方寄票')

        purchaser_name = gl.get_value('purchaser_name')
        purchaserName_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[13]/div[2]/a',
                                                      sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaserName_1, "详情页出收货方", '代理方寄票')
        purchaserName_page = Ca().xpath_href_(xpath_front + '/div/div[1]/div[2]/div[1]/div[13]/div[2]/a',
                                                         sys._getframe().f_lineno)
        new_execute_script(purchaserName_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方寄票",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中名称信息", "代理方寄票")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        supplier_name_1 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[2]/div[1]/div[14]/div[2]/a',
                                                      sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_1, "详情页出发货方", '代理方寄票')
        supplierName_page = Ca().xpath_href_(xpath_front + '/div/div[1]/div[2]/div[1]/div[14]/div[2]/a',
                                                        sys._getframe().f_lineno)
        new_execute_script(supplierName_page)
        time.sleep(2.5)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代理方寄票",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Ca().xpath_text_(
            '//*[@id="name"]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, purchaser_name_3, "新页面中名称信息", "代理方寄票")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        Ca().xpath_click_(xpath_front + '/div/div[1]/div[2]/div[2]/span/button', "点击确认寄票", "代理方寄票",
                                     "云平台‘代理方’", sys._getframe().f_lineno)
        Ca().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]',
                                     "再次确认寄票", "代理方寄票", "云平台‘代理方’", sys._getframe().f_lineno)

        time.sleep(3)
        state_3 = Ca().xpath_text_(xpath_front + '/div/div[1]/div[1]/span')
        self.check_information_if('采购商待收票', state_3, "详情页寄票状态", '代理方寄票')

        Ca().slide_("0", sys._getframe().f_lineno)
        Ca().xpath_click_('//*[@id="3$Menu"]/li[2]', "点击进入收票列表", "代理方寄票", "云平台‘代理方’",
                                     sys._getframe().f_lineno)
        time.sleep(2.5)
        Ca().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击进入已收票",
                                     "代理方寄票", "云平台‘代理方’", sys._getframe().f_lineno)
        receiptSn = gl.get_value('receiptSn')
        receiptSn_ = Ca().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table'
                                                               '/tbody/tr[1]/td[1]', sys._getframe().f_lineno)
        self.check_information_if(receiptSn, receiptSn_, "收票单号", '代理方寄票')
        state_5 = Ca().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_if('采购商待收票', state_5, "寄票状态", '代理方寄票')
        time.sleep(0.5)

    def run(self):  # 实现主要逻辑
        # self.driver.get(self.start_url)
        self.login()

    def run0_5(self):  # 客户管理
        self.customer_management()

    def run1(self):  # 代理方同意委托
        self.agent_agree_contract()

    def run1_1(self):  # 代理方拒绝委托
        self.refuse_entrust()

    def run2(self):  # 代理方通过发货申请
        self.Delivery_application()

    def run2_1(self):  # 代理方拒绝发货申请
        self.refuse_delivery_application()

    def run3_1(self):  # 代理方查看供方出货后的货品信息
        self.supplier_deliver_goods()

    def run3_2(self):  # 代理方查看采方收货后的货品信息
        self.purchaser_collect()

    def run3_3(self):  # 代理方查看采方品检后的货品信息
        self.purchaser_inspection()

    def run3_4(self):  # 代理方查看采方入库后的货品信息
        self.purchaser_warehousing()

    def run4(self):  # 代理方收票/寄票
        self.receive_invoice()
        self.send_invoice()

    def run_excel(self):
        Ca().excel_write()  # 写入excel


if __name__ == '__main__':
    daili = PC_926_agent()
    daili.run()  # 代理方登录
    # daili.run0_5()  # 代理方拒绝委托
    # daili.run1_1()  # 代理方拒绝委托
    # daili.run1()  # 代理方同意委托
    # daili.run2_1()  # 代理方拒绝发货申请
    # daili.run2()  # 代理方通过发货申请
    # daili.run4()  # 代理方收票/寄票
    # daili.run_excel()
