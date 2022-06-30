# -- coding: utf-8 --
# @Author : Zw
# @File : PC_926_supplier.py

import os
import random
import re
import sys
import time
from decimal import *
from selenium.webdriver.common.by import By

import config.globalvar as gl
from config.config_supplier import Config_pc_supplier as Cs, Logger


def current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "-供应方-"
    return current_time


def service_coefficient(n, x):
    sum = float(n) * 0.00015 * float(x) / 100  # n发货金额 0.00015服务费系数 x服务费占比
    sum1 = '%.2f' % sum
    # print(sum1)
    return sum1


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
    return re_int2


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

number1 = random.randint(30, 100)
number2 = random.randint(30, 100)
c = random.uniform(10, 50)
price1 = round(c, 2)
d = random.uniform(10, 50)
price2 = round(d, 2)


def goods_iofo():  # 随机金额，数量 商品信息
    # global number2,number1
    e = number1 * price1
    f = number2 * price2
    amount1 = round(e, 2)  # 一类货品总价
    amount2 = round(f, 2)  # 二类货品总价
    totalAmount = amount1 + amount2
    amount_1 = Decimal(str(amount1)).quantize(Decimal('0.00'))
    amount_2 = Decimal(str(amount2)).quantize(Decimal('0.00'))
    total_Amount = Decimal(str(totalAmount)).quantize(Decimal('0.00'))

    return number1, number2, price1, price2, amount_1, amount_2, total_Amount


# 获取新的页面信息
def new_execute_script(test):
    global count
    count += 1
    print("count : %d" % count)
    driver = Cs().driver
    # 打开一个新页面
    driver.execute_script('window.open()')
    # 定位到新的页面
    driver.switch_to.window(driver.window_handles[count])
    driver.get(test)
    time.sleep(2.5)
    print("切换跳转至另一页面")
    # 定位回原来的页面
    # driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)


def tes1t_time():
    test_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return test_time


path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('log_pc.txt')

start_url = Cs.start_url
print("网址为：", start_url)
if re.findall('test', start_url) or re.findall('b.926.net', start_url):
    xpath_front = '//div[@class="ant-row"]/div/div[2]'
    xpath_front_1 = '//*[@id="root"]/div/section/div[2]/section/main/div/div/div/div[1]'
    xpath_front_2 = '//*[@id="root"]/div/section/div[3]/section/main/div/div/div/div[2]'
    xpath_main = '//main[@class="ant-layout-content"]'
    print('xpath信息为：', xpath_front)
else:
    xpath_front = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div[2]'
    xpath_front_1 = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div[1]'
    xpath_main = '//*[@id="root"]/div/div/div[2]/div[2]/div'
    print('xpath信息为：', xpath_front)


class PC_926_supplier():
    # object_name = print(sys._getframe().f_code.co_name)
    start_url = Cs().start_url
    driver = Cs().driver
    gl._init()
    a = 0

    def check_information_if(self, Check_value, capture, Check_contents, process):
        # time.sleep(0.2)
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if Check_value == capture:
            Cs().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % Check_value)
            Cs().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)

    # 正则判断，校验信息
    def check_information_re(self, Check_value, capture, Check_contents, process):
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if re.findall(Check_value, capture):
            Cs().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % Check_value)
            Cs().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)

    # 时间判断，校验信息
    def check_information_time(self, capture, Check_contents, process):
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if re.findall(tes1t_time(), capture):
            Cs().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % tes1t_time())
            Cs().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘发起方’", sys._getframe().f_lineno)

    # 校验操作记录
    def Operation_record(self, driver, information, information_user, step, check_info, check_time, check_user,
                         hierarchy):
        time.sleep(1)
        record_state1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[%s]/div[2]/ul/li/div[3]/div/div[1]' % hierarchy)
        self.check_information_if(information, record_state1, check_info, step)  # information"发起方修改合同申请"  step"修改合同"
        # Cs().is_toast_exist("获取发起合同后的操作状态", "修改合同", "云平台‘发起方’",sys._getframe().f_lineno)
        record_time1 = Cs().xpath_text_(xpath_front + '/div/div/div[3]/div[3]/div[%s]/div[2]/ul/li'
                                                      '/div[3]/div/div[3]' % hierarchy)
        self.check_information_time(record_time1, check_time, step)
        # Cs().is_toast_exist("获取发起合同后的操作时间", "修改合同", "云平台‘发起方’",sys._getframe().f_lineno)
        record_operator1 = Cs().xpath_text_(xpath_front + '/div/div/div[3]/div[3]/div[%s]/div[2]'
                                                          '/ul/li/div[3]/div/div[2]' % hierarchy)
        self.check_information_if(information_user, record_operator1, check_user, step)

    # 校验被拒绝后的操作记录
    def Operation_record_refuse(self, driver, information, information_user, step, check_info, check_time, check_user,
                                check_reason, check_details):
        time.sleep(1)
        if step == "查看被合作方拒绝的委托信息":
            cooperation_refuse_details = gl.get_value('cooperation_refuse_details')
            cooperation_refuse_reason = gl.get_value('cooperation_refuse_reason')
            refuse_reason1 = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[3]')
            self.check_information_re(cooperation_refuse_reason, refuse_reason1, check_reason, step)

            refuse_details1 = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[4]')
            self.check_information_re(cooperation_refuse_details, refuse_details1, check_details, step)
        else:
            agent_refuse_details = gl.get_value('agent_refuse_details')
            agent_refuse_reason = gl.get_value('agent_refuse_reason')
            refuse_reason1 = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[3]')
            self.check_information_re(agent_refuse_reason, refuse_reason1, check_reason, step)

            refuse_details1 = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[4]')
            self.check_information_re(agent_refuse_details, refuse_details1, check_details, step)
        record_state1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[1]')
        self.check_information_if(information, record_state1, check_info, step)

        record_time1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[5]')
        self.check_information_time(record_time1, check_time, step)

        record_operator1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[2]')
        self.check_information_if(information_user, record_operator1, check_user, step)

    def performance_record(self, driver, step):
        print("履行记录")
        time.sleep(2.5)
        total_Amount = gl.get_value('total_Amount')  # 货品总价
        price_sum_check_all_2 = gl.get_value('price_sum_check_all_2')  # 两种商品总价
        purchaser_name = gl.get_value('purchaser_name')
        agent_name = gl.get_value('agent_name')
        supplier_name = gl.get_value('supplier_name')
        invoiceApplySn = gl.get_value('invoiceApplySn')
        purchaser_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[1]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "履行记录中采购（甲）方公司名称", step)
        agent_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[3]/div[2]')
        self.check_information_if(agent_name, agent_name_1, "履行记录中代理（乙）方公司名称", step)
        supplier_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[2]/div[2]')
        self.check_information_if(supplier_name, supplier_name_1, "履行记录中销售方（丙）方公司名称", step)
        price_sum_check_all_ = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[4]/div[2]/span')
        self.check_information_re(price_sum_check_all_2, price_sum_check_all_, "履行记录中合同总价", step)
        total_Amount_ = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[5]/div/div[1]/div/div/span')
        self.check_information_re(str(total_Amount), total_Amount_, "履行记录中发货商品总价", step)
        # todo 校验代理通过时间
        if step == "校验代理方通过审批后的合同":
            application_adopt_time = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[5]/div/div[2]/div/div[1]/div[2]')
            self.check_information_time(application_adopt_time, "履行记录中发货申请通过时间", step)
            state_ = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[5]/div/div[2]/div/div[2]/div[2]')
            self.check_information_if("发货", state_, "履行记录中发货方出货时间", step)
            invoiceApplySn_ = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[5]/div/div[2]/div/div[3]/div[2]')
            self.check_information_if(invoiceApplySn, invoiceApplySn_, "履行记录中发货申请单号", step)

    # 获取并校验导航信息（导航有两步）
    def navigation_two(self, driver, information_1, information_2, step, check_info_1, check_info_2):

        navigation_1 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div[1]/div[3]/div')
        self.check_information_if(information_1, navigation_1, check_info_1, step)
        navigation_2 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div[2]/div[3]/div')
        self.check_information_if(information_2, navigation_2, check_info_2, step)

    # 获取并校验导航信息（导航有三步）
    def navigation_three(self, driver, information_1, information_2, information_3, step,
                         check_info_1, check_info_2, check_info_3):

        navigation_1 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[1]/div[3]/div')
        self.check_information_if(information_1, navigation_1, check_info_1, step)
        navigation_2 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[2]/div[3]/div')
        self.check_information_if(information_2, navigation_2, check_info_2, step)
        navigation_3 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[3]/div[3]/div')
        self.check_information_if(information_3, navigation_3, check_info_3, step)

    # 获取并校验导航信息（导航有四步）
    def navigation_four(self, driver, information_1, information_2, information_3, information_4, step,
                        check_info_1, check_info_2, check_info_3, check_info_4):
        navigation_1 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[1]/div[3]/div')
        self.check_information_if(information_1, navigation_1, check_info_1, step)
        navigation_2 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[2]/div[3]/div')
        self.check_information_if(information_2, navigation_2, check_info_2, step)
        navigation_3 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[3]/div[3]/div')
        self.check_information_if(information_3, navigation_3, check_info_3, step)
        navigation_4 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[4]/div[3]/div')
        self.check_information_if(information_4, navigation_4, check_info_4, step)

    # 获取并校验页面目录信息（导航有两步）
    def catalog_two(self, driver, information_1, information_2, step, check_info_1, check_info_2):
        catalog_1 = Cs().xpath_text_(xpath_front_1 + '/div/span[1]/span[1]/span')
        self.check_information_if(information_1, catalog_1, check_info_1, step)
        catalog_2 = Cs().xpath_text_(xpath_front_1 + '/div/span[2]/span[1]/span')
        self.check_information_if(information_2, catalog_2, check_info_2, step)

    # 获取并校验页面目录信息（导航有三步）
    def catalog_three(self, driver, information_1, information_2, information_3, step,
                      check_info_1, check_info_2, check_info_3):
        catalog_1 = Cs().xpath_text_(xpath_front_1 + '/div/span[1]/span[1]/span')
        self.check_information_if(information_1, catalog_1, check_info_1, step)
        catalog_2 = Cs().xpath_text_(xpath_front_1 + '/div/span[2]/span[1]//span')
        self.check_information_if(information_2, catalog_2, check_info_2, step)
        catalog_3 = Cs().xpath_text_(xpath_front_1 + '/div/span[3]/span[1]/span')
        self.check_information_if(information_3, catalog_3, check_info_3, step)

    # 获取并校验页面分类列表信息（列表有三类）
    def list_three(self, driver, information_1, information_2, information_3, step,
                   check_info_1, check_info_2, check_info_3):
        classification_1 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

    # 获取并校验页面分类列表信息（列表有四类）
    def list_four(self, driver, information_1, information_2, information_3, information_4, step,
                  check_info_1, check_info_2, check_info_3, check_info_4):
        classification_1 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

    # 获取并校验页面分类列表信息（列表有五类）
    def list_five(self, driver, information_1, information_2, information_3, information_4, information_5, step,
                  check_info_1, check_info_2, check_info_3, check_info_4, check_info_5):
        classification_1 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

        classification_5 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]')
        self.check_information_if(information_5, classification_5, check_info_5, step)

    # 获取并校验页面分类列表信息（列表有6类）
    def list_six(self, driver, information_1, information_2, information_3, information_4, information_5, information_6,
                 step,
                 check_info_1, check_info_2, check_info_3, check_info_4, check_info_5, check_info_6):
        classification_1 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

        classification_5 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]')
        self.check_information_if(information_5, classification_5, check_info_5, step)

        classification_6 = Cs().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[6]')
        self.check_information_if(information_6, classification_6, check_info_6, step)

    def list_contents_seven(self, driver, step, information_1, information_2, information_3,
                            information_4, information_5, information_6, check_info_2, check_info_3,
                            check_info_4, check_info_5, check_info_6):
        purchaser_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]')
        self.check_information_re(check_info_2, purchaser_name_1, information_1, step)
        agent_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_re(check_info_3, agent_name_1, information_2, step)
        supplier_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[4]')
        self.check_information_re(check_info_4, supplier_name_1, information_3, step)
        price_sum_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_re(check_info_5, price_sum_1, information_4, step)
        a_time = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[6]/div')
        self.check_information_time(a_time, information_5, step)
        state_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[7]/div')
        self.check_information_if(check_info_6, state_1, information_6, step)

    def list_contents_eight(self, driver, step, information_1, information_2, information_3,
                            information_4, information_5, information_6, information_7, check_info_2, check_info_3,
                            check_info_4, check_info_5, check_info_6, check_info_7):
        purchaser_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]')
        self.check_information_re(check_info_2, purchaser_name_1, information_1, step)
        agent_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_re(check_info_3, agent_name_1, information_2, step)
        supplier_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[4]')
        self.check_information_re(check_info_4, supplier_name_1, information_3, step)
        type_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[5]/div')
        self.check_information_if(check_info_7, type_1, information_7, step)
        price_sum_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[6]')
        self.check_information_re(check_info_5, price_sum_1, information_4, step)
        a_time = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[7]/div')
        self.check_information_time(a_time, information_5, step)
        state_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[8]/div')
        self.check_information_if(check_info_6, state_1, information_6, step)

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

        apply_number = gl.get_value('apply_number')
        # global x
        x = 0
        if step != "查看发起后的合同信息":
            x = 2
        purchaser_name_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (39 + x))
        print(purchaser_name_1)
        self.check_information_if(purchaser_name, purchaser_name_1, "合同内容中采购（甲）方公司名称", step)
        purchaser_926_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (43 + x))
        self.check_information_if(purchaser_926, purchaser_926_1, "合同内容中采购（甲）方公司926链号", step)
        purchaser_contacts_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (47 + x))
        self.check_information_if('东方联系人', purchaser_contacts_1, "合同内容中采购（甲）方联系人", step)
        purchaser_phone_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (50 + x))
        self.check_information_if('东方联系号码', purchaser_phone_1, "合同内容中采购（甲）方号码", step)
        purchaser_email_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (54 + x))
        self.check_information_if(purchaser_email, purchaser_email_1, "合同内容中采购（甲）方邮箱", step)
        purchaser_address_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (58 + x))
        self.check_information_if(purchaser_address, purchaser_address_1, "合同内容中采购（甲）方地址", step)
        purchaser_bank_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (62 + x))
        self.check_information_if(purchaser_bank, purchaser_bank_1, "合同内容中采购（甲）方开户行", step)
        purchaser_account_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (66 + x))
        self.check_information_if(purchaser_account, purchaser_account_1, "合同内容中采购（甲）方账号", step)

        agent_name_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (40 + x))
        self.check_information_if(agent_name, agent_name_1, "合同内容中代理（乙）方公司名称", step)
        agent_926_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (44 + x))
        self.check_information_if(agent_926, agent_926_1, "合同内容中代理（乙）方公司926链号", step)
        # agent_contacts_1 = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (48+x) ).text
        # self.check_information_if('天河联系人', agent_contacts_1, "合同内容中代理（乙）方联系人", step)
        agent_phone_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (51 + x))
        self.check_information_if('18823772926', agent_phone_1, "合同内容中代理（乙）方号码", step)
        agent_email_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (55 + x))
        self.check_information_if('926@926.net.cn', agent_email_1, "合同内容中代理（乙）方邮箱", step)
        # agent_address_1 = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (59+x) ).text
        # self.check_information_if(agent_address, agent_address_1, "合同内容中代理（乙）方地址", step)
        agent_bank_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (63 + x))
        self.check_information_if('招商银行股份有限公司深圳科发支行', agent_bank_1, "合同内容中代理（乙）方开户行", step)
        agent_account_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (67 + x))
        self.check_information_if('755940017210601', agent_account_1, "合同内容中代理（乙）方账号", step)

        supplier_name_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (41 + x))
        self.check_information_if(supplier_name, supplier_name_1, "合同内容中销售（丙）方公司名称", step)
        supplier_926_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (45 + x))
        self.check_information_if(supplier_926, supplier_926_1, "合同内容中销售（丙）方公司926链号", step)
        supplier_contacts_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (48 + x))
        self.check_information_if('天河联系人', supplier_contacts_1, "合同内容中销售（丙）方联系人", step)
        supplier_phone_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (52 + x))
        self.check_information_if('天河联系号码', supplier_phone_1, "合同内容中销售（丙）方号码", step)
        supplier_email_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (56 + x))
        self.check_information_if(supplier_email, supplier_email_1, "合同内容中销售（丙）方邮箱", step)
        supplier_address_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (60 + x))
        self.check_information_re(supplier_address_1, supplier_address, "合同内容中销售（丙）方地址", step)
        supplier_bank_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (64 + x))
        self.check_information_if(supplier_bank, supplier_bank_1, "合同内容中销售（丙）方开户行", step)
        supplier_account_1 = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (68 + x))
        self.check_information_if(supplier_account, supplier_account_1, "合同内容中销售（丙）方账号", step)

        contractnumber = Cs().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (1))
        gl.set_value('contractnumber', contractnumber[6:])

        # 校验编辑前的合同信息
        if step == "查看发起后的合同信息":
            number1, number2, price1, price2, amount_1, amount_2, total_Amount = goods_iofo()
            goods_name = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[77]')
            self.check_information_if("接线盒盖毛坯", goods_name, "合同内容中商品名称", step)

            # specifications = Cs().xpath_text_('//*[@id="goodVOsTD"]/tr/th[2]')
            # self.check_information_if("", specifications, "合同内容中商品规格", step)

            number = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[78]')
            self.check_information_if("%s(件)" % number1, number, "合同内容中商品数量", step)

            unit_price = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[79]')
            self.check_information_if(str(price1), unit_price, "合同内容中商品单价", step)

            total_price = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[80]')
            self.check_information_if(amount_1, total_price, "合同内容中商品总价", step)

            full_price = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[93]')
            self.check_information_if(str(amount_1), full_price, "合同内容中商品总价", step)

            zufs = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[25]')
            self.check_information_re("现金付款", zufs, "合同内容中支付方式", step)
            self.check_information_re("xybh", zufs, "合同内容中协议编号", step)
        # 校验编辑后的合同信息
        else:
            number1, number2, price1, price2, amount_1, amount_2, total_Amount = goods_iofo()
            goods_name = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (77 + x))
            self.check_information_if("接线盒盖毛坯", goods_name, "合同内容中一类商品名称", step)

            # specifications = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (78+x) ).text
            # self.check_information_if("", specifications, "合同内容中商品规格", step)

            number = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (78 + x))
            self.check_information_if("%s(件)" % number1, number, "合同内容中一类商品数量", step)

            unit_price = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (79 + x))
            self.check_information_if(str(price1), unit_price, "合同内容中一类商品单价", step)

            total_price = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (80 + x))
            self.check_information_if(amount_1, total_price, "合同内容中一类商品总价", step)

            goods_name = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (82 + x))
            self.check_information_if("接线盒盖", goods_name, "合同内容中二类商品名称", step)

            specifications = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (83 + x))
            self.check_information_if("TF", specifications, "二类合同内容中二类商品规格", step)

            number222 = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (84 + x))
            self.check_information_if("%s(件)" % number2, number222, "合同内容中二类商品数量", step)

            unit_price2 = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (85 + x))
            self.check_information_if(str(price2), unit_price2, "合同内容中二类商品单价", step)

            total_price2 = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (86 + x))
            self.check_information_if(amount_2, total_price2, "合同内容中二类商品总价", step)

            full_price = Cs().xpath_text_(
                '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (100))
            self.check_information_if(str(total_Amount), full_price, "合同内容中商品总价", step)

            zufs = Cs().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (25 + x))
            self.check_information_re("货到开银行承兑汇票", zufs, "合同内容中支付方式", step)
            # self.check_information_re("xybh", zufs, "合同内容中协议编号", step)

        # 释放iframe
        # driver.switch_to_default_content()

        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[3]', "点击查看申请信息",
                          step, "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        purchaser_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_2, "采购（甲）方公司名称", step)

        purchaser_926_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]')
        self.check_information_if(purchaser_926, purchaser_926_2, "采购（甲）方公司926链号", step)
        purchaser_email_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[2]')
        self.check_information_if(purchaser_email, purchaser_email_2, "采购（甲）方邮箱", step)
        purchaser_contacts_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[4]/div/div[2]')
        self.check_information_if('东方联系人', purchaser_contacts_2, "采购（甲）方联系人", step)
        purchaser_phone_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[5]/div/div[2]')
        self.check_information_if('东方联系号码', purchaser_phone_2, "采购（甲）方联系号码", step)

        agent_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[2]')
        self.check_information_if(agent_name, agent_name_2, "代理（乙）方公司名称", step)
        agent_926_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[2]')
        self.check_information_if(agent_926, agent_926_2, "代理（乙）方公司名称", step)
        agent_email_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[3]/div/div[2]')
        self.check_information_if(agent_email_1, agent_email_2, "代理（乙）方邮箱", step)

        # agent_contacts_2 = Cs().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[4]/div/div[2]')
        # self.check_information_if('朱丹', agent_contacts_2, "代理（乙）方联系人", step)

        agent_phone = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[5]/div/div[2]')
        self.check_information_if(agent_phone_1, agent_phone, "代理（乙）方联系电话", step)

        supplier_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[1]/div/div[2]')
        self.check_information_if("(发起方)%s" % supplier_name, supplier_name_2, "销售方（丙）方公司名称", step)

        supplier_926_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[2]/div/div[2]')
        self.check_information_if(supplier_926, supplier_926_2, "销售方（丙）方公司926链号", step)

        supplier_email_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[3]/div/div[2]')
        self.check_information_if(supplier_email, supplier_email_2, "销售方（丙）方邮箱", step)

        supplier_contacts_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[4]/div/div[2]')
        self.check_information_if('天河联系人', supplier_contacts_2, "销售方（丙）方联系人", step)

        supplier_phone_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[5]/div/div[2]')
        self.check_information_if('天河联系号码', supplier_phone_2, "销售方（丙）方电话", step)

        Cs().slide_("500")
        picture_1 = Cs().xpath_href_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]'
                          '/div[2]/div[1]/span/div[1]/div/div/span/a[1]')

        self.check_information_re("625b4822e90d95601e40dcdf7335b7ac.jpg", picture_1, "合同图片信息", step)

        if step == "查看发起后的合同信息":  # 校验原始合同编号,商品总价
            contract_mark = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[2]')
            self.check_information_if("6228484735", contract_mark, "原始合同编号", step)

            protocolSignTimeStr = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[1]/div')
            self.check_information_re('20', protocolSignTimeStr, "协议签订日期", step)
            protocolNumber = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]')
            self.check_information_re('xybh', protocolNumber, "协议编号", step)
            deliveryTypeName = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[3]/div/div[2]')
            self.check_information_re('甲方自提', deliveryTypeName, "收货方式", step)
            secondPaymentTypeName = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[4]/div/div[2]')
            self.check_information_re('现金付款', secondPaymentTypeName, "乙方付款方式:", step)
            price_sum = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[4]/div/div[2]')
            self.check_information_re(str(amount_1), price_sum, "商品总价", step)

        else:
            contract_mark = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[2]')
            self.check_information_if("62284844935", contract_mark, "原始合同编号", step)
            gl.set_value('contract_mark', contract_mark)
            # price_sum = Cs().xpath_text_(
            #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div/div[2]')
            # self.check_information_re(total_Amount, price_sum, "商品总价", step)

            protocolSignTimeStr = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[1]/div')
            self.check_information_re('20', protocolSignTimeStr, "协议签订日期", step)
            protocolNumber = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]')
            self.check_information_re('xybh', protocolNumber, "协议编号", step)
            deliveryTypeName = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[3]/div/div[2]')
            self.check_information_re('甲方自提', deliveryTypeName, "交货方式", step)
            secondPaymentTypeName = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[4]/div/div[2]')
            self.check_information_re('银行承兑汇票', secondPaymentTypeName, "乙方付款方式:", step)
            receiptTerm = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[1]/div/div[2]')
            self.check_information_re('5个月', receiptTerm, "汇票期限:", step)
            secondAcceptanceDraftTimeTypeName = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[2]/div/div[2]')
            self.check_information_re('货到开银行承兑汇票', secondAcceptanceDraftTimeTypeName, "乙方开承兑汇票时间:", step)
            thirdReceiptTimeTypeName = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[3]/div/div[2]')
            self.check_information_re('乙方开银行承兑汇票前', thirdReceiptTimeTypeName, "*丙方开发票时间:", step)
            thirdReceiptTimeNum = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[4]/div/div[2]')
            self.check_information_re('150天', thirdReceiptTimeNum, "乙方开银行承兑汇票前:", step)
            Cs().slide_('750')
            price_sum = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[4]/div/div[2]')
            self.check_information_re(str(total_Amount), price_sum, "商品总价", step)

            gl.set_value('protocolSignTimeStr', protocolSignTimeStr)
            gl.set_value('protocolNumber', protocolNumber)
            gl.set_value('deliveryTypeName', deliveryTypeName)
            gl.set_value('secondPaymentTypeName', secondPaymentTypeName)
            gl.set_value('receiptTerm', receiptTerm)
            gl.set_value('secondAcceptanceDraftTimeTypeName', secondAcceptanceDraftTimeTypeName)
            gl.set_value('thirdReceiptTimeTypeName', thirdReceiptTimeTypeName)
            gl.set_value('thirdReceiptTimeNum', thirdReceiptTimeNum)

        settlement_date = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[3]/div/div[2]')
        self.check_information_if('票到3天', settlement_date, "结算方式", step)
        gl.set_value("settlement_date", settlement_date)

        application_number = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]/div/div[2]')
        self.check_information_if(apply_number, application_number, "发起合同编号", step)
        contractnumber = gl.get_value('contractnumber')
        contractnumber_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[2]')
        if re.findall(tes1t_time(), contractnumber_2):
            self.check_information_time(contractnumber_2, "内部提交时间", step)
            submission_time = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[3]/div/div[2]')
            time.sleep(0.5)
            if re.findall(tes1t_time(), submission_time):
                self.check_information_time(contractnumber_2, "合作方审签时间", step)
                contractnumber_2 = Cs().xpath_text_(
                    xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[4]/div/div[2]')
                if re.findall(tes1t_time(), contractnumber_2) and step != "查看被代理方拒绝的委托信息":
                    self.check_information_time(contractnumber_2, "合作方审签时间", step)
                    time.sleep(0.5)
                    contractnumber_3 = Cs().xpath_text_(
                        xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[5]/div/div[2]')

                else:
                    pass
            else:
                pass
        else:
            self.check_information_re(contractnumber, contractnumber_2, "合同编号", step)

        # Cs().slide_("0")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[2]', "点击查看附件信息",
                          step, "云平台‘发起方’", sys._getframe().f_lineno)

        picture_2 = Cs().xpath_href_(xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]/span'
                                                   '/div[1]/div/div/span/a[1]')
        # print('picture_1 = %s' % picture_1)
        # print('picture = %s' % picture)
        self.check_information_if(str(picture_1), str(picture_2), "原始合同图片", step)

        # 校验原始合同编号
        if step == "查看发起后的合同信息":
            contract_mark = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[2]')
            self.check_information_if("6228484735", contract_mark, "原始合同编号", step)
        else:
            contract_mark = Cs().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[2]')
            self.check_information_if("62284844935", contract_mark, "原始合同编号", step)

        settlement = Cs().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[3]/div/div[2]')
        self.check_information_if(settlement_date, settlement, "结算方式", step)
        gl.set_value('settlement_date', settlement_date)

    def login(self):
        driver = self.driver
        start_url = self.start_url
        driver.get(start_url)
        Cs().name_click_("ant-menu-item", "点击密码登录", "登录", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().id_clear_("手机号")
        if re.findall('test', start_url):
            Cs().id_send_("手机号", "18216482019", )  # 测试
            Cs().is_toast_exist("输入正确的手机号", "登录", "云平台‘发起方’", sys._getframe().f_lineno)
        elif re.findall('10.', start_url):  # 开发
            Cs().id_send_("手机号", "18216482019")  # 开发
            Cs().is_toast_exist("输入正确的手机号", "登录", "云平台‘发起方’", sys._getframe().f_lineno)
        elif re.findall('pre', start_url):  # 预生产
            Cs().id_send_("手机号", "18216482019")  # 生产测试账号 15183834489   生产通用账号 18216482019
            Cs().is_toast_exist("输入正确的手机号", "登录", "云平台‘发起方’", sys._getframe().f_lineno)
        else:
            Cs().id_send_("手机号", "15183834489")  # 生产测试账号 15183834489
            Cs().is_toast_exist("输入正确的手机号", "登录", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().id_clear_("密码")
        Cs().id_send_("密码", "123456")
        Cs().is_toast_exist("输入正确的密码", "登录", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_("//button[@class='ant-btn login-form-button ant-btn-primary']", "点击登录",
                          "登录", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_('//*[@id="1$Menu"]/li', "点击进入企业实名认证", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        supplier_name = Cs().xpath_text_('//*[@id="7448-753004"]', "获取企业名称", "发起合同", "云平台‘发起方’",
                                         sys._getframe().f_lineno)

        Cs().text_click_("云平台", "进入926云平台", "登录", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        # catalog = Cs().xpath_text_('//*[@id="root"]/div/section/div[2]/div/div/div/div/div/div/ul/li[1]/div/span/span', sys._getframe().f_lineno)
        # self.check_information_if("合同管理", catalog, "成功进入云平台", "进入926云平台")
        # gl.set_value('supplier_name',supplier_name) # 供方企业名
        Cs().xpath_click_('//*[@id="10$Menu"]/li[1]', "点击进入云平台认证", "获取企业信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        Cs().xpath_click_(xpath_front + '/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[4]/button',
                          "点击进入云平台认证详情", "获取企业信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        Cs().slide_("800")
        # js = "window.scrollTo(100,2000);"
        # driver.execute_script(js)
        supplier_address = Cs().xpath_text_(
            '//*[@id="0地址"]', "获取供应方地址", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        supplier_email = Cs().xpath_text_(
            '//*[@id="4指定邮箱"]', "获取供应方邮箱 ", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        # Cs().slide_("2500")
        # driver.execute_script('window.scrollBy(0,2500)')
        # target = driver.find_element_by_xpath('//*[@id="4指定邮箱"]')
        # driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去

        # '//*[@id="root"]/div/section/div[2]/section/main/div/div/div/div[2]/div/div/div[3]/div[2]/div[6]/div/div[2]/div/div[3]/div[1]/div/div[2]/div/span/id',
        supplier_bank = Cs().xpath_text_('//*[@id="3开户银行（含支行）"]',
            "获取供应方开户银行 ", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        supplier_account = Cs().xpath_text_(
            '//*[@id="1企业银行账号"]', "获取银行账号 ", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().is_toast_exist("获取企业信息完毕", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        gl.set_value('supplier_name', supplier_name)
        gl.set_value('supplier_address', supplier_address)  # 获取供应方地址
        gl.set_value('supplier_email', supplier_email)  # 获取供应方邮箱
        gl.set_value('supplier_bank', supplier_bank)  # 获取供应方开户银行
        gl.set_value('supplier_account', supplier_account)  # 获取供应方银行账号
        print(supplier_name, supplier_address, supplier_email, supplier_bank, supplier_account)

    def contract(self):
        driver = self.driver
        print("*****发起方提交合同申请*****")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "点击进入合同签审", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        # 校验目录信息
        self.catalog_two(driver, "合同管理", "合同审签列表", "发起合同", "合同审签列表页一级目录", "合同审签列表页二级目录")
        self.list_four(driver, "全部", "我方待审签", "合作方待审签", "受托方待审签", "发起合同", "合同签审-全部列表",
                       "合同签审-我方待审批列表", "合同签审-合作方待审批列表", "合同签审-受托方待审批列表")

        Cs().xpath_click_("//button[@class='ant-btn ant-btn-primary']", "点击发起委托", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        # 校验发起委托页面①中的目录以及导航信息
        self.catalog_three(driver, "合同管理", "合同审签", "发起委托", "发起合同", "发起委托一级目录", "发起委托二级目录", "发起委托三级目录")
        self.navigation_two(driver, "选择三方信息", "填写申请单详情", "发起合同", "发起合同第一步导航信息", "发起合同第二步导航信息")

        # 发起委托
        Cs().name_click_("ant-select-selection__rendered", "选择角色", "发起合同", "云平台‘发起方’",
                         sys._getframe().f_lineno)
        time.sleep(0.5)
        # 选择成为供应商
        Cs().xpath_click_("//li[@class='ant-select-dropdown-menu-item"
                          " ant-select-dropdown-menu-item-active']", "选择成为供应商", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        # 选择代理商
        Cs().xpath_click_('//*[@id="RightRouteDiv"]/div/div/div/div[2]/div/div/div[2]/div[3]/div/input', "选择代理方", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_("//tr[@class='ant-table-row ant-table-row-level-0']/td[2]", "选中代理方", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[4]/div/input', "选择合作方", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        Cs().xpath_click_("//tr[@class='ant-table-row ant-table-row-level-0']", "选中合作方", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        start_url = self.start_url
        purchaser_email = gl.get_value('purchaser_email')
        if re.findall('test',start_url):
            link = Cs().xpath_text_(xpath_main + '/div/div/div/div[2]/div/div/div[2]/div[5]/div/div[2]')
            self.check_information_if("71316798", link, "926链号", "发起合同")
        else:
            link = Cs().xpath_text_(xpath_main + '/div/div/div/div[2]/div/div/div[2]/div[5]/div/div[2]')
            self.check_information_if("00386990", link, "926链号", "发起合同")
        email = Cs().xpath_text_(xpath_main + '/div/div/div/div[2]/div/div/div[2]/div[6]/div/div[2]')
        self.check_information_if(purchaser_email, email, "邮箱", "发起合同")
        # phone = Cs().xpath_text_(xpath_main + '/div/div/div/div[2]/div/div/div[2]/div[7]/div/div[2]')
        # self.check_information_if("15884564576", phone, "联系电话", "发起合同")

        Cs().xpath_click_("//button[@class='ant-btn ant-btn-primary']", "点击'下一步'进入已发起委托", "发起合同",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)

        # 校验发起委托页面②中的目录以及导航信息
        self.catalog_three(driver, "合同管理", "合同审签", "发起委托", "发起合同", "发起委托②一级目录", "发起委托②二级目录", "发起委托②三级目录")
        self.navigation_two(driver, "选择三方信息", "填写申请单详情", "发起合同", "发起合同第一步导航信息", "发起合同第二步导航信息")

        # 获取并校验三方信息
        purchaser_name = gl.get_value('purchaser_name')  # 采方企业名
        purchaser_email = gl.get_value('purchaser_email')  # 采方企业名
        purchaser_name1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[1]/div[2]/div[1]/div/div[2]')
        self.check_information_if(purchaser_name, purchaser_name1, "甲（采购）方企业名", "发起合同")
        
        if re.findall('test',start_url):
            purchaser_926 = Cs().xpath_text_(
                xpath_front + '/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]')
            self.check_information_if("71316798", purchaser_926, "甲（采购）方926链号", "发起合同")
        else:
            purchaser_926 = Cs().xpath_text_(
                xpath_front + '/div/div/div[2]/div[1]/div[2]/div[2]/div/div[2]')
            self.check_information_if("00386990", purchaser_926, "甲（采购）方926链号", "发起合同")
        
        purchaser_email1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[1]/div[2]/div[3]/div/div[2]')
        self.check_information_if(purchaser_email, purchaser_email1, "甲（采购）方邮箱", "发起合同")
        Cs().xpath_send_(xpath_front + '/div/div/div[2]/div[1]/div[2]/div[4]/div/input', "东方联系人")
        Cs().is_toast_exist("输入采购方联系人", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(xpath_front + '/div/div/div[2]/div[1]/div[2]/div[5]/div/input', "东方联系号码")
        Cs().is_toast_exist("输入采购方联系号码", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        agent_name = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[1]/div[3]/div[1]/div/div[2]')
        self.check_information_if("深圳926", agent_name, "乙（代理)方企业名", "发起合同")
        agent_926 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[1]/div[3]/div[2]/div/div[2]')
        self.check_information_if("27861194", agent_926, "乙（代理)方926链号", "发起合同")
        agent_email = Cs().xpath_text_(xpath_front + '/div/div/div[2]/div[1]/div[3]/div[3]/div/div[2]')
        self.check_information_if("926service@926.com", agent_email, "乙（代理)方邮箱", "发起合同")
        # agent_contacts = Cs().xpath_text_(xpath_front + '/div/div/div[2]/div[1]/div[3]/div[5]/div/div[2]')
        # self.check_information_if("18823772926", agent_phone, "乙（代理)方联系人", "发起合同")
        agent_phone = Cs().xpath_text_(xpath_front + '/div/div/div[2]/div[1]/div[3]/div[5]/div/div[2]')
        self.check_information_if("17051202834", agent_phone, "乙（代理)方联系号码", "发起合同")

        supplier_name = gl.get_value('supplier_name')  # 采方企业名
        supplier_email = gl.get_value('supplier_email')  # 采方企业名
        supplier_name1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[1]/div[4]/div[1]/div/div[2]')
        self.check_information_if(supplier_name, supplier_name1, "丙（销售)方企业名", "发起合同")
        supplier_926 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[1]/div[4]/div[2]/div/div[2]')
        self.check_information_if("03355125", supplier_926, "丙（销售)方926链号", "发起合同")
        supplier_email1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[1]/div[4]/div[3]/div/div[2]')
        self.check_information_if(supplier_email, supplier_email1, "丙（销售)方邮箱", "发起合同")
        # supplier_phone = Cs().xpath_text_(
        #     xpath_front + '/div/div/div[2]/div[1]/div[4]/div[4]/div/div[2]')
        # self.check_information_if("15234521231", supplier_phone, "丙（销售)方电话", "发起合同")
        Cs().xpath_send_(xpath_front + '/div/div/div[2]/div[1]/div[4]/div[4]/div/input', "天河联系人")
        Cs().is_toast_exist("输入销售方联系人", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(xpath_front + '/div/div/div[2]/div[1]/div[4]/div[5]/div/input', "天河联系号码")
        Cs().is_toast_exist("输入销售方联系号码", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)

        Cs().xpath_send_(
            '//span[@class="CustomAntUpload"]/div[2]/span/input[@type="file"]', "D:\shangwo\图片信息\合同1.jpg")  # 上传图片
        Cs().is_toast_exist("上传图片", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_clear_(xpath_front + '/div/div/div[2]/div[2]/div[2]/div[2]/div/input')  # 清空原始合同编号
        time.sleep(2.5)
        Cs().xpath_send_(xpath_front + '/div/div/div[2]/div[2]/div[2]/div[2]/div/input',
                         "6228484735")  # 输入原始合同编号
        Cs().is_toast_exist("输入原始合同编号", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[2]/div[2]/div[3]/div/input', "点击选择结算方式",
                          "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # Cs().xpath_click_('/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div/div/div/ul/li[3]',
        #                               "点击选择结算方式-翻页", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        # Cs().xpath_click_(
        #         '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td', "选中结算方式",
        #         "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_('//div[@class="ant-modal-body"]/div[1]/button',
                          "点击选择自定义结算方式", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_('//div[@class="ant-modal-body"]/div[2]/div/div[2]/input', "3")
        Cs().is_toast_exist("输入结算期限", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        #
        Cs().xpath_click_('//div[@class="ant-modal-body"]/button', "确认自定义结算方式期限",
                          "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().slide_("450")
        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[3]/div[2]/div[1]/div/span/div/input', "点击协议签订日期",
                          "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_('//tbody[@class="ant-calendar-tbody"]/tr[1]/td[1]/div', "选中协议签订日期",
                          "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)

        Cs().xpath_send_(xpath_front + '/div/div/div[2]/div[3]/div[2]/div[2]/div/input', "xybh")
        Cs().is_toast_exist("填写协议编号", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)

        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[3]/div[2]/div[3]/div/input', "选择交货方式",
                          "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        driver.find_element_by_xpath(
            u"(.//*[normalize-space(text()) and normalize-space(.)='交货方式名称'])[1]/following::td[1]").click()
        print("选中交货方式")
        # Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[3]/div[2]/div[4]/div/input',
        #                   "选择付款方式", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        # driver.find_element_by_xpath(
        #     u"(.//*[normalize-space(text()) and normalize-space(.)='乙方付款方式名称'])[1]/following::td[1]").click()
        # print("乙方付款方式名称")

        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[3]/div[2]/div[4]/div/input',
                        "选择付款方式", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        driver.find_element(By.CSS_SELECTOR,
                            ".ant-table-wrapper:nth-child(1) .ant-table-row:nth-child(1) > td:nth-child(1)").click()
        print("乙方付款方式名称")
        Cs().slide_("750")
        Cs().xpath_click_('//i[@class="anticon anticon-plus-circle"]', "点击增加货品", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        number1, number2, price1, price2, amount_1, amount_2, total_Amount = goods_iofo()
        gl.set_value('total_Amount', total_Amount)
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr/td[2]/div/textarea',
            "接线盒盖毛坯")  # 货品名称
        Cs().is_toast_exist("输入货品名称", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr/td[4]/div/div/div[2]/input',
            str(number1))  # 货品数量
        Cs().is_toast_exist("输入货品数量", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr/td[5]/div/textarea',
            "件")  # 货品单位
        Cs().is_toast_exist("输入货品单位", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr/td[6]/div/div/div[2]/input',
            str(price1))  # 货品价格
        Cs().is_toast_exist("输入货品价格", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        # Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[4]/button[2]', "点击确定", "发起合同", "云平台‘发起方’",
        #                               sys._getframe().f_lineno)
        time.sleep(1)
        price_1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr/td[7]')
        self.check_information_if(str(amount_1), price_1, "一类商品总价", "发起合同")

        price_sum = Cs().xpath_text_('//*[@id="RightRouteDiv"]/div/div/div/div[2]/div/div/div[2]/div[4]/div/div[2]')
        self.check_information_if("总计:￥%s" % amount_1, price_sum, "所有商品总价", "发起合同")

        price_sum_check_all_1 = re_int1(price_sum)
        price_single_1 = re_int1(price_1)

        # gl.set_value('purchaser_name', purchaser_name)
        gl.set_value('purchaser_926', purchaser_926)
        # gl.set_value('purchaser_email', purchaser_email)
        # gl.set_value('purchaser_phone', purchaser_phone)
        gl.set_value('agent_name', agent_name)
        gl.set_value('agent_926', agent_926)
        gl.set_value('agent_email', agent_email)
        gl.set_value('agent_phone', agent_phone)
        gl.set_value('supplier_926', supplier_926)
        # gl.set_value('supplier_email', supplier_email)
        # gl.set_value('supplier_name', supplier_name)
        # gl.set_value('supplier_phone', supplier_phone)
        gl.set_value('price_single_1', price_single_1)
        gl.set_value('price_sum_check_all_1', price_sum_check_all_1)

        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[5]/button[2]', "点击确定", "发起合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]',
                          "再次确定", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)

    def contract_initiated(self):  # 发起合同后编辑合同申请申请
        driver = self.driver
        start_url = self.start_url

        print("*****编辑合同申请*****")
        # Cs().slide_("0")

        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "进入合同签审", "查看发起后的合同信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                          "进入我方待审签", "查看发起后的合同信息", "云平台‘发起方’", sys._getframe().f_lineno)
        # time.sleep(1)
        # # todo 创建编号 用于校验编号信息
        apply_number = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_re("CR", apply_number, '合同创建编号', "查看发起后的合同信息")
        gl.set_value('apply_number', apply_number)
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        number1, number2, price1, price2, amount_1, amount_2, total_Amount = goods_iofo()
        self.list_contents_seven(driver, '查看发起后的合同信息', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点",
                                 purchaser_name, '深圳926', supplier_name,
                                 '￥%s' % amount_1, '销售方待审签')
        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                        '/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
                          "查看发起后的合同信息", "云平台‘发起方’", sys._getframe().f_lineno)

        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "查看发起后的合同信息", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方审签", "采购方审签", "受托方审签", "查看发起后的合同信息",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看发起后的合同信息")

        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看发起后的合同信息", "云平台‘发起方’", sys._getframe().f_lineno)

        self.Operation_record(driver, "发起方创建合同申请", "%s 18216482019_s" % supplier_name, "查看发起后的合同信息",
                              "发起合同后的操作状态", "发起合同后的操作时间", "发起合同后的操作者信息", "4")

        print('------------点击编辑已发起的委托-------------')
        time.sleep(1)
        Cs().xpath_keys_S(xpath_front + '/div/div/div[2]/button[1]', "点击编辑已发起的委托", "查看发起后的合同信息",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_clear_(xpath_front + '/div/div/div[2]/div[2]/div[2]/div[2]/div/input')  # 清空原始合同编号
        Cs().slide_("300")
        Cs().xpath_send_(xpath_front + '/div/div/div[2]/div[2]/div[2]/div[2]/div/input',
                         "62284844935")  # 输入原始合同编号

        Cs().is_toast_exist("再次编辑输入原始合同编号", "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().slide_('450')
        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[3]/div[2]/div[4]/div/input',
                          "选择付款方式", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        driver.find_element(By.CSS_SELECTOR,
                            ".ant-table-wrapper:nth-child(1) .ant-table-row:nth-child(1) > td:nth-child(1)").click()
        print("乙方付款方式名称")
        Cs().slide_("750")
        Cs().xpath_click_('//i[@class="anticon anticon-plus-circle"]', "再次新增货品", "点击编辑已发起的委托",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        number1, number2, price1, price2, amount_1, amount_2, total_Amount = goods_iofo()
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr[2]/td[2]/div/textarea',
            "接线盒盖")  # 货品名称
        Cs().is_toast_exist("输入货品名称", "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr[2]/td[3]/div/textarea',
            "TF")  # 货品名称
        Cs().is_toast_exist("输入货品型号", "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr[2]/td[4]/div/div/div[2]/input',
            str(number2))  # 货品数量
        Cs().is_toast_exist("输入货品数量", "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr[2]/td[5]/div/textarea',
            "件")  # 货品单位
        Cs().is_toast_exist("输入货品单位", "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr[2]/td[6]/div/div/div[2]/input',
            str(price2))  # 货品价格
        Cs().is_toast_exist("输入货品价格", "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)

        price_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[4]/div/div[1]/div/div/div/div/div/table/tbody/tr[2]/td[7]')
        self.check_information_if(str(amount_2), price_2, "新增商品总价", "点击编辑已发起的委托")

        price_sum = Cs().xpath_text_('//*[@id="RightRouteDiv"]/div/div/div/div[2]/div/div/div[2]/div[4]/div/div[2]')
        self.check_information_if("总计:￥%s" % total_Amount, price_sum, "所有商品总价格", "点击编辑已发起的委托")
        # global price_sum_check_all_2, price_many_2
        gl.set_value('number1', number1)
        gl.set_value('number2', number2)
        gl.set_value('price1', price1)
        gl.set_value('price2', price2)
        gl.set_value('amount_1', amount_1)
        gl.set_value('amount_2', amount_2)

        price_many_2 = re_int1(price_2)
        price_sum_check_all_2 = re_int1(price_sum)
        gl.set_value('price_many_2', price_many_2)
        gl.set_value('price_sum_check_all_2', price_sum_check_all_2)
        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[5]/button', "点击确认修改", "点击编辑已发起的委托",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(
            '//div[@class="ant-modal-confirm-btns"]/button[2]', "再次点击确认",
            "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        # 编辑完毕
        print("*****查看校验我方编辑之后合同申请*****")
        # Cs().slide_("0")
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div'
                                        '/div/div[1]/div[2]', "进入我方待审签", "查看编辑后的合同信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
            "查看编辑后的合同信息", "云平台‘发起方’", sys._getframe().f_lineno)

        time.sleep(2.5)  # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "查看发起后的合同信息", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方审签", "采购方审签", "受托方审签", "查看发起后的合同信息",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看我方编辑后的合同信息")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看编辑后的合同信息", "云平台‘发起方’", sys._getframe().f_lineno)

        self.Operation_record(driver, "发起方修改合同申请", "二天河软件企业注册名字 18216482019_s", "查看编辑后的合同信息",
                              "编辑合同后的操作状态", "编辑合同后的操作时间", "编辑合同后的操作者信息", "4")
        time.sleep(1)
        # 签审合同
        Cs().xpath_click_(
            xpath_front + '/div/div/div[2]/button[2]', "点击确认审签", "签审合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        # Cs().xpath_click_('/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div/label', "点击已阅读合同", "签审合同",
        #                               "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_keys_S('//div[@class="ant-modal-body"]/div/label', "点击已阅读合同", "签审合同",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_keys_S('//div[@class="ant-modal-body"]/div/button', "再次确认审签", "签审合同",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_send_('//div[@class="ant-col ant-col-17"]/input', "48152")
        Cs().is_toast_exist("输入验证码", "签审合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_keys_S('//div[@class="ant-modal-footer"]/button[2]', "点击确定",
                          "签审合同", "云平台‘发起方’", sys._getframe().f_lineno)

        time.sleep(1)
        print("*****查看校验待采购方审批的合同申请*****")
        # Cs().slide_("0")

        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "进入合同签审", "查看校验待采购方审批的合同申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]',
                          "进入合作方待审签", "查看校验待采购方审批的合同申请", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        apply_number = gl.get_value('apply_number')
        apply_number_3 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_re(apply_number, apply_number_3, "‘合作方待审批’创建编号", "查看校验待采购方审批的合同申请")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        self.list_contents_seven(driver, '查看校验待采购方审批的合同申请', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点",
                                 purchaser_name, agent_name, supplier_name,
                                 str(total_Amount), '采购方待审签')

        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                        '/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
                          "查看校验待采购方审批的合同申请", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "查看校验待采购方审批的合同申请", "合同详情一级目录", "合同详情二级目录",
                           "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方审签", "受托方审签", "查看校验待采购方审批的合同申请",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看校验待采购方审批的合同申请")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看校验待采购方审批的合同申请", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        self.Operation_record(driver, "发起方提交合同申请", "二天河软件企业注册名字 18216482019_s", "查看校验待采购方审批的合同申请",
                              "查看我方签审后的操作状态", "查看我方签审后的操作时间", "查看我方签审后的操作者信息", "4")

    def refuse_entrust(self):  # 修改被合作方拒绝的委托
        driver = self.driver
        start_url = self.start_url

        print("*****查看被合作方拒绝的委托信息*****")

        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="0$Menu"]/li[2]', "进入合同处理", "查看被合作方拒绝的委托信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        # 校验目录
        self.catalog_two(driver, "合同管理", "合同处理列表", "查看被合作方拒绝的委托信息", "合同详情一级目录", "合同详情二级目录")
        # self.navigation_three(driver, "销售方已审签", "采购方审签", "受托方审签", "查看被（合作方）拒绝后重新发起的合同信息",
        #                       "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                          "进入我方待处理", "查看被合作方拒绝的委托信息", "云平台‘发起方’", sys._getframe().f_lineno)
        apply_number = gl.get_value('apply_number')
        apply_number_2 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘我方待审批’创建编号", "查看被合作方拒绝的委托信息")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        total_Amount = gl.get_value('total_Amount')
        self.list_contents_eight(driver, '查看被合作方拒绝的委托信息', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点", '合同类别',
                                 purchaser_name, agent_name, supplier_name,
                                 '￥%s' % total_Amount, '采购方拒绝', '代理销售')
        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                        '/div/div/table/tbody/tr[1]/td[9]/div/a/button', "点击查看",
                          "查看被合作方拒绝的委托信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同处理", "合同详情", "查看被合作方拒绝的委托信息", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方拒绝", "受托方审签", "查看被合作方拒绝的委托信息",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")
        # 拒绝理由、拒绝详情
        cooperation_refuse_reason = gl.get_value("cooperation_refuse_reason")
        cooperation_refuse_details = gl.get_value("cooperation_refuse_details")
        cooperation_refuse_reason_ = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div[1]')
        self.check_information_re(cooperation_refuse_reason, cooperation_refuse_reason_, "拒绝理由", "查看被合作方拒绝的委托信息")
        cooperation_refuse_details_ = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div[2]')
        self.check_information_re(cooperation_refuse_details, cooperation_refuse_details_, "拒绝详情", "查看被合作方拒绝的委托信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看被合作方拒绝的委托信息")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看被合作方拒绝的委托信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        self.Operation_record_refuse(driver, "合作方拒绝合同申请", "一广州新东方企业注册名字 18390552449_s", "查看被合作方拒绝的委托信息",
                                     "查看被合作方拒绝后的操作状态", "查看被合作方拒绝后的操作时间", "查看被合作方拒绝后的操作者信息",
                                     "查看被合作方拒绝后的理由", "查看被合作方拒绝后的详情")
        print("*****修改被合作方拒绝的委托*****")
        Cs().xpath_keys_S(xpath_front + '/div/div/div[2]/button', "点击修改委托", "修改被合作方拒绝合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[2]/div[2]/div[3]/div/input', "点击选择结算方式",
                          "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        # Cs().xpath_click_('/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div/div/div/ul/li[3]',
        #                               "点击选择结算方式-翻页", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        # Cs().xpath_click_(
        #         '/html/body/div[3]/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td', "选中结算方式",
        #         "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_('//div[@class="ant-modal-body"]/div[1]/button',
                          "点击选择自定义结算方式", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_send_('//div[@class="ant-modal-body"]/div[2]/div/div[2]/input', "2")
        Cs().is_toast_exist("输入结算期限", "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        #
        Cs().xpath_click_('//div[@class="ant-modal-body"]/button', "确认自定义结算方式期限",
                          "发起合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().slide_("500")
        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[5]/button', "点击确认修改", "点击编辑已发起的委托",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(
            '//div[@class="ant-modal-confirm-btns"]/button[2]', "再次点击确认",
            "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        time.sleep(1)
        print("*****查看被合作方拒绝后重新修改的委托*****")
        # Cs().slide_("0")

        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "进入合同签审", "查看被合作方拒绝后重新修改的委托", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                          "进入我方待审签", "查看被合作方拒绝后重新修改的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)

        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                        '/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
                          "查看被合作方拒绝后重新修改的委托", "云平台‘发起方’", sys._getframe().f_lineno)

        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "查看被合作方拒绝后重新修改的委托", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方审签", "采购方审签", "受托方审签", "查看被合作方拒绝后重新修改的委托",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看被合作方拒绝后重新修改的委托")

        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看被合作方拒绝后重新修改的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        self.Operation_record(driver, "发起方修改合同申请", "二天河软件企业注册名字 18216482019_s", "查看被合作方拒绝后重新修改的委托",
                              "发起合同后的操作状态", "发起合同后的操作时间", "发起合同后的操作者信息", "4")
        print("***********审批被合作方拒绝合同***************")
        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "进入已发起委托", "审批被合作方拒绝合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        Cs().xpath_click_(xpath_front + '/div/div[1]'
                                        '/div/div[1]/div/div/div/div/div[1]/div[2]', "进入我方待审签",
                          "审批被合作方拒绝合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]'
                                        '/div/div/div/div/div/table/tbody/tr[1]/td[8]/div/a/button',
                          "点击查看", "审批被合作方拒绝合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        Cs().xpath_keys_S(xpath_front + '/div/div/div[2]/button[2]', "点击确认审批", "审批被合作方拒绝合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_keys_S("//input[@class='ant-checkbox-input']", "合同已阅读", "审批被合作方拒绝合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_keys_S('//div[@class="ant-modal-body"]/div/button', "确认审签",
                          "审批被代理方拒绝合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_send_('//div[@class="ant-col ant-col-17"]/input', "48152", "输入验证码", "签审合同",
                         "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_keys_S('//div[@class="ant-modal-footer"]/button[2]', "点击确定",
                          "签审合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # Cs().slide_("0")
        print("***********查看被合作方拒绝后我方再次签审合同信息***************")
        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "进入合同签审", "查看被合作方拒绝后我方再次签审合同信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)

        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]',
                          "进入合作方待审签", "查看被合作方拒绝后我方再次签审合同信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)

        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                        '/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
                          "查看被合作方拒绝后我方再次签审合同信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "查看被合作方拒绝后我方再次签审合同信息", "合同详情一级目录", "合同详情二级目录",
                           "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方审签", "受托方审签", "查看被合作方拒绝后我方再次签审合同信息",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看被合作方拒绝后我方再次签审合同信息")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看被合作方拒绝后我方再次签审合同信息", "云平台‘发起方’", sys._getframe().f_lineno)
        self.Operation_record(driver, "发起方提交合同申请", "二天河软件企业注册名字 18216482019_s", "查看被合作方拒绝后我方再次签审合同信息",
                              "查看我方签审后的操作状态", "查看我方签审后的操作时间", "查看我方签审后的操作者信息", "4")
        time.sleep(1)

    def refuse_entrust_1(self):  # 修改被代理方拒绝的委托
        driver = self.driver
        start_url = self.start_url
        print("*****查看被代理方拒绝的委托信息*****")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="0$Menu"]/li[2]', "进入合同处理", "查看被代理方拒绝的委托信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        # 校验目录
        self.catalog_two(driver, "合同管理", "合同处理列表", "查看被代理方拒绝的委托信息", "合同详情一级目录", "合同详情二级目录")

        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                          "进入我方待处理", "查看被代理方拒绝的委托信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        apply_number = gl.get_value('apply_number')
        apply_number_2 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘我方待审批’创建编号", "查看被代理方拒绝的委托信息")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        total_Amount = gl.get_value('total_Amount')
        self.list_contents_eight(driver, '查看被代理方拒绝的委托信息', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点", '合同类别',
                                 purchaser_name, agent_name, supplier_name,
                                 '￥%s' % total_Amount, '受托方拒绝', '代理销售')
        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                        '/div/div/table/tbody/tr[1]/td[9]/div/a/button', "点击查看",
                          "查看被代理方拒绝的委托信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)

        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同处理", "合同详情", "查看被代理方拒绝的委托信息", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方已审签", "受托方拒绝", "查看被代理方拒绝的委托信息",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")
        # 拒绝理由、拒绝详情
        agent_refuse_reason = gl.get_value("agent_refuse_reason")
        agent_refuse_details = gl.get_value("agent_refuse_details")
        agent_refuse_reason_ = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div[1]')
        self.check_information_re(agent_refuse_reason, agent_refuse_reason_, "拒绝理由", "查看被代理方拒绝的委托信息")
        agent_refuse_details_ = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div[2]')
        self.check_information_re(agent_refuse_details, agent_refuse_details_, "拒绝详情", "查看被代理方拒绝的委托信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看被代理方拒绝的委托信息")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看被代理方拒绝的委托信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)

        self.Operation_record_refuse(driver, "代理商拒绝合同申请", "深圳926 18772606900_s", "查看被代理方拒绝的委托信息",
                                     "查看被代理方拒绝后的操作状态", "查看被代理方拒绝后的操作时间", "查看被代理方拒绝后的操作者信息",
                                     "查看被代理方拒绝后的理由", "查看被代理方拒绝后的详情")
        print("*****修改被代理方拒绝的委托*****")
        Cs().xpath_keys_S(xpath_front + '/div/div/div[2]/button', "点击修改委托", "修改被代理方拒绝的委托", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().slide_("400")
        Cs().xpath_click_(xpath_front + '/div/div/div[2]/div[5]/button', "点击确认修改", "点击编辑已发起的委托",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(
            '//div[@class="ant-modal-confirm-btns"]/button[2]', "再次点击确认",
            "点击编辑已发起的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        time.sleep(1)
        print("*****查看被代理方拒绝后重新修改的委托*****")
        # Cs().slide_("0")

        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "进入合同签审", "查看被代理方拒绝后重新修改的委托", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                          "进入我方待审签", "查看被代理方拒绝后重新修改的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)

        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                        '/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
                          "查看被代理方拒绝后重新修改的委托", "云平台‘发起方’", sys._getframe().f_lineno)

        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "查看被代理方拒绝后重新修改的委托", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方审签", "采购方审签", "受托方审签", "查看被代理方拒绝后重新修改的委托",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看被代理方拒绝后重新修改的委托")

        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看被代理方拒绝后重新修改的委托", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        self.Operation_record(driver, "发起方修改合同申请", "二天河软件企业注册名字 18216482019_s", "查看被代理方拒绝后重新修改的委托",
                              "发起合同后的操作状态", "发起合同后的操作时间", "发起合同后的操作者信息", "4")
        print("***********审批被代理方拒绝合同***************")
        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "进入已发起委托", "审批被代理方拒绝合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        Cs().xpath_click_(xpath_front + '/div/div[1]'
                                        '/div/div[1]/div/div/div/div/div[1]/div[2]', "进入我方待审签",
                          "审批被代理方拒绝合同", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]'
                                        '/div/div/div/div/div/table/tbody/tr[1]/td[8]/div/a/button',
                          "点击查看", "审批被代理方拒绝合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        Cs().xpath_keys_S(xpath_front + '/div/div/div[2]/button[2]', "点击确认审批", "审批被代理方拒绝合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_keys_S("//input[@class='ant-checkbox-input']", "合同已阅读", "审批被代理方拒绝合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_keys_S('//div[@class="ant-modal-body"]/div/button', "确认审签",
                          "审批被代理方拒绝合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_send_('//div[@class="ant-col ant-col-17"]/input', "48152", "输入验证码", "签审合同",
                         "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_keys_S('//div[@class="ant-modal-footer"]/button[2]', "点击确定",
                          "签审合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # Cs().slide_("0")
        print("***********查看被代理方拒绝后我方再次签审合同信息***************")
        Cs().xpath_click_('//*[@id="0$Menu"]/li[1]', "进入合同签审", "查看被代理方拒绝后我方再次签审合同信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]',
                          "进入合作方待审签", "查看被代理方拒绝后我方再次签审合同信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)

        Cs().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                        '/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
                          "查看被代理方拒绝后我方再次签审合同信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "查看被代理方拒绝后我方再次签审合同信息", "合同详情一级目录", "合同详情二级目录",
                           "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方审签", "受托方审签", "查看被代理方拒绝后我方再次签审合同信息",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看被代理方拒绝后我方再次签审合同信息")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                          "点击操作记录", "查看被代理方拒绝后我方再次签审合同信息", "云平台‘发起方’", sys._getframe().f_lineno)
        self.Operation_record(driver, "发起方提交合同申请", "二天河软件企业注册名字 18216482019_s", "查看被代理方拒绝后我方再次签审合同信息",
                              "查看我方签审后的操作状态", "查看我方签审后的操作时间", "查看我方签审后的操作者信息", "4")

    def see_cooperation_adopt(self):
        print("*****校验代理方通过审批后的合同信息****")
        driver = self.driver
        Cs().xpath_click_('//*[@id="0$Menu"]/li[3]', "进入合同签订", "校验代理方通过审批后的合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
        self.catalog_two(driver, "合同管理", "合同签订列表", "校验代理方通过审批后的合同", "合同审签列表页一级目录", "合同审签列表页二级目录")
        self.list_three(driver, "全部", "代理采购", "代理销售", "校验代理方通过审批后的合同", "合同签审-全部列表",
                        "合同签审-我方待审批列表", "合同签审-合作方待审批列表")

        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "进入代理销售",
                          "校验代理方通过审批后的合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        contractnumber_number_3 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(contractnumber, contractnumber_number_3, "校验合同编号是否一致", "校验代理方通过审批后的合同")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        total_Amount = gl.get_value('total_Amount')
        self.list_contents_seven(driver, '校验代理方通过审批后的合同', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点",
                                 purchaser_name, agent_name, supplier_name,
                                 '￥%s' % total_Amount, '受托方已通过')
        Cs().xpath_click_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
            "校验代理方通过审批后的合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同签订", "合同详情", "校验代理方通过审批后的合同", "合同详情一级目录", "合同详情二级目录",
                           "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方已审签", "受托方已审签", "校验代理方通过审批后的合同",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "校验代理方通过审批后的合同")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]', "点击操作记录",
                          "校验代理方通过审批后的合同", "云平台‘发起方’", sys._getframe().f_lineno)

        self.Operation_record(driver, "代理商已审签", "深圳926 18772606900_s", "校验代理方通过审批后的合同",
                              "查看代理方签审后的操作状态", "查看代理方签审后的操作时间", "查看代理方签审后的操作者信息", "4")

    def Delivery_application(self):  # 代销方申请发货
        driver = self.driver
        print("*****代销方申请发货*****")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击发货申请", "发起发货申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        # 校验目录信息
        self.catalog_two(driver, "代销管理", "发货申请", "发起发货申请", "发货申请列表页一级目录", "发货申请列表页二级目录")
        self.list_six(driver, "所有发货单", "客户待审批", "代理方待审批", "代理方已通过", "客户未通过", "代理方未通过", "发起发货申请", "代销管理-所有发货单列表",
                      "代销管理-客户待审批列表", "代销管理-代理方待审批列表", "代销管理-代理方已通过列表", "代销管理-客户未通过列表", "代销管理-代理方未通过列表")
        time.sleep(1)
        Cs().xpath_keys_S(xpath_front + '/div/div[3]/button', "点击申请发货", "发起发货申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        self.catalog_three(driver, "代销管理", "发货申请", "新增发货单", "发起发货申请", "发货申请列表页一级目录",
                           "发货申请列表页二级目录", "发货申请列表页三级目录")
        Cs().xpath_click_(xpath_front + '/div/div/div[1]/div[2]/div/div/div[2]/button', "选择收货单位", "发起发货申请",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_click_('//tbody[@class="ant-table-tbody"]/tr/td', "选中收货单位", "发起发货申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div/div[1]/div[2]/div/div/div[4]/button', "选择委托合同", "发起发货申请",
                          "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(3)
        Cs().xpath_click_('//tbody[@class="ant-table-tbody"]/tr[1]', "选中委托合同", "发起发货申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(2.5)
        contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
        contractnumber_1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div/div/div[4]/button/span')
        # print(contractnumber, "_1wei : %s" % contractnumber_1)
        self.check_information_if(contractnumber, contractnumber_1, '合同编号是否一致', "发起发货申请")
        number1, number2, price1, price2, amount_1, amount_2, total_Amount = goods_iofo()
        Cs().xpath_clear_(
            xpath_front + '/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/table/tbody/tr[1]/'
                          'td[4]/div/div[2]/input')
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/table/tbody/tr[1]/'
                          'td[4]/div/div[2]/input', number1)
        Cs().is_toast_exist("输入发货数量1", "发起发货申请", "云平台‘发起方’", sys._getframe().f_lineno)
        Cs().xpath_clear_(
            xpath_front + '/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/table/tbody/tr[2]/'
                          'td[4]/div/div[2]/input')
        Cs().xpath_send_(
            xpath_front + '/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/table/tbody/tr[2]/'
                          'td[4]/div/div[2]/input', number2)
        Cs().is_toast_exist("输入发货数量2", "发起发货申请", "云平台‘发起方’", sys._getframe().f_lineno)
        price_sum_check_all_2 = gl.get_value('price_sum_check_all_2')  # 两种商品总价
        price_sum_check_all_2 = re_int1(price_sum_check_all_2)
        # print(price_sum_check_all_2)
        total_Amount1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p[2]/span')
        total_1goods = re_int1(total_Amount1)
        total_Amount = gl.get_value('total_Amount')
        self.check_information_re(str(total_Amount), total_1goods, '货品总价', "发起发货申请")
        gl.set_value('total_Amount', total_1goods)  # 货品总价
        balance = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p[1]')
        # estimateReduceQuota_1 = re_sub_(estimateReduceQuota_1)  # 显示为12,500.00 正则筛选
        contract_surplus = int(price_sum_check_all_2) - int(total_Amount)
        self.check_information_re(str(contract_surplus), balance, '合同余额', "发起发货申请")
        Cs().xpath_send_(
            xpath_front + '/div/div/div[3]/div[2]/div[1]/div/div[2]/div/div[2]/input', "40")
        Cs().is_toast_exist("输入服务费比例", "发起发货申请", "云平台‘发起方’", sys._getframe().f_lineno)

        Cs().xpath_keys_S(xpath_front + '/div/div/div[4]/button', "点击确定", "发起发货申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(2.5)
        print("*********查看发货单信息***********")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击发货管理", "查看发货单信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击客户待审批",
                          "查看发货单信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)

        invoiceApplySn = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re('DF', invoiceApplySn, "查看发货单信息", "发起发货申请")
        gl.set_value('invoiceApplySn', invoiceApplySn)
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        receiving_party_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中收货单位", "发起发货申请")

        agent_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "发起发货申请")
        total_Amount = gl.get_value('total_Amount')
        contract_sum = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        self.check_information_if('￥%s.00' % total_Amount, contract_sum, "列表中发货金额", "发起发货申请")
        state_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('客户待审批', state_1, "查看发货单信息", "发起发货申请")

        Cs().xpath_click_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击查看", "查看发货单信息",
            "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "发货申请", "发货单详情", "查看发货单信息", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 发起申请', '采购方 待审批', "代理方 待审核", "查看发货单信息",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名

        supplierName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplierName_1, "获取详情页中发货方名称", "查看发货单信息")
        supplier_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(supplier_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaserName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_1, "获取详情页中收货方名称", "查看发货单信息")
        purchaser_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        supplier_address = gl.get_value('supplier_address')  # 销售方（丙）方地址

        supplierAdress = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress, "发货地址-详情页", "查看发货单信息")

        purchaserAdress = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress, "收货地址：详情页", "查看发货单信息")

        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)方电话
        supplierPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplierPhone, "获取详情页中发货方号码", "查看发货单信息")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中收货方号码", "查看发货单信息")

        forwarding_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "查看发货单信息")
        #
        receiving_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "查看发货单信息")
        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p/span')

        self.check_information_if("¥%s" % total_Amount, price_sum, "获取详情页中商品总价", "查看发货单信息")
        price_sum = re_int1(price_sum)

        Cs().slide_("580")
        time.sleep(0.5)

        our_service_charge = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        our_service_charge_check = str(service_coefficient(price_sum, forwarding_proportion))
        self.check_information_if(our_service_charge_check, our_service_charge, "获取详情页中我方服务费金额", "查看发货单信息")
        gl.set_value('our_service_charge', our_service_charge)  # 我方服务费
        their_service_charge = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        their_service_charge_check = str(service_coefficient(price_sum, receiving_proportion))
        # their_service_charge_check = str(their_service_charge_check)
        self.check_information_if(their_service_charge_check, their_service_charge, "详情页中他方服务费金额", "查看发货单信息")
        gl.set_value('their_service_charge', their_service_charge)  # 他方服务费

        submission_time = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[4]/div[2]/div[4]/div[2]')
        self.check_information_time(submission_time, "详情页中提交时间", "查看发货单信息")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看发货单信息")

        invoiceApplySn_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[1]/div[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "详情页中发货单号", "查看发货单信息")
        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[3]/div[2]/a')
        self.check_information_re(contractnumber, Contract_number_2, "详情页中合同编号", "查看发货单信息")

        record_state = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                        '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("供应商已提交", record_state, "发起合同后的操作状态", "查看发货单信息")

        record_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time, "发起合同后的操作时间", "查看发货单信息")

        record_operator = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                           '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')

        self.check_information_re("15183834489_s", record_operator, "获取发起合同后的操作者信息", "查看发货单信息")
        Cs().is_toast_exist("获取发起申请后的操作者信息", "查看发货单信息", "云平台‘发起方’", sys._getframe().f_lineno)

        print("*****获取发货申请未三方通过前的云票额度*****")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入额度管理首页", "获取发货申请未三方通过前的云票额度", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        totalCreditQuota_supplier = gl.get_value('totalCreditQuota_supplier')  # 丙 销售总授信云票"
        totalCirculationQuota_supplier = gl.get_value('totalCirculationQuota_supplier')  # 丙 销售总流转云票"
        # totalQuota_supplier = gl.get_value('totalQuota_supplier')  # 甲 总云票 （授信+流转）
        totalOccupyCreditQuota_supplier = gl.get_value('totalOccupyCreditQuota_supplier')  # 丙 销售 已占用授信云票
        totalOccupyCirculationQuota_supplier = gl.get_value('totalOccupyCirculationQuota_supplier')  # 丙 销售 已占用流转云票
        # totalFrozenCreditQuota_supplier = gl.get_value('totalFrozenCreditQuota_supplier')  # 丙 销售 获取已冻结授信云票
        # totalFrozenCirculationQuota_supplier = gl.get_value('totalFrozenCirculationQuota_supplier')  # 丙 销售 已冻结流转云票
        totalOccupancyCreditQuota_supplier = gl.get_value('totalOccupancyCreditQuota_supplier')  # 丙 销售 可用总授信(总-已用)
        totalOccupancyCirculationQuota_supplier = gl.get_value(
            'totalOccupancyCirculationQuota_supplier')  # 丙 销售 余总流转(总-已用

        estimateReduceQuota_supplier = Cs().xpath_text_(xpath_front + '/div/div[3]/div/div[2]/div[2]')
        Cs().is_toast_exist("获取预计减少云票", "获取发货申请未三方通过前的云票额度", "云平台‘发起方’", sys._getframe().f_lineno)
        surplusAvailableTotalCreditQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupancyCreditQuota_supplier, surplusAvailableTotalCreditQuota_1, "可用授信",
                                  "获取发货申请未三方通过前的云票额度")
        occupyTotalCreditQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[1]/p[2]')
        self.check_information_re(totalOccupyCreditQuota_supplier, occupyTotalCreditQuota_1, "已用授信",
                                  "获取发货申请未三方通过前的云票额度")
        totalCreditQuota_1 = Cs().xpath_text_(xpath_front + '/div/div[2]/div/div[1]/div[3]')
        self.check_information_re(totalCreditQuota_supplier, totalCreditQuota_1, "总授信", "获取发货申请未三方通过前的云票额度")

        estimateAddQuota_supplier = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div[1]/div[2]')  # 预增云票
        Cs().is_toast_exist("获取预增云票", "获取发货申请未三方通过前的云票额度", "云平台‘发起方’", sys._getframe().f_lineno)

        totalCirculationQuota_1 = Cs().xpath_text_(xpath_front + '/div/div[2]/div/div[2]/div[3]')
        totalCirculationQuota_1 = re_sub_(totalCirculationQuota_1)
        self.check_information_re(totalCirculationQuota_supplier, totalCirculationQuota_1, "总流转", "获取发货申请未三方通过前的云票额度")

        surplusTotalCirculationQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[4]')
        surplusTotalCirculationQuota_1 = re_sub_(surplusTotalCirculationQuota_1)
        self.check_information_re(totalOccupancyCirculationQuota_supplier, surplusTotalCirculationQuota_1,
                                  "剩余流转", "获取发货申请未三方通过前的云票额度")
        surplusAvailableTotalCirculationQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        surplusAvailableTotalCirculationQuota_check = int(surplusTotalCirculationQuota_1) * 0.8
        self.check_information_re(str(surplusAvailableTotalCirculationQuota_check)[0:-2],
                                  surplusAvailableTotalCirculationQuota_1,
                                  "可用流转", "获取发货申请未三方通过前的云票额度")
        occupyAvailableTotalCirculationQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[1]/p[2]')
        self.check_information_re(totalOccupyCirculationQuota_supplier, occupyAvailableTotalCirculationQuota_1,
                                  "已用流转", "获取发货申请未三方通过前的云票额度")
        loanAbilityQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[3]/p[2]')
        totalCirculationQuota_supplier_check = int(totalCirculationQuota_supplier) * 0.5
        self.check_information_re(str(totalCirculationQuota_supplier_check), loanAbilityQuota_1, "可贷现",
                                  "获取发货申请未三方通过前的云票额度")

        gl.set_value("estimateAddQuota_supplier", estimateAddQuota_supplier)  # 预增云票
        gl.set_value("estimateReduceQuota_supplier", estimateReduceQuota_supplier)  # 预计减少云票

    def refuse_application(self):  # 查看被合作方拒绝的申请
        print("*********查看被合作方拒绝的申请***********")
        driver = self.driver
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击发货管理", "查看被合作方拒绝的申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]',
                          "点击hezuo方未通过", "查看被合作方拒绝的申请", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        invoiceApplySn_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看被合作方拒绝的申请", "发起发货申请")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        receiving_party_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中收货单位", "查看被合作方拒绝的申请")

        agent_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "查看被合作方拒绝的申请")

        contract_sum = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00' % total_Amount, contract_sum, "列表中发货金额", "查看被合作方拒绝的申请")
        state_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('客户未通过', state_1, "查看发货单信息", "查看被合作方拒绝的申请")

        Cs().xpath_click_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击查看", "查看被合作方拒绝的申请",
            "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "发货申请", "发货单详情", "查看被合作方拒绝的申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 发起申请', '采购方 未通过', "代理方 待审核", "查看被合作方拒绝的申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        supplierName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplierName_1, "获取详情页中发货方名称", "查看被合作方拒绝的申请")
        supplier_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(supplier_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        purchaserName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_1, "获取详情页中收货方名称", "查看被合作方拒绝的申请")
        purchaser_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        supplier_address = gl.get_value('supplier_address')  # 销售方（丙）方地址

        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货地址-详情页", "查看被合作方拒绝的申请")

        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址：详情页", "查看被合作方拒绝的申请")

        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)方电话
        supplierPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplierPhone, "获取详情页中发货方号码", "查看被合作方拒绝的申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中收货方号码", "查看被合作方拒绝的申请")

        forwarding_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "查看被合作方拒绝的申请")
        #
        receiving_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "查看被合作方拒绝的申请")
        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p/span')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if("¥%s" % total_Amount, price_sum, "获取详情页中商品总价", "查看被合作方拒绝的申请")
        price_sum = re_int1(price_sum)
        Cs().slide_("580")
        time.sleep(0.5)
        our_service_charge = gl.get_value('our_service_charge')
        our_service_charge_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "查看被合作方通过的申请")

        their_service_charge = gl.get_value('their_service_charge')
        their_service_charge_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        self.check_information_if(their_service_charge, their_service_charge_1, "详情页中他方服务费金额", "查看被合作方通过的申请")

        submission_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[4]/div[2]')
        self.check_information_time(submission_time, "详情页中提交时间", "查看被合作方拒绝的申请")

        customer_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[5]/div[2]')
        self.check_information_time(customer_time, "详情页中客户拒绝时间", "查看被合作方通过的申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看被合作方拒绝的申请")

        invoiceApplySn_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[1]/div[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "详情页中发货单号", "查看被合作方拒绝的申请")
        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[3]/div[2]/a')
        self.check_information_re(contractnumber, Contract_number_2, "详情页中合同编号", "查看被合作方拒绝的申请")
        Cs().slide_("700")
        record_state = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                        '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("采购商拒绝", record_state, "发起合同后的操作状态", "查看被合作方拒绝的申请")

        record_operator = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                           '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
        self.check_information_re("18474793371", record_operator, "获取发起合同后的操作者信息", "查看被合作方拒绝的申请")

        failureTag = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_re("其他 金额部分", failureTag, "拒绝后发货申请后的拒绝标签", "查看被合作方拒绝的申请")

        remark = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[4]')
        self.check_information_re("fkl", remark, "拒绝后发货申请后的拒绝理由", "查看被合作方拒绝的申请")

        record_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[5]')
        self.check_information_time(record_time, "发起合同后的操作时间", "查看被合作方拒绝的申请")

    def adopt_application_1(self):  # 查看被合作方通过的申请
        print("*********查看被合作方通过的申请***********")
        driver = self.driver
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击发货管理", "查看被合作方通过的申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击代理方待审批",
                          "查看被合作方通过的申请", "云平台‘发起方’", sys._getframe().f_lineno)

        invoiceApplySn = gl.get_value('invoiceApplySn')
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        invoiceApplySn_2 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_2, "列表中申请单号", "查看被合作方通过的申请")

        receiving_party_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中收货单位", "查看被合作方拒绝的申请")

        agent_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "查看被合作方拒绝的申请")

        contract_sum = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00' % total_Amount, contract_sum, "列表中发货金额", "查看被合作方拒绝的申请")
        state_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('代理方待审批', state_1, "查看发货单信息", "查看被合作方拒绝的申请")

        Cs().xpath_click_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击查看", "查看被合作方通过的申请",
            "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "发货申请", "发货单详情", "查看被合作方通过的申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 已审批', '采购方 已同意', "代理方 待审核", "查看被合作方通过的申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        supplierName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplierName_1, "获取详情页中发货方名称", "查看被合作方通过的申请")
        supplier_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(supplier_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaserName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_1, "获取详情页中收货方名称", "查看被合作方通过的申请")

        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        supplier_address = gl.get_value('supplier_address')  # 销售方（丙）方地址
        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货地址-详情页", "查看被合作方通过的申请")

        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址：详情页", "查看被合作方通过的申请")

        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)方电话
        supplierPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplierPhone, "获取详情页中发货方号码", "查看被合作方通过的申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中收货方号码", "查看被合作方通过的申请")

        forwarding_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "查看被合作方通过的申请")
        #
        receiving_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "查看被合作方通过的申请")
        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p/span')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if("¥%s" % total_Amount, price_sum, "获取详情页中商品总价", "查看被合作方通过的申请")
        our_service_charge = gl.get_value('our_service_charge')
        Cs().slide_("580")
        time.sleep(0.5)
        our_service_charge_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "查看被合作方通过的申请")

        their_service_charge = gl.get_value('their_service_charge')
        their_service_charge_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        self.check_information_if(their_service_charge, their_service_charge_1, "详情页中他方服务费金额", "查看被合作方通过的申请")

        submission_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[4]/div[2]')
        self.check_information_time(submission_time, "详情页中提交时间", "查看被合作方通过的申请")

        customer_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[5]/div[2]')
        self.check_information_time(customer_time, "详情页中客户提交时间", "查看被合作方通过的申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看被合作方通过的申请")

        invoiceApplySn_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[1]/div[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "详情页中发货单号", "查看被合作方通过的申请")
        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[3]/div[2]/a')
        self.check_information_re(contractnumber, Contract_number_2, "详情页中合同编号", "查看被合作方通过的申请")
        Cs().slide_("700")
        record_state = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                        '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("采购商已同意", record_state, "发起合同后的操作状态", "查看被合作方通过的申请")

        record_operator = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                           '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
        self.check_information_re("18474793371", record_operator, "获取发起合同后的操作者信息", "查看被合作方通过的申请")

        record_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time, "发起合同后的操作时间", "查看被合作方通过的申请")

    def refuse_application_1(self):  # 查看被代理方拒绝的合同
        print("*********查看被代理方拒绝的合同***********")
        driver = self.driver
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击发货申请", "查看被代理方拒绝的合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[6]', "点击代理方未通过",
                          "查看被代理方拒绝的合同", "云平台‘发起方’", sys._getframe().f_lineno)

        invoiceApplySn = gl.get_value('invoiceApplySn')
        invoiceApplySn_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看被代理方拒绝的合同", "发起发货申请")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        receiving_party_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中收货单位", "查看被代理方拒绝的合同")

        agent_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "查看被代理方拒绝的合同")

        contract_sum = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')

        self.check_information_if('￥%s.00' % total_Amount, contract_sum, "列表中发货金额", "查看被代理方拒绝的合同")
        state_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('代理方未通过', state_1, "查看发货单信息", "查看被代理方拒绝的合同")

        Cs().xpath_click_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击查看", "查看被代理方拒绝的合同",
            "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "发货申请", "发货单详情", "查看被代理方拒绝的合同", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 已审批', '采购方 已同意', "代理方 未通过", "查看被代理方拒绝的合同",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        supplierName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplierName_1, "获取详情页中发货方名称", "查看被代理方拒绝的合同")
        supplier_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(supplier_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaserName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_1, "获取详情页中收货方名称", "查看被代理方拒绝的合同")
        purchaser_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        supplier_address = gl.get_value('supplier_address')  # 销售方（丙）方地址
        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货地址-详情页", "查看被代理方拒绝的合同")

        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址：详情页", "查看被代理方拒绝的合同")

        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)方电话
        supplierPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplierPhone, "获取详情页中发货方号码", "查看被代理方拒绝的合同")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中收货方号码", "查看被代理方拒绝的合同")

        forwarding_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "查看被代理方拒绝的合同")
        #
        receiving_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "查看被代理方拒绝的合同")
        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p/span')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if("¥%s" % total_Amount, price_sum, "获取详情页中商品总价", "查看被代理方拒绝的合同")
        Cs().slide_("580")
        time.sleep(0.5)
        our_service_charge = gl.get_value('our_service_charge')
        our_service_charge_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "查看被代理方拒绝的合同")

        their_service_charge = gl.get_value('their_service_charge')
        their_service_charge_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        self.check_information_if(their_service_charge, their_service_charge_1, "详情页中他方服务费金额", "查看被代理方拒绝的合同")

        submission_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[4]/div[2]')
        self.check_information_time(submission_time, "详情页中提交时间", "查看被代理方拒绝的合同")

        customer_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[5]/div[2]')
        self.check_information_time(customer_time, "详情页中客户拒绝时间", "查看被代理方拒绝的合同")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看被代理方拒绝的合同")

        invoiceApplySn_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[1]/div[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "详情页中发货单号", "查看被代理方拒绝的合同")
        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[3]/div[2]/a')
        self.check_information_re(contractnumber, Contract_number_2, "详情页中合同编号", "查看被代理方拒绝的合同")
        Cs().slide_("700")
        record_state = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                        '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("代理驳回", record_state, "详情页的操作状态", "查看被代理方拒绝的合同")
        record_operator = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                           '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
        self.check_information_re("18772606900_s", record_operator, "详情页的操作者信息", "查看被代理方拒绝的合同")
        failureTag = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_re("其他 金额部分", failureTag, "详情页的拒绝标签", "查看被代理方拒绝的合同")

        remark = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[4]')
        self.check_information_re("fkl", remark, "拒绝后发货申请后的拒绝理由", "查看被代理方拒绝的合同")

        record_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[5]')
        self.check_information_time(record_time, "拒绝后发货申请后的操作时间", "查看被代理方拒绝的合同")

    def see_application_adopt(self):  # 查看被代理方通过的发货申请
        print("*********查看被代理方通过的发货申请***********")
        driver = self.driver
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[1]', "点击发货申请", "查看被代理方通过的发货申请", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]', "点击代理方已通过",
                          "查看被代理方通过的发货申请", "云平台‘发起方’", sys._getframe().f_lineno)

        invoiceApplySn = gl.get_value('invoiceApplySn')
        invoiceApplySn_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看被代理方通过的发货申请", "发起发货申请")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        receiving_party_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中收货单位", "查看被代理方通过的发货申请")

        agent_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "查看被代理方通过的发货申请")

        contract_sum = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00' % total_Amount, contract_sum, "列表中发货金额", "查看被代理方通过的发货申请")
        state_1 = Cs().xpath_text_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('代理方已通过', state_1, "查看发货单信息", "查看被代理方通过的发货申请")

        Cs().xpath_click_(
            xpath_front + '/div/div[4]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击查看", "查看被代理方通过的发货申请",
            "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "发货申请", "发货单详情", "查看被代理方通过的发货申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 已审批', '采购方 已同意', "代理方 已同意", "查看被代理方通过的发货申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        supplierName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplierName_1, "获取详情页中发货方名称", "查看被代理方通过的发货申请")
        supplier_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(supplier_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        supplier_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplier_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaserName_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_1, "获取详情页中收货方名称", "查看被代理方通过的发货申请")
        purchaser_name_page_1 = Cs().xpath_href_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        supplier_address = gl.get_value('supplier_address')  # 销售方（丙）方地址
        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货地址-详情页", "查看被代理方通过的发货申请")

        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址：详情页", "查看被代理方通过的发货申请")

        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)方电话
        supplierPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplierPhone, "获取详情页中发货方号码", "查看被代理方通过的发货申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中收货方号码", "查看被代理方通过的发货申请")

        forwarding_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "查看被代理方通过的发货申请")
        #
        receiving_proportion = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "查看被代理方通过的发货申请")
        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p/span')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if("¥%s" % total_Amount, price_sum, "获取详情页中商品总价", "查看被代理方通过的发货申请")
        Cs().slide_("580")
        time.sleep(0.5)
        our_service_charge = gl.get_value('our_service_charge')
        our_service_charge_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "查看被代理方通过的发货申请")

        their_service_charge = gl.get_value('their_service_charge')
        their_service_charge_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        self.check_information_if(their_service_charge, their_service_charge_1, "详情页中他方服务费金额", "查看被代理方通过的发货申请")

        submission_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[4]/div[2]')
        self.check_information_time(submission_time, "详情页中提交时间", "查看被代理方通过的发货申请")

        customer_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[5]/div[2]')
        self.check_information_time(customer_time, "详情页中客户通过时间", "查看被代理方通过的发货申请")

        customer_time1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[6]/div[2]')
        self.check_information_time(customer_time1, "详情页中代理通过时间", "查看被代理方通过的发货申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看被代理方通过的发货申请")

        invoiceApplySn_1 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[1]/div[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "详情页中发货单号", "查看被代理方通过的发货申请")
        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[4]/div[2]/div[3]/div[2]/a')
        self.check_information_re(contractnumber, Contract_number_2, "详情页中合同编号", "查看被代理方通过的发货申请")
        Cs().slide_("700")
        record_state = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                        '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("代理通过", record_state, "详情页的操作状态", "查看被代理方通过的发货申请")

        record_operator = Cs().xpath_text_('//div[@class="ant-row"]/div/div[2]'
                                           '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
        self.check_information_re("18772606900_s", record_operator, "详情页的操作者信息", "查看被代理方通过的发货申请")

        record_time = Cs().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time, "发起合同后的操作时间", "查看被代理方通过的发货申请")

        print("*********查看代理方通过发货申请后的合同履行***********")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="0$Menu"]/li[4]', "进入合同履行", "查看代理方通过发货申请后的合同", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
        self.catalog_two(driver, "合同管理", "合同履行列表", "查看代理方通过发货申请后的合同", "合同审签列表页一级目录", "合同审签列表页二级目录")
        self.list_three(driver, "全部", "代理采购", "代理销售", "查看代理方通过发货申请后的合同", "合同履行-全部列表",
                        "合同履行-我方待审批列表", "合同履行-合作方待审批列表")

        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "进入代理销售",
                          "查看代理方通过发货申请后的合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        contractnumber_number_3 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(contractnumber, contractnumber_number_3, "校验合同编号是否一致", "查看代理方通过发货申请后的合同")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名

        self.list_contents_seven(driver, '查看代理方通过发货申请后的合同', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中签订日期", "列表中流程节点",
                                 purchaser_name, agent_name, supplier_name,
                                 '￥%s' % gl.get_value(total_Amount), '受托方已通过')
        Cs().xpath_click_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
            "查看代理方通过发货申请后的合同", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同履行", "合同详情", "查看代理方通过发货申请后的合同", "合同详情一级目录", "合同详情二级目录",
                           "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方已审签", "受托方已审签", "查看代理方通过发货申请后的合同",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cs().slide_("100")
        self.contract_content(driver, "查看代理方通过发货申请后的合同")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[5]', "点击操作记录",
                          "校验代理方通过审批后的合同", "云平台‘发起方’", sys._getframe().f_lineno)

        self.Operation_record(driver, "代理商已审签", "深圳926 18772606900_s", "查看代理方通过发货申请后的合同",
                              "查看代理方签审后的操作状态", "查看代理方签审后的操作时间", "查看代理方签审后的操作者信息", "5")
        Cs().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]', "点击履行记录",
                          "校验代理方通过审批后的合同", "云平台‘发起方’", sys._getframe().f_lineno)
        self.performance_record(driver, "校验代理方通过审批后的合同")  # 校验合同履行信息
        #
        print("*****查看通过发货申请后云票额度信息*****")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入额度管理首页", "查看通过发货申请后云票额度信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        total_Amount = gl.get_value('total_Amount')  # 货品总价
        totalCreditQuota_supplier = gl.get_value('totalCreditQuota_supplier')  # 丙 销售总授信云票"
        totalCirculationQuota_supplier = gl.get_value('totalCirculationQuota_supplier')  # 丙 销售总流转云票"
        estimateAddQuota_supplier = gl.get_value("estimateAddQuota_supplier")  # 预增云票
        totalOccupyCreditQuota_supplier = gl.get_value('totalOccupyCreditQuota_supplier')  # 丙 销售 已占用授信云票
        totalOccupyCirculationQuota_supplier = gl.get_value('totalOccupyCirculationQuota_supplier')  # 丙 销售 已占用流转云票
        totalOccupancyCreditQuota_supplier = gl.get_value('totalOccupancyCreditQuota_supplier')  # 丙 销售 可用总授信(总-已用)
        totalOccupancyCirculationQuota_supplier = gl.get_value(
            'totalOccupancyCirculationQuota_supplier')  # 丙 销售 余总流转(总-已用)

        estimateReduceQuota_supplier_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div/div[2]/div[2]')
        self.check_information_re("0", estimateReduceQuota_supplier_1, "预计减少云票",
                                  "查看通过发货申请后云票额度信息")
        surplusAvailableTotalCreditQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupancyCreditQuota_supplier, surplusAvailableTotalCreditQuota_1, "可用授信",
                                  "查看通过发货申请后云票额度信息")
        occupyTotalCreditQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[1]/p[2]')
        self.check_information_re(totalOccupyCreditQuota_supplier, occupyTotalCreditQuota_1, "已用授信",
                                  "查看通过发货申请后云票额度信息")
        totalCreditQuota_1 = Cs().xpath_text_(xpath_front + '/div/div[2]/div/div[1]/div[3]')
        self.check_information_re(totalCreditQuota_supplier, totalCreditQuota_1, "总授信", "查看通过发货申请后云票额度信息")

        estimateAddQuota_supplier_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div[1]/div[2]')  # 预增云票
        estimateAddQuota_supplier_check = int(estimateAddQuota_supplier) + int(total_Amount)
        print(estimateAddQuota_supplier)
        print(total_Amount)
        self.check_information_re(str(estimateAddQuota_supplier_check), estimateAddQuota_supplier_1, "预计增加云票",
                                  "查看通过发货申请后云票额度信息")

        totalCirculationQuota_1 = Cs().xpath_text_(xpath_front + '/div/div[2]/div/div[2]/div[3]')
        totalCirculationQuota_1 = re_sub_(totalCirculationQuota_1)
        self.check_information_re(totalCirculationQuota_supplier, totalCirculationQuota_1, "总流转", "查看通过发货申请后云票额度信息")

        surplusTotalCirculationQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[4]')
        surplusTotalCirculationQuota_1 = re_sub_(surplusTotalCirculationQuota_1)
        self.check_information_re(totalOccupancyCirculationQuota_supplier, surplusTotalCirculationQuota_1,
                                  "剩余流转", "查看通过发货申请后云票额度信息")
        surplusAvailableTotalCirculationQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        surplusAvailableTotalCirculationQuota_check = int(surplusTotalCirculationQuota_1) * 0.8
        self.check_information_re(str(surplusAvailableTotalCirculationQuota_check)[0:-2],
                                  surplusAvailableTotalCirculationQuota_1,
                                  "可用流转", "查看通过发货申请后云票额度信息")
        occupyAvailableTotalCirculationQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupyCirculationQuota_supplier, occupyAvailableTotalCirculationQuota_1,
                                  "已用流转", "查看通过发货申请后云票额度信息")
        loanAbilityQuota_1 = Cs().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[3]/p[2]')
        loanAbilityQuota_check = int(totalOccupancyCirculationQuota_supplier) * 0.5
        self.check_information_re(str(loanAbilityQuota_check), loanAbilityQuota_1, "可贷现", "查看通过发货申请后云票额度信息")

        time.sleep(1)
        Cs().xpath_click_('//*[@id="3$Menu"]/li[5]', "点击进入预计增加云票", "查看通过发货申请后云票额度信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(2.5)
        estimateAddQuota_1 = Cs().xpath_text_(xpath_front + '/div/div/div[1]/span')
        estimateAddQuota_1 = re_sub_(estimateAddQuota_1)  # 显示为12,500.00 正则筛选
        estimateAddQuota_check = int(total_Amount) + int(estimateAddQuota_supplier)
        # estimateAddQuota_check = 10000
        self.check_information_re(str(estimateAddQuota_check), estimateAddQuota_1, "预计增加云票", "查看通过发货申请后云票额度信息")
        invoiceApplySn = gl.get_value('invoiceApplySn')  # DF 发货单
        invoiceApplySn_0 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_0, "发货申请单号", "查看通过发货申请后云票额度信息")
        deliveryGoodTime_1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[3]/div')
        self.check_information_if("", deliveryGoodTime_1, "出货日期", "查看通过发货申请后云票额度信息")
        estimateChangeQuota_2 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[4]/span')
        estimateChangeQuota_2 = re_sub_(estimateChangeQuota_2)  # 显示为12,500.00 正则筛选
        self.check_information_re(estimateAddQuota_check, estimateChangeQuota_2, "预计变化的云票", "查看通过发货申请后云票额度信息")
        totalAmount_1 = Cs().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[5]/span', sys._getframe().f_lineno)
        totalAmount_1 = re_sub_(totalAmount_1)  # 显示为12,500.00 正则筛选
        self.check_information_re(str(total_Amount), totalAmount_1, "发货单货品总价", "查看通过发货申请后云票额度信息")
        shipping_details_page = Cs().xpath_href_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[6]/a')
        # 打开一个新页面
        new_execute_script(shipping_details_page)
        shipping_details = Cs().xpath_text_(
            xpath_front_1 + '/div/span[3]/span[1]/span', sys._getframe().f_lineno)
        self.check_information_if('发货单详情', shipping_details, "发货单货品总价", "查看通过发货申请后云票额度信息")
        Cs().slide_("300", )
        invoiceApplySn_3 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[4]/div[2]/div[1]/div[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_3, "新页面发货申请单号", "查看通过发货申请后云票额度信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        # driver.get('https://python.org')

    # 出货
    def deliver_goods(self):  # 代销方出货
        driver = self.driver
        print("*********代销方出货***********")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[2]', "点击出货管理", "代销方出货", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(3)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击待出货",
                          "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        self.catalog_two(driver, "代销管理", "出货单列表", "代销方出货", "出货单列表页一级目录", "出货单列表页二级目录")
        self.list_six(driver, "所有发货单", "待出货", "已出货", "已收货", "已品检", "已入库", "代销方出货", "出货管理-全部列表",
                      "出货管理-待出货列表", "出货管理-已出货列表", "出货管理-已收货列表", "出货管理-已品检列表", "出货管理-已入库列表")
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        invoiceSn = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]', sys._getframe().f_lineno)
        self.check_information_re('DO', invoiceSn, "列表中发货申请单号", "查看代理方通过发货申请后的出货管理")
        gl.set_value('invoiceSn', invoiceSn)
        receiving_party_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_2, "列表中收货单位", "查看代理方通过发货申请后的出货管理")

        agent_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_2, "列表中代理方", "查看代理方通过发货申请后的出货管理")

        contract_sum1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00' % total_Amount, contract_sum1, "列表中发货金额", "查看代理方通过发货申请后的出货管理")
        state_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('待出货', state_2, "查看发货单状态", "查看代理方通过发货申请后的出货管理")

        Cs().xpath_click_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button',
                          "点击查看", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "出货单列表", "出货单详情", "代销方出货", "代销管理详情页一级目录",
                           "代销管理详情页二级目录", "代销管理详情页三级目录")
        # self.navigation_three(driver, '销售方 已审批', '采购方 已同意', "代理方 已同意", "查看被代理方通过的发货申请",
        #                       "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)  #方电话

        supplier_name_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplier_name_1, "发货单位-详情页", "代销方出货")
        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        supplier_address = gl.get_value('supplier_address')  # 销售方（丙）方地址

        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货地址-详情页", "代销方出货")

        supplier_phone_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplier_phone_1, "发货单位电话", "代销方出货")

        purchaser_name_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位：详情页", "代销方出货")

        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址：详情页", "代销方出货")

        purchaser_phone_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "收货单位电话", "代销方出货")
        total_Amount = gl.get_value('total_Amount')
        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p', sys._getframe().f_lineno)
        price_sum = re_int1(price_sum)
        self.check_information_if(str(total_Amount), price_sum, "获取详情页中商品总价", "代销方出货")
        Cs().slide_("550")
        Luckynumber = random.randint(1, 2)
        print('Luckynumber = %d' % Luckynumber)
        gl.set_value('Luckynumber', Luckynumber)
        if Luckynumber / 2 == 1:  # 双数 物流
            Cs().xpath_click_(xpath_front + '/div/div[3]/div[3]/div[2]/div/div/label[2]',
                              "选中“物流配送”", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
            time.sleep(0.5)
            Cs().xpath_clear_(xpath_front + '/div/div[3]/div[3]/div[2]/div[2]/div[1]/input',
                              sys._getframe().f_lineno)
            Cs().xpath_send_(xpath_front + '/div/div[3]/div[3]/div[2]/div[2]/div[1]/input', "龙门镖局")
            Cs().is_toast_exist("填写物流公司", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
            Cs().xpath_clear_(xpath_front + '/div/div[3]/div[3]/div[2]/div[2]/div[2]/input',
                              sys._getframe().f_lineno)
            Cs().xpath_send_(xpath_front + '/div/div[3]/div[3]/div[2]/div[2]/div[2]/input', "12580",
                             sys._getframe().f_lineno)
            Cs().is_toast_exist("物流单号", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
            Cs().xpath_send_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div[2]/div[3]/span/div[2]/span/input[@type="file"]',
                "D:\shangwo\图片信息\物流单.jpg", sys._getframe().f_lineno)  # 上传图片
            Cs().is_toast_exist("上传物流单", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
            time.sleep(2.5)
            Cs().xpath_send_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div[2]/div[4]/span/div[2]/span/input[@type="file"]',
                "D:\shangwo\图片信息\出货单.jpg", sys._getframe().f_lineno)  # 上传图片
            Cs().is_toast_exist("上传出货单", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
            time.sleep(2.5)
            Cs().slide_("900", sys._getframe().f_lineno)
            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "代销方出货")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "代销方出货")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "代销方出货")

            shipment_time = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "代销方出货")

            supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方926链号
            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('供应商待出货', record_state1, "操作记录中未出货状态", '代销方出货')

            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if('13245678999_s', record_operator1, "操作记录中发起申请操作人", '代销方出货')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '代销方出货')

            Cs().xpath_click_('//div[@class="ant-row"]/div/div[2]/div/div[3]/div[6]/button', "点击确认出货",
                              "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
        else:  # 单数自提
            Cs().xpath_click_(xpath_front + '/div/div[3]/div[3]/div[2]/div/div/label[1]',
                              "选中“自提”", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "代销方出货")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "代销方出货")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "代销方出货")

            shipment_time = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "代销方出货")

            supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方926链号
            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('供应商待出货', record_state1, "操作记录中未出货状态", '代销方出货')

            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(supplier_name, record_operator1, "操作记录中发起申请操作人", '代销方出货')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '代销方出货')

            Cs().xpath_click_('//div[@class="ant-row"]/div/div[2]/div/div[3]/div[6]/button', "点击确认出货",
                              "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)

        print("*********查看代销方出货后的货单信息***********")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[2]', "点击出货管理", "查看代销方出货后的货单信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击已出货",
                          "查看代销方出货后的货单信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        invoiceSn = gl.get_value('invoiceSn')
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        invoiceSn_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_if(invoiceSn, invoiceSn_2, "列表中发货申请单号", "查看代销方出货后的货单信息")

        receiving_party_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_2, "列表中收货单位", "查看代销方出货后的货单信息")

        agent_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_2, "列表中代理方", "查看代销方出货后的货单信息")

        contract_sum1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥$s.00' % total_Amount, contract_sum1, "列表中发货金额", "查看代销方出货后的货单信息")
        state_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('已出货', state_2, "查看发货单信息", "查看代销方出货后的货单信息")

        Cs().xpath_click_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button',
                          "点击查看", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "出货单列表", "出货单详情", "查看代销方出货后的货单信息", "代销管理详情页一级目录",
                           "代销管理详情页二级目录", "代销管理详情页三级目录")
        self.navigation_four(driver, '待收货', '待品检', "待入库", "入库完成", "查看代销方出货后的货单信息",
                             "出货详情第一步导航信息", "出货详情第二步导航信息", "出货详情第三步导航信息", "出货详情第四步导航信息")
        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)  #方电话

        supplier_name_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplier_name_1, "发货单位-详情页", "查看代销方出货后的货单信息")

        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        supplier_address = gl.get_value('supplier_address')  # 销售方（丙）方地址
        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货地址-详情页", "查看代销方出货后的货单信息")

        supplier_phone_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplier_phone_1, "发货单位电话", "查看代销方出货后的货单信息")

        purchaser_name_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位：详情页", "查看代销方出货后的货单信息")
        purchaser_address = gl.get_value('purchaser_address')
        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址：详情页", "查看代销方出货后的货单信息")

        purchaser_phone_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "收货单位电话", "查看代销方出货后的货单信息")
        total_Amount = gl.get_value('total_Amount')
        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p', sys._getframe().f_lineno)
        price_sum = re_int1(price_sum)
        self.check_information_if(str(total_Amount), price_sum, "获取详情页中商品总价", "查看代销方出货后的货单信息")
        try:
            Cs().slide_("555", sys._getframe().f_lineno)
            print("++++++++++++++++++++++++++++++++++=")
            companyName = driver.find_element_by_xpath(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[1]/div[1]/div[2]').text
            self.check_information_if('龙门镖局', companyName, "详情页中物流公司信息", "查看代销方出货后的货单信息")
            print("校验是否为物流配送，获取物流公司信息：%s " % companyName)
            logisticsSn = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[1]/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('12580', logisticsSn, "详情页中物流单号信息", "查看代销方出货后的货单信息")
            logistics_img = Cs().xpath_src_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_re('3f208131bd12d16ae283596c943dd507.jpg', logistics_img, "详情页中物流单图片",
                                      "查看代销方出货后的货单信息")
            invoiceApply_img = Cs().xpath_src_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_re('d47b0c57843a9a9087af58b1080b2a2b.jpg', invoiceApply_img, "详情页中出货单图片",
                                      "查看代销方出货后的货单信息")
            Cs().slide_("1900", sys._getframe().f_lineno)
            gl.set_value('logisticsSn', logisticsSn)  # 物流公司信息
            gl.set_value('companyName', companyName)  # 物流单号信息
            gl.set_value('logistics_img', logistics_img)  # 详情页中物流单图片
            gl.set_value('invoiceApply_img', invoiceApply_img)  # 详情页中出货单图片
            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "查看代销方出货后的货单信息")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看代销方出货后的货单信息")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "查看代销方出货后的货单信息")

            shipment_time = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "查看代销方出货后的货单信息")

            supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方926链号
            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商待收货', record_state1, "操作记录中未出货状态", '查看代销方出货后的货单信息')

            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(supplier_name, record_operator1, "操作记录中发起申请操作人", '查看代销方出货后的货单信息')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '查看代销方出货后的货单信息')

        except Exception:
            Cs().slide_("555", sys._getframe().f_lineno)
            distribution_mode = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if('自提', distribution_mode, "详情页中出货单编号", "查看代销方出货后的货单信息")
            gl.set_value('distribution_mode', distribution_mode)

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "查看代销方出货后的货单信息")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看代销方出货后的货单信息")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "查看代销方出货后的货单信息")

            shipment_time = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "查看代销方出货后的货单信息")

            supplier_name = gl.get_value('supplier_name')  # 丙（销售)  #方926链号
            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商待收货', record_state1, "操作记录中未出货状态", '查看代销方出货后的货单信息')

            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(supplier_name, record_operator1, "操作记录中发起申请操作人", '查看代销方出货后的货单信息')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '查看代销方出货后的货单信息')

    # 采购收货
    def purchaser_collect(self):
        driver = self.driver
        print("*********查看采购方收货后的货单信息***********")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[2]', "点击出货管理", "查看采购方收货后的货单信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]', "点击已收货",
                          "查看采购方收货后的货单信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        invoiceSn = gl.get_value('invoiceSn')
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        invoiceSn_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_if(invoiceSn, invoiceSn_2, "列表中发货申请单号", "查看采购方收货后的货单信息")

        receiving_party_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_2, "列表中收货单位", "查看采购方收货后的货单信息")

        agent_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_2, "列表中代理方", "查看采购方收货后的货单信息")

        contract_sum1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00' % total_Amount, contract_sum1, "列表中发货金额", "查看采购方收货后的货单信息")
        state_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('已收货', state_2, "查看发货单信息", "查看采购方收货后的货单信息")

        Cs().xpath_click_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button',
                          "点击查看", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "出货单列表", "出货单详情", "查看采购方收货后的货单信息", "代销管理详情页一级目录",
                           "代销管理详情页二级目录", "代销管理详情页三级目录")
        self.navigation_four(driver, '待收货', '待品检', "待入库", "入库完成", "查看采购方收货后的货单信息",
                             "出货详情第一步导航信息", "出货详情第二步导航信息", "出货详情第三步导航信息", "出货详情第四步导航信息")
        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)  #方电话
        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        supplier_address = gl.get_value('supplier_address')  # 销售方（丙）方地址

        supplier_name_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplier_name_1, "发货单位", "采购方收货")

        # supplier_name_page_1 = Cs().xpath_href_(
        #     xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        # new_execute_script(supplier_name_page_1)
        # self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
        #                    "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        # supplier_name_2 = Cs().xpath_text_(
        #     xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        # self.check_information_if(supplier_name, supplier_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # # 定位回原来的页面
        # driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货地址：详情页", "采购方收货")

        supplier_phone_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplier_phone_1, "发货单位电话", "采购方收货")
        total_Amount = gl.get_value('total_Amount')

        purchaser_name_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位-详情页", "采购方收货")

        # purchaser_name_page_1 = Cs().xpath_href_(
        #     xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        # new_execute_script(purchaser_name_page_1)
        # self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
        #                    "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        # purchaser_name_2 = Cs().xpath_text_(
        #     xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        # self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # # 定位回原来的页面
        # driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址-详情页", "采购方收货")

        purchaser_phone_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_phone, purchaser_phone_1, "收货单位电话：详情页", "采购方收货")

        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p', sys._getframe().f_lineno)
        price_sum = re_int1(price_sum)
        self.check_information_if(str(total_Amount), price_sum, "获取详情页中商品总价", "采购方收货")
        try:
            Cs().slide_("555", sys._getframe().f_lineno)
            logisticsSn = gl.get_value('logisticsSn')  # 物流公司信息
            companyName = gl.get_value('companyName')  # 物流单号信息
            logistics_img = gl.get_value('logistics_img')  # 详情页中物流单图片
            invoiceApply_img = gl.get_value('invoiceApply_img')  # 详情页中出货单图片
            companyName_1 = driver.find_element_by_xpath(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[1]/div[1]/div[2]').text
            self.check_information_if(companyName, companyName_1, "详情页中物流公司信息", "查看代销方出货后的货单信息")
            print("校验是否为物流配送，获取物流公司信息：%s " % companyName)
            logisticsSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[1]/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(logisticsSn, logisticsSn_1, "详情页中物流单号信息", "查看代销方出货后的货单信息")
            logistics_img_1 = Cs().xpath_src_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_re(logistics_img, logistics_img_1, "详情页中物流单图片", "查看代销方出货后的货单信息")
            invoiceApply_img_1 = Cs().xpath_src_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_if(invoiceApply_img, invoiceApply_img_1, "详情页中出货单图片",
                                      "查看代销方出货后的货单信息")
            Cs().slide_("1900", sys._getframe().f_lineno)

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "查看采购方收货后的货单信息")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看采购方收货后的货单信息")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "查看采购方收货后的货单信息")

            shipment_time = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "查看采购方收货后的货单信息")

            supplier_926 = gl.get_value('supplier_926')  # 丙（销售)  #方926链号
            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已收货', record_state1, "操作记录中未出货状态", '查看采购方收货后的货单信息')

            purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '查看采购方收货后的货单信息')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '查看采购方收货后的货单信息')

        except Exception:
            Cs().slide_("555", sys._getframe().f_lineno)
            distribution_mode = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if('自提', distribution_mode, "详情页中出货单编号", "查看采购方收货后的货单信息")
            gl.set_value('distribution_mode', distribution_mode)

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "查看采购方收货后的货单信息")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看采购方收货后的货单信息")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "查看采购方收货后的货单信息")

            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已收货', record_state1, "操作记录中未出货状态", '查看采购方收货后的货单信息')

            purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '查看采购方收货后的货单信息')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '查看采购方收货后的货单信息')

    # 采购品检
    def purchaser_inspection(self):
        driver = self.driver
        print("*********查看采购方品检后的货单信息***********")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[2]', "点击出货管理", "查看采购方品检后的货单信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]', "点击已品检",
                          "查看采购方品检后的货单信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        invoiceSn = gl.get_value('invoiceSn')
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        invoiceSn_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_if(invoiceSn, invoiceSn_2, "列表中发货申请单号", "查看采购方品检后的货单信息")

        receiving_party_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_2, "列表中收货单位", "查看采购方品检后的货单信息")

        agent_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_2, "列表中代理方", "查看采购方品检后的货单信息")

        contract_sum1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00' % total_Amount, contract_sum1, "列表中发货金额", "查看采购方品检后的货单信息")
        state_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('已品检', state_2, "查看发货单信息", "查看采购方品检后的货单信息")

        Cs().xpath_click_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button',
                          "点击查看", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "出货单列表", "出货单详情", "查看采购方品检后的货单信息", "代销管理详情页一级目录",
                           "代销管理详情页二级目录", "代销管理详情页三级目录")
        self.navigation_four(driver, '待收货', '待品检', "待入库", "入库完成", "查看采购方品检后的货单信息",
                             "出货详情第一步导航信息", "出货详情第二步导航信息", "出货详情第三步导航信息", "出货详情第四步导航信息")
        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)  #方电话
        supplierAdress = gl.get_value('supplierAdress')
        purchaserAdress = gl.get_value('purchaserAdress')

        supplier_name_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplier_name_1, "发货单位", "查看采购方品检后的货单信息")

        # supplier_name_page_1 = Cs().xpath_href_(
        #     xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        # new_execute_script(supplier_name_page_1)
        # self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看采购方品检后的货单信息",
        #                    "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        # supplier_name_2 = Cs().xpath_text_(
        #     xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        # self.check_information_if(supplier_name, supplier_name_2, "新页面中销售方企业名称信息", "查看采购方品检后的货单信息")
        # # 定位回原来的页面
        # driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        supplier_address = gl.get_value('supplier_address')
        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货单位：详情页", "查看采购方品检后的货单信息")

        supplier_phone_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplier_phone_1, "发货单位电话", "查看采购方品检后的货单信息")
        total_Amount = gl.get_value('total_Amount')

        purchaser_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位-详情页", "查看采购方品检后的货单信息")

        # purchaser_name_page_1 = Cs().xpath_href_(
        #     xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        # new_execute_script(purchaser_name_page_1)
        # self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看采购方品检后的货单信息",
        #                    "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        # purchaser_name_2 = Cs().xpath_text_(
        #     xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        # self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看采购方品检后的货单信息")
        # # 定位回原来的页面
        # driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        purchaser_address = gl.get_value('purchaser_address')
        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址-详情页", "查看采购方品检后的货单信息")

        purchaser_phone_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "收货单位电话：详情页", "查看采购方品检后的货单信息")

        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p', sys._getframe().f_lineno)
        price_sum = re_int1(price_sum)
        self.check_information_if(str(total_Amount), price_sum, "获取详情页中商品总价", "查看采购方品检后的货单信息")
        try:
            Cs().slide_("555", sys._getframe().f_lineno)
            logisticsSn = gl.get_value('logisticsSn')  # 物流公司信息
            companyName = gl.get_value('companyName')  # 物流单号信息
            logistics_img = gl.get_value('logistics_img')  # 详情页中物流单图片
            invoiceApply_img = gl.get_value('invoiceApply_img')  # 详情页中出货单图片
            companyName_1 = driver.find_element_by_xpath(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[1]/div[1]/div[2]').text
            self.check_information_if(companyName, companyName_1, "详情页中物流公司信息", "查看采购方品检后的货单信息")
            print("校验是否为物流配送，获取物流公司信息：%s " % companyName)
            logisticsSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[1]/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(logisticsSn, logisticsSn_1, "详情页中物流单号信息", "查看采购方品检后的货单信息")
            logistics_img_1 = Cs().xpath_src_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_re(logistics_img, logistics_img_1, "详情页中物流单图片",
                                      "查看采购方品检后的货单信息")
            invoiceApply_img_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_if(invoiceApply_img, invoiceApply_img_1, "详情页中出货单图片",
                                      "查看采购方品检后的货单信息")
            Cs().slide_("1900", sys._getframe().f_lineno)

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "查看采购方品检后的货单信息")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看采购方品检后的货单信息")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "查看采购方品检后的货单信息")

            shipment_time = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "查看采购方品检后的货单信息")

            supplier_926 = gl.get_value('supplier_926')  # 丙（销售)  #方926链号
            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已品检', record_state1, "操作记录中未出货状态", '查看采购方品检后的货单信息')

            purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '查看采购方品检后的货单信息')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '查看采购方品检后的货单信息')

        except Exception:
            Cs().slide_("555", sys._getframe().f_lineno)
            distribution_mode = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if('自提', distribution_mode, "详情页中出货单编号", "查看采购方品检后的货单信息")
            gl.set_value('distribution_mode', distribution_mode)

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "查看采购方品检后的货单信息")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看采购方品检后的货单信息")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "查看采购方品检后的货单信息")

            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已品检', record_state1, "操作记录中未出货状态", '查看采购方品检后的货单信息')

            purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '查看采购方品检后的货单信息')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '查看采购方品检后的货单信息')

    # 采购入库
    def purchaser_warehousing(self):
        driver = self.driver
        print("*********查看采购方入库后的货单信息***********")
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[2]', "点击出货管理", "查看采购方入库后的货单信息", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(1)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[6]', "点击已入库",
                          "查看采购方入库后的货单信息", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        invoiceSn = gl.get_value('invoiceSn')
        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        supplier_name = gl.get_value('supplier_name')  # 丙（销售)方企业名
        invoiceSn_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_if(invoiceSn, invoiceSn_2, "列表中发货申请单号", "查看采购方入库后的货单信息")

        receiving_party_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_2, "列表中收货单位", "查看采购方入库后的货单信息")

        agent_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_2, "列表中代理方", "查看采购方入库后的货单信息")

        contract_sum1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00' % total_Amount, contract_sum1, "列表中发货金额", "查看采购方入库后的货单信息")
        state_2 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('已入库', state_2, "查看发货单信息", "查看采购方入库后的货单信息")

        Cs().xpath_click_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button',
                          "点击查看", "代销方出货", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "出货单列表", "出货单详情", "查看采购方入库后的货单信息", "代销管理详情页一级目录",
                           "代销管理详情页二级目录", "代销管理详情页三级目录")
        self.navigation_four(driver, '待收货', '待品检', "待入库", "入库完成", "查看采购方入库后的货单信息",
                             "出货详情第一步导航信息", "出货详情第二步导航信息", "出货详情第三步导航信息", "出货详情第四步导航信息")
        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        supplier_phone = gl.get_value('supplier_phone')  # 丙（销售)  #方电话
        supplierAdress = gl.get_value('supplierAdress')
        purchaserAdress = gl.get_value('purchaserAdress')

        supplier_name_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(supplier_name, supplier_name_1, "发货单位", "查看采购方入库后的货单信息")

        # supplier_name_page_1 = Cs().xpath_href_(
        #     xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        # new_execute_script(supplier_name_page_1)
        # self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看采购方入库后的货单信息",
        #                    "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        # supplier_name_2 = Cs().xpath_text_(
        #     xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        # self.check_information_if(supplier_name, supplier_name_2, "新页面中销售方企业名称信息", "查看采购方入库后的货单信息")
        # # 定位回原来的页面
        # driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        supplier_address = gl.get_value('supplier_address')
        supplierAdress_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(supplier_address, supplierAdress_1, "发货单位：详情页", "查看采购方入库后的货单信息")

        supplier_phone_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(supplier_phone, supplier_phone_1, "发货单位电话", "查看采购方入库后的货单信息")
        total_Amount = gl.get_value('total_Amount')

        purchaser_name_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位-详情页", "查看采购方入库后的货单信息")

        # purchaser_name_page_1 = Cs().xpath_href_(
        #     xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        # new_execute_script(purchaser_name_page_1)
        # self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看采购方入库后的货单信息",
        #                    "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        # purchaser_name_2 = Cs().xpath_text_(
        #     xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        # self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看采购方入库后的货单信息")
        # # 定位回原来的页面
        # driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        purchaser_address = gl.get_value('purchaser_address')
        purchaserAdress_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "收货地址-详情页", "查看采购方入库后的货单信息")

        purchaser_phone_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "收货单位电话：详情页", "查看采购方入库后的货单信息")

        price_sum = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p', sys._getframe().f_lineno)
        price_sum = re_int1(price_sum)
        self.check_information_if(str(total_Amount), price_sum, "获取详情页中商品总价", "查看采购方入库后的货单信息")
        try:
            Cs().slide_("555", sys._getframe().f_lineno)
            logisticsSn = gl.get_value('logisticsSn')  # 物流公司信息
            companyName = gl.get_value('companyName')  # 物流单号信息
            logistics_img = gl.get_value('logistics_img')  # 详情页中物流单图片
            invoiceApply_img = gl.get_value('invoiceApply_img')  # 详情页中出货单图片
            companyName_1 = driver.find_element_by_xpath(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[1]/div[1]/div[2]').text
            self.check_information_if(companyName, companyName_1, "详情页中物流公司信息", "查看采购方入库后的货单信息")
            print("校验是否为物流配送，获取物流公司信息：%s " % companyName)
            logisticsSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[1]/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(logisticsSn, logisticsSn_1, "详情页中物流单号信息", "查看采购方入库后的货单信息")
            logistics_img_1 = Cs().xpath_src_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[2]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_re(logistics_img, logistics_img_1, "详情页中物流单图片",
                                      "查看采购方入库后的货单信息")
            invoiceApply_img_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_if(invoiceApply_img, invoiceApply_img_1, "详情页中出货单图片",
                                      "查看采购方入库后的货单信息")
            Cs().slide_("1900", sys._getframe().f_lineno)

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "查看采购方入库后的货单信息")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看采购方入库后的货单信息")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "查看采购方入库后的货单信息")

            shipment_time = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "查看采购方入库后的货单信息")

            supplier_926 = gl.get_value('supplier_926')  # 丙（销售)  #方926链号
            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已入库', record_state1, "操作记录中未出货状态", '查看采购方入库后的货单信息')

            purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '查看采购方入库后的货单信息')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '查看采购方入库后的货单信息')
        except Exception:
            Cs().slide_("555", sys._getframe().f_lineno)
            distribution_mode = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[3]/div[2]/div/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if('自提', distribution_mode, "详情页中出货单编号", "查看采购方入库后的货单信息")
            gl.set_value('distribution_mode', distribution_mode)

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "查看采购方入库后的货单信息")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "查看采购方入库后的货单信息")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "查看采购方入库后的货单信息")

            record_state1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已入库', record_state1, "操作记录中未出货状态", '查看采购方入库后的货单信息')

            purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
            record_operator1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '查看采购方入库后的货单信息')

            record_time1 = Cs().xpath_text_(
                xpath_front + '/div/div[3]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '查看采购方入库后的货单信息')

    def send_invoice(self):
        driver = self.driver
        # Cs().slide_("0")
        Cs().xpath_click_('//*[@id="1$Menu"]/li[3]', "点击寄票信息", "代销方寄票", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(2.5)
        # 校验目录信息
        self.catalog_two(driver, "代销管理", "寄票信息", "代销方寄票", "寄票信息列表页一级目录", "寄票信息列表页二级目录")
        self.list_four(driver, "全部", "待寄票", "已寄票", "已收票", "代销方寄票", "代销管理-所有发货单列表",
                       "代销管理-待寄票列表", "代销管理-已寄票列表", "代销管理-已收票列表")

        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击待寄票",
                          "代销方寄票", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        purchaser_name = gl.get_value('purchaser_name')
        agent_name = gl.get_value('agent_name')
        total_Amount = gl.get_value('total_Amount')
        receiptSn = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]', sys._getframe().f_lineno)
        self.check_information_re("SP", receiptSn, "列表页寄票编号", '代销方寄票')
        gl.set_value('receiptSn', receiptSn)
        supplierName = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[3]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, supplierName, "列表页寄票单位", '代销方寄票')
        agentName = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]', sys._getframe().f_lineno)
        self.check_information_if(agent_name, agentName, "列表页收票单位", '代销方寄票')
        totalAmount = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]', sys._getframe().f_lineno)
        self.check_information_re(str(total_Amount), totalAmount, "列表页寄票金额", '代销方寄票')
        state_1 = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]', sys._getframe().f_lineno)
        self.check_information_if('供应商待寄票', state_1, "列表页寄票状态", '代销方寄票')
        Cs().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button', "点击查看", "代销方寄票",
            "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        self.catalog_three(driver, "代销管理", "寄票信息", "寄票详情", "代销方寄票", "寄票信息详情页一级目录"
                           , "寄票信息详情页二级目录", "寄票信息详情页二级目录")
        self.navigation_three(driver, '待寄发票', '寄票', "完成收票", "代销方寄票",
                              "出货详情第一步导航信息", "出货详情第二步导航信息", "出货详情第三步导航信息")

        receiptSn_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[1]/div[2]',
                                       sys._getframe().f_lineno)
        self.check_information_if(receiptSn, receiptSn_1, "详情页寄票编号", '代销方寄票')
        supplier_name = gl.get_value('supplier_name')
        supplierName = Cs().xpath_text_(xpath_front + '/div/div[3]/div[1]/div[2]/div/div/div[2]/div[2]',
                                        sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplierName, "详情页寄票单位", '代销方寄票')

        contractnumber = gl.get_value('contractnumber')
        contractSn_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div[1]/div[2]',
                                        sys._getframe().f_lineno)
        self.check_information_if(contractnumber, contractSn_1, "详情页代理合同", '代销方寄票')

        invoiceSn = gl.get_value('invoiceSn')
        invoiceSn_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div[2]/div[2]/a',
                                       sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "详情页发货编号", '代销方寄票')

        Cs().xpath_click_(xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div[2]/div[2]/a',
                          "点击详情页发货编号", '代销方寄票', "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        self.catalog_three(driver, "代销管理", "出货单列表", "出货单详情", "代销方寄票",
                           "出货管理页一级目录", "出货管理页二级目录", '出货管理页三级目录')
        driver.back()
        time.sleep(1)

        invoiceReceiptSn = Cs().xpath_text_(xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div[3]/div[2]',
                                            sys._getframe().f_lineno)
        self.check_information_if(receiptSn, invoiceReceiptSn, "详情页寄票单号", '代销方寄票')

        Cs().xpath_click_(xpath_front + '/div/div[3]/div[4]/button', "点击确认寄票", "代销方寄票", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        Cs().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认",
                          "代销方寄票", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        invoiceReceipt_time = Cs().xpath_text_(
            xpath_front + '/div/div[3]/div[2]/div[2]/div/div/div[4]/div[2]',
            sys._getframe().f_lineno)
        self.check_information_time(invoiceReceipt_time, "寄票时间", '代销方寄票')

        Cs().xpath_click_('//*[@id="1$Menu"]/li[3]', "点击寄票信息", "代销方寄票", "云平台‘发起方’",
                          sys._getframe().f_lineno)
        time.sleep(2.5)
        Cs().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击已寄票",
                          "代销方寄票", "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(2.5)
        supplier_name = gl.get_value('supplier_name')
        agent_name = gl.get_value('agent_name')
        total_Amount = gl.get_value('total_Amount')
        receiptSn_2 = Cs().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody'
                                                     '/tr/td[2]', sys._getframe().f_lineno)
        self.check_information_re(receiptSn, receiptSn_2, "操作记录中发起申请时间", '代销方寄票')

        supplierName = Cs().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody'
                                                      '/tr/td[3]', sys._getframe().f_lineno)
        self.check_information_if(supplier_name, supplierName, "操作记录中发起申请时间", '代销方寄票')
        agentName = Cs().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody'
                                                   '/tr/td[4]', sys._getframe().f_lineno)
        self.check_information_if(agent_name, agentName, "操作记录中发起申请时间", '代销方寄票')
        totalAmount = Cs().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody'
                                                     '/tr/td[5]', sys._getframe().f_lineno)

        self.check_information_re(str(total_Amount), totalAmount, "操作记录中发起申请时间", '代销方寄票')
        state_1 = Cs().xpath_text_(xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody'
                                                 '/tr/td[6]', sys._getframe().f_lineno)
        self.check_information_if('代理商待收票', state_1, "操作记录中发起申请时间", '代销方寄票')

    def run(self):  # 实现主要逻辑
        # self.driver.get(self.start_url)
        self.login()  # 登录

    def run1(self):
        self.contract()  # 发起方申请委托
        self.contract_initiated()  # 发起方编辑委托

    def run1_1(self):
        self.refuse_entrust()  # 修改被合作方拒绝的合同

    def run1_2(self):
        self.refuse_entrust_1()  # 修改被代理方拒绝的合同

    def run1_3(self):
        self.see_cooperation_adopt()  # 校验代理方通过审批后的合同信息

    def run2(self):
        self.Delivery_application()  # 代销方申请发货

    def run2_1(self):
        self.refuse_application()  # 查看被合作方拒绝的申请

    def run2_2(self):
        self.adopt_application_1()  # 查看被合作方通过的申请

    def run2_3(self):
        self.refuse_application_1()  # 查看被代理方拒绝的申请

    def run2_4(self):
        self.see_application_adopt()  # 查看被代理方通过的申请

    def run3(self):
        self.deliver_goods()  # 供应方发货

    def run3_1(self):
        self.purchaser_collect()  # 采购收

    def run3_2(self):
        self.purchaser_inspection()  # 采购品检

    def run3_3(self):
        self.purchaser_warehousing()  # 采购入库

    def run4(self):
        self.send_invoice()  # 供应方寄票

    def run_excel(self):
        Cs().excel_write()  # 写入excel


if __name__ == '__main__':
    gongyin = PC_926_supplier()

    gongyin.run()  # 登录
    gongyin.run1()  # 发起方申请委托 + 发起方修改委托
    # gongyin.run1_1()  # 修改被合作方拒绝的合同
    # gongyin.run1_2()  # 修改被代理方拒绝的合同
    # gongyin.run1_3()  # 校验代理方通过审批后的合同信息
    # gongyin.run2()  # 代销方申请发货
    # gongyin.run2_1()  # 代销方申请发货
    # gongyin.run2()  # 代销方申请发货
    # gongyin.run2_1()  # 查看被合作方拒绝的合同
    # gongyin.run2_2()  # 查看被合作方通过的合同
    # gongyin.run2_3()  # 查看被代理方拒绝的合同
    # gongyin.run2_4()  # 查看被代理方通过的合同
    # gongyin.run3()  # 供应方发货
    # gongyin.run4()  # 供应方寄票

    # gongyin.run_excel()  # 写入excel
