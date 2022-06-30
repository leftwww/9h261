# -- coding: utf-8 -- 
# @Author : Zw
# @File : pc_926_agent.py


from config.config_purchaser import Config_pc_purchaser as Cp, Logger
import config.globalvar as gl
import time, datetime, sys, os, re
import shutil
import xlrd, xlutils, xlwt
from xlrd import open_workbook
from xlutils.copy import copy


def current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "-采购方-"
    return current_time


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


def tes1t_time():
    test_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return test_time


path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('log_pc.txt')

start_url = Cp().start_url
if re.findall('test', start_url) or re.findall('b.926.net', start_url):
    xpath_front = '//*[@id="root"]/div/section/div[2]/section/main/div/div/div/div[2]'
    xpath_front_1 = '//*[@id="root"]/div/section/div[2]/section/main/div/div/div/div[1]'
    xpath_front_2 = '//*[@id="root"]/div/section/div[3]/section/main/div/div/div/div[2]'
    xpath_main = '//main[@class="ant-layout-content"]'
else:
    xpath_front = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div[2]'
    xpath_front_1 = '//*[@id="root"]/div/div/div[2]/div[2]/div/div/div/div/div[1]'
    xpath_main = '//*[@id="root"]/div/div/div[2]/div[2]/div'

count = 0


# 获取新的页面信息
def new_execute_script(test):
    global count
    count += 1  # 调用一次则加一
    print("count : %d" % count)
    driver = Cp().driver
    # 打开一个新页面
    driver.execute_script('window.open()')
    # 定位到新的页面
    driver.switch_to.window(driver.window_handles[count])  # 新的页面则用最新的索引
    driver.get(test)
    time.sleep(2)
    print("切换跳转至另一页面")
    # 定位回原来的页面
    # driver.switch_to.window(driver.window_handles[0])


class PC_926_purchaser:
    start_url = Cp().start_url
    driver = Cp().driver
    # book = open_workbook("C:\\Users\Zuow\Desktop\\test_case.xlsx")
    # news = []
    gl._init()
    a = 0
    
    
    def check_information_if(self, Check_value, capture, Check_contents, process):
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if Check_value == capture:
            Cp().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘采购方’",
                                                sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % Check_value)
            Cp().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘采购方’",
                                               sys._getframe().f_lineno)

    def check_information_re(self, Check_value, capture, Check_contents, process):
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if re.findall(Check_value, capture):
            Cp().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘采购方’",
                                                sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % Check_value)
            Cp().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘采购方’",
                                               sys._getframe().f_lineno)

    def check_information_time(self, capture, Check_contents, process):
        # capture = 获取到的值  Check_value = 校验获取到的值 Check_contents = 校验内容 process = 哪个环节
        if re.findall(tes1t_time(), capture):
            Cp().is_toast_exist("校验 %s  成功" % Check_contents, process, "云平台‘采购方’",
                                                sys._getframe().f_lineno)
        else:
            print("获取的信息为：%s" % capture + "  ----  " + "检验参数为：%s" % tes1t_time())
            Cp().is_page_exist("校验 %s 失败 " % Check_contents, process, "云平台‘采购方’",
                                               sys._getframe().f_lineno)

            # 获取新的页面信息

    # 校验操作记录
    def Operation_record(self, driver, information, information_user, step, check_info, check_time, check_user,
                         hierarchy):
        time.sleep(1)

        record_state1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[%s]/div[2]/ul/li/div[3]/div/div[1]' % hierarchy)
        self.check_information_if(information, record_state1, check_info, step)  # information"发起方修改合同申请"  step"修改合同"
        # Cp().is_toast_exist("获取发起合同后的操作状态", "修改合同", "云平台‘采购方’",sys._getframe().f_lineno)
        record_time1 = Cp().xpath_text_(xpath_front + '/div/div/div[3]/div[3]/div[%s]/div[2]/ul/li'
                                                                      '/div[3]/div/div[3]' % hierarchy)
        self.check_information_time(record_time1, check_time, step)
        # Cp().is_toast_exist("获取发起合同后的操作时间", "修改合同", "云平台‘采购方’",sys._getframe().f_lineno)
        record_operator1 = Cp().xpath_text_(xpath_front + '/div/div/div[3]/div[3]/div[%s]/div[2]'
                                                                          '/ul/li/div[3]/div/div[2]' % hierarchy)
        self.check_information_if(information_user, record_operator1, check_user, step)

    # 校验被拒绝后的操作记录
    def Operation_record_refuse(self, driver, information, information_user, step, check_info, check_time, check_user,
                                check_reason, check_details):
        time.sleep(1)
       
        record_state1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[1]')
        self.check_information_if(information, record_state1, check_info, step)

        record_time1 = Cp().xpath_text_(xpath_front + '/div/div/div[3]/div[3]/div[4]'
                                                                      '/div[2]/ul/li[1]/div[3]/div/div[5]')
        self.check_information_time(record_time1, check_time, step)

        record_operator1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[2]')
        self.check_information_if(information_user, record_operator1, check_user, step)
        
        global cooperation_refuse_details,cooperation_refuse_reason
        cooperation_refuse_details = gl.get_value('cooperation_refuse_details')
        cooperation_refuse_reason = gl.get_value('cooperation_refuse_reason')
        refuse_reason1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[3]')
        self.check_information_re(cooperation_refuse_reason, refuse_reason1, check_reason, step)

        refuse_details1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/ul/li[1]/div[3]/div/div[4]')
        self.check_information_re(cooperation_refuse_details, refuse_details1, check_details, step)

    def performance_record(self, driver, step):
        total_Amount = gl.get_value('total_Amount')  # 货品总价
        purchaser_name = gl.get_value('purchaser_name')
        agent_name = gl.get_value('agent_name')
        purchaser_name = gl.get_value('purchaser_name')
        invoiceApplySn = gl.get_value('invoiceApplySn')  # DF 发货单
        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[1]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "履行记录中采购（甲）方公司名称", step)
        agent_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[3]/div[2]')
        self.check_information_if(agent_name, agent_name_1, "履行记录中代理（乙）方公司名称", step)
        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[2]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "履行记录中销售方（丙）方公司名称", step)
        price_sum_check_all_ = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[4]/div[2]/span')
        self.check_information_re(str(total_Amount), price_sum_check_all_, "履行记录中合同总价", step)
        total_Amount_ = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[5]/div/div[1]/div/div/span')
        self.check_information_re(str(total_Amount), total_Amount_, "履行记录中发货商品总价", step)
        # todo 校验代理通过时间
        if step == "校验代理方通过审批后的合同":
            application_adopt_time = Cp().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[5]/div/div[2]/div/div[1]/div[2]')
            self.check_information_time(application_adopt_time, "履行记录中发货申请通过时间", step)
            state_ = Cp().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[5]/div/div[2]/div/div[2]/div[2]')
            self.check_information_if("发货", state_, "履行记录中发货方出货时间", step)
            invoiceApplySn_ = Cp().xpath_text_(
                xpath_front + '/div/div/div[3]/div[3]/div[4]/div[2]/div/div[5]/div/div[2]/div/div[3]/div[2]')
            self.check_information_if(invoiceApplySn, invoiceApplySn_, "履行记录中发货申请单号", step)

    # 获取并校验导航信息（导航有两步）
    def navigation_two(self, driver, information_1, information_2, step, check_info_1, check_info_2):

        navigation_1 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div[1]/div[3]/div')
        self.check_information_if(information_1, navigation_1, check_info_1, step)
        navigation_2 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div[2]/div[3]/div')
        self.check_information_if(information_2, navigation_2, check_info_2, step)

    # 获取并校验导航信息（导航有三步）
    def navigation_three(self, driver, information_1, information_2, information_3, step,
                         check_info_1, check_info_2, check_info_3):

        navigation_1 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[1]/div[3]/div')
        self.check_information_if(information_1, navigation_1, check_info_1, step)
        navigation_2 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[2]/div[3]/div')
        self.check_information_if(information_2, navigation_2, check_info_2, step)
        navigation_3 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[3]/div[3]/div')
        self.check_information_if(information_3, navigation_3, check_info_3, step)

    # 获取并校验页面目录信息（导航有两步）
    def catalog_two(self, driver, information_1, information_2, step, check_info_1, check_info_2):
        catalog_1 = Cp().xpath_text_(xpath_front_1 + '/div/span[1]/span[1]/span')
        self.check_information_if(information_1, catalog_1, check_info_1, step)
        catalog_2 = Cp().xpath_text_(xpath_front_1 + '/div/span[2]/span[1]/span')

        self.check_information_if(information_2, catalog_2, check_info_2, step)

    # 获取并校验页面目录信息（导航有三步）
    def catalog_three(self, driver, information_1, information_2, information_3, step,
                      check_info_1, check_info_2, check_info_3):
        catalog_1 = Cp().xpath_text_(xpath_front_1 + '/div/span[1]/span[1]/span')
        self.check_information_if(information_1, catalog_1, check_info_1, step)
        catalog_2 = Cp().xpath_text_(xpath_front_1 + '/div/span[2]/span[1]//span')
        self.check_information_if(information_2, catalog_2, check_info_2, step)
        catalog_3 = Cp().xpath_text_(xpath_front_1 + '/div/span[3]/span[1]/span')
        self.check_information_if(information_3, catalog_3, check_info_3, step)

    # 获取并校验页面分类列表信息（列表有三类）
    def list_three(self, driver, information_1, information_2, information_3, step,
                   check_info_1, check_info_2, check_info_3):
        classification_1 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

    # 获取并校验页面分类列表信息（列表有四类）
    def list_four(self, driver, information_1, information_2, information_3, information_4, step,
                  check_info_1, check_info_2, check_info_3, check_info_4):
        classification_1 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

    # 获取并校验页面分类列表信息（列表有五类）
    def list_five(self, driver, information_1, information_2, information_3, information_4, information_5, step,
                  check_info_1, check_info_2, check_info_3, check_info_4, check_info_5):
        classification_1 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

        classification_5 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]')
        self.check_information_if(information_5, classification_5, check_info_5, step)

    # 获取并校验页面分类列表信息（列表有6类）
    def list_six(self, driver, information_1, information_2, information_3, information_4, information_5,
                 information_6, step, check_info_1, check_info_2, check_info_3, check_info_4, check_info_5,
                 check_info_6):
        classification_1 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[1]')
        self.check_information_if(information_1, classification_1, check_info_1, step)
        classification_2 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]')
        self.check_information_if(information_2, classification_2, check_info_2, step)

        classification_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]')
        self.check_information_if(information_3, classification_3, check_info_3, step)

        classification_4 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]')
        self.check_information_if(information_4, classification_4, check_info_4, step)

        classification_5 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]')
        self.check_information_if(information_5, classification_5, check_info_5, step)

        classification_6 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[6]')
        self.check_information_if(information_6, classification_6, check_info_6, step)

    def list_contents_seven(self, driver, step, information_1, information_2, information_3,
                            information_4, information_5, information_6, check_info_2, check_info_3,
                            check_info_4, check_info_5, check_info_6):
        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]')
        self.check_information_re(check_info_2, purchaser_name_1, information_1, step)
        agent_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_re(check_info_3, agent_name_1, information_2, step)
        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[4]')
        self.check_information_re(check_info_4, purchaser_name_1, information_3, step)
        price_sum_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        self.check_information_re(check_info_5, price_sum_1, information_4, step)
        a_time = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[6]/div')
        self.check_information_time(a_time, information_5, step)
        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[7]/div')
        self.check_information_if(check_info_6, state_1, information_6, step)

    # 获取并校验导航信息（导航有四步）
    def navigation_four(self, driver, information_1, information_2, information_3, information_4, step,
                        check_info_1, check_info_2, check_info_3, check_info_4):
        navigation_1 = Cp().xpath_text_(xpath_front + '/div/div/div/div/div/div/div/div[1]/div[3]/div')
        self.check_information_if(information_1, navigation_1, check_info_1, step)
        navigation_2 = Cp().xpath_text_(xpath_front + '/div/div/div/div/div/div/div/div[2]/div[3]/div')
        self.check_information_if(information_2, navigation_2, check_info_2, step)
        navigation_3 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[3]/div[3]/div')
        self.check_information_if(information_3, navigation_3, check_info_3, step)
        navigation_3 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/div/div/div/div[3]/div[3]/div')
        self.check_information_if(information_4, navigation_3, check_info_4, step)

    def list_contents_eight(self, driver, step, information_1, information_2, information_3,
                            information_4, information_5, information_6, information_7, check_info_2, check_info_3,
                            check_info_4, check_info_5, check_info_6, check_info_7):
        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[2]')
        self.check_information_re(check_info_2, purchaser_name_1, information_1, step)
        agent_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_re(check_info_3, agent_name_1, information_2, step)
        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[4]')
        self.check_information_re(check_info_4, purchaser_name_1, information_3, step)
        type_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[5]/div')
        self.check_information_if(check_info_7, type_1, information_7, step)
        price_sum_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[6]')
        self.check_information_re(check_info_5, price_sum_1, information_4, step)
        a_time = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[7]/div')
        self.check_information_time(a_time, information_5, step)
        state_1 = Cp().xpath_text_(
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

        price_single_1 = gl.get_value('price_single_1')
        price_sum_check_all_1 = gl.get_value('price_sum_check_all_1')
        price_sum_check_all_2 = gl.get_value('price_sum_check_all_2')
        price_many_2 = gl.get_value('price_many_2')
        apply_number = gl.get_value('apply_number')

        x = 2
        purchaser_name_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (39 + x))
        print(purchaser_name_1)
        self.check_information_if(purchaser_name, purchaser_name_1, "合同内容中采购（甲）方公司名称", step)
        purchaser_926_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (43 + x))
        self.check_information_if(purchaser_926, purchaser_926_1, "合同内容中采购（甲）方公司926链号", step)
        purchaser_contacts_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (47 + x))
        self.check_information_if('东方联系人', purchaser_contacts_1, "合同内容中采购（甲）方联系人", step)
        purchaser_phone_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (50 + x))
        self.check_information_if('东方联系号码', purchaser_phone_1, "合同内容中采购（甲）方号码", step)
        purchaser_email_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (54 + x))
        self.check_information_if(purchaser_email, purchaser_email_1, "合同内容中采购（甲）方邮箱", step)
        purchaser_address_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (58 + x))
        self.check_information_if(purchaser_address, purchaser_address_1, "合同内容中采购（甲）方地址", step)
        purchaser_bank_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (62 + x))
        self.check_information_if(purchaser_bank, purchaser_bank_1, "合同内容中采购（甲）方开户行", step)
        purchaser_account_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (66 + x))
        self.check_information_if(purchaser_account, purchaser_account_1, "合同内容中采购（甲）方账号", step)

        agent_name_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (40 + x))
        self.check_information_if(agent_name, agent_name_1, "合同内容中代理（乙）方公司名称", step)
        agent_926_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (44 + x))
        self.check_information_if(agent_926, agent_926_1, "合同内容中代理（乙）方公司926链号", step)
        # agent_contacts_1 = Cp().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (48+x) ).text
        # self.check_information_if('天河联系人', agent_contacts_1, "合同内容中代理（乙）方联系人", step)
        agent_phone_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (51 + x))
        self.check_information_if('18823772926', agent_phone_1, "合同内容中代理（乙）方号码", step)
        agent_email_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (55 + x))
        self.check_information_if('926@926.net.cn', agent_email_1, "合同内容中代理（乙）方邮箱", step)
        # agent_address_1 = Cp().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (59+x) ).text
        # self.check_information_if(agent_address, agent_address_1, "合同内容中代理（乙）方地址", step)
        agent_bank_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (63 + x))
        self.check_information_if('招商银行股份有限公司深圳科发支行', agent_bank_1, "合同内容中代理（乙）方开户行", step)
        agent_account_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (67 + x))
        self.check_information_if('755940017210601', agent_account_1, "合同内容中代理（乙）方账号", step)

        supplier_name_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (41 + x))
        self.check_information_if(supplier_name, supplier_name_1, "合同内容中销售（丙）方公司名称", step)
        supplier_926_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (45 + x))
        self.check_information_if(supplier_926, supplier_926_1, "合同内容中销售（丙）方公司926链号", step)
        supplier_contacts_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (48 + x))
        self.check_information_if('天河联系人', supplier_contacts_1, "合同内容中销售（丙）方联系人", step)
        supplier_phone_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (52 + x))
        self.check_information_if('天河联系号码', supplier_phone_1, "合同内容中销售（丙）方号码", step)
        supplier_email_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (56 + x))
        self.check_information_if(supplier_email, supplier_email_1, "合同内容中销售（丙）方邮箱", step)
        supplier_address_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (60 + x))
        self.check_information_re(supplier_address_1, supplier_address, "合同内容中销售（丙）方地址", step)
        supplier_bank_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (64 + x))
        self.check_information_if(supplier_bank, supplier_bank_1, "合同内容中销售（丙）方开户行", step)
        supplier_account_1 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (68 + x))
        self.check_information_if(supplier_account, supplier_account_1, "合同内容中销售（丙）方账号", step)

        contractnumber = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (1))

        number1 = gl.get_value('number1')
        number2 = gl.get_value('number2')
        price1 = gl.get_value('price1')
        price2 = gl.get_value('price2')
        amount_1= gl.get_value('amount_1')
        amount_2 = gl.get_value('amount_2')
        total_Amount = gl.get_value('total_Amount')
        goods_name = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (77 + x))
        self.check_information_if("接线盒盖毛坯", goods_name, "合同内容中一类商品名称", step)

        # specifications = Cp().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]'% (78+x) ).text
        # self.check_information_if("", specifications, "合同内容中商品规格", step)

        number = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (78 + x))
        self.check_information_if("%s(件)" % number1, number, "合同内容中一类商品数量", step)

        unit_price = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (79 + x))
        self.check_information_if(str(price1), unit_price, "合同内容中一类商品单价", step)

        total_price = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (80 + x))
        self.check_information_if(str(amount_1), total_price, "合同内容中一类商品总价", step)

        goods_name = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (82 + x))
        self.check_information_if("接线盒盖", goods_name, "合同内容中二类商品名称", step)

        specifications = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (83 + x))
        self.check_information_if("TF", specifications, "二类合同内容中二类商品规格", step)

        number222 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (84 + x))
        self.check_information_if("%s(件)" % number2, number222, "合同内容中二类商品数量", step)

        unit_price2 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (85 + x))
        self.check_information_if(str(price2), unit_price2, "合同内容中二类商品单价", step)

        total_price2 = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (86 + x))
        self.check_information_if(str(amount_2), total_price2, "合同内容中二类商品总价", step)

        full_price = Cp().xpath_text_(
            '//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (100))
        self.check_information_if(str(total_Amount), full_price, "合同内容中商品总价", step)

        zufs = Cp().xpath_text_('//div[@class="react-pdf__Document center"]/div[1]/div[1]/span[%s]' % (25 + x))
        self.check_information_re("货到开银行承兑汇票", zufs, "合同内容中支付方式", step)

        # 释放iframe
        # driver.switch_to_default_content()

        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[3]', "点击查看申请信息",
                          step, "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_2, "采购（甲）方公司名称", step)

        purchaser_926_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]')
        self.check_information_if(purchaser_926, purchaser_926_2, "采购（甲）方公司926链号", step)
        purchaser_email_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[3]/div/div[2]')
        self.check_information_if(purchaser_email, purchaser_email_2, "采购（甲）方邮箱", step)
        purchaser_contacts_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[4]/div/div[2]')
        self.check_information_if('东方联系人', purchaser_contacts_2, "采购（甲）方联系人", step)
        purchaser_phone_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[2]/div[5]/div/div[2]')
        self.check_information_if('东方联系号码', purchaser_phone_2, "采购（甲）方联系号码", step)

        agent_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[2]')
        self.check_information_if(agent_name, agent_name_2, "代理（乙）方公司名称", step)
        agent_926_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[2]/div/div[2]')
        self.check_information_if(agent_926, agent_926_2, "代理（乙）方公司名称", step)
        agent_email_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[3]/div/div[2]')
        self.check_information_if(agent_email_1, agent_email_2, "代理（乙）方邮箱", step)

        # agent_contacts_2 = Cp().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[4]/div/div[2]')
        # self.check_information_if('朱丹', agent_contacts_2, "代理（乙）方联系人", step)

        agent_phone = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[3]/div[5]/div/div[2]')
        self.check_information_if(agent_phone_1, agent_phone, "代理（乙）方联系电话", step)

        supplier_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[1]/div/div[2]')
        self.check_information_if("(发起方)%s" % supplier_name, supplier_name_2, "销售方（丙）方公司名称", step)

        supplier_926_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[2]/div/div[2]')
        self.check_information_if(supplier_926, supplier_926_2, "销售方（丙）方公司926链号", step)

        supplier_email_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[3]/div/div[2]')
        self.check_information_if(supplier_email, supplier_email_2, "销售方（丙）方邮箱", step)

        supplier_contacts_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[4]/div/div[2]')
        self.check_information_if('天河联系人', supplier_contacts_2, "销售方（丙）方联系人", step)

        supplier_phone_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[1]/div[4]/div[5]/div/div[2]')
        self.check_information_if('天河联系号码', supplier_phone_2, "销售方（丙）方电话", step)

        Cp().slide_("500")
        picture_1 = Cp().xpath_href_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]'
                          '/div[2]/div[1]/span/div[1]/div/div/span/a[1]')

        self.check_information_re("625b4822e90d95601e40dcdf7335b7ac.jpg", picture_1, "合同图片信息", step)

        protocolSignTimeStr = gl.get_value('protocolSignTimeStr')
        protocolNumber = gl.get_value('protocolNumber')
        deliveryTypeName = gl.get_value('deliveryTypeName')
        secondPaymentTypeName = gl.get_value('secondPaymentTypeName')
        receiptTerm = gl.get_value('receiptTerm')
        secondAcceptanceDraftTimeTypeName = gl.get_value('secondAcceptanceDraftTimeTypeName')
        thirdReceiptTimeTypeName = gl.get_value('thirdReceiptTimeTypeName')
        thirdReceiptTimeNum = gl.get_value('thirdReceiptTimeNum')
        contract_mark = gl.get_value('contract_mark')
        contract_mark = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[2]/div[2]/div[2]/div/div[2]')
        self.check_information_if("62284844935", contract_mark, "原始合同编号", step)
        gl.set_value('contract_mark', contract_mark)
        # price_sum = Cp().xpath_text_(
        #     xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div/div[2]')
        # self.check_information_re(total_Amount, price_sum, "商品总价", step)

        protocolSignTimeStr = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[1]/div')
        self.check_information_re('20', protocolSignTimeStr, "协议签订日期", step)
        protocolNumber = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[2]/div/div[2]')
        self.check_information_re('xybh', protocolNumber, "协议编号", step)
        deliveryTypeName = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[3]/div/div[2]')
        self.check_information_re('甲方自提', deliveryTypeName, "交货方式", step)
        secondPaymentTypeName = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[4]/div/div[2]')
        self.check_information_re('银行承兑汇票', secondPaymentTypeName, "乙方付款方式:", step)
        receiptTerm = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[1]/div/div[2]')
        self.check_information_re('5个月', receiptTerm, "汇票期限:", step)
        secondAcceptanceDraftTimeTypeName = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[2]/div/div[2]')
        self.check_information_re('货到开银行承兑汇票', secondAcceptanceDraftTimeTypeName, "乙方开承兑汇票时间:", step)
        thirdReceiptTimeTypeName = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[3]/div/div[2]')
        self.check_information_re('乙方开银行承兑汇票前', thirdReceiptTimeTypeName, "*丙方开发票时间:", step)
        thirdReceiptTimeNum = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[3]/div[2]/div[5]/div[4]/div/div[2]')
        self.check_information_re('150天', thirdReceiptTimeNum, "乙方开银行承兑汇票前:", step)
        Cp().slide_('750')
        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[1]/div[4]/div/div[2]')
        self.check_information_re(str(total_Amount), price_sum, "商品总价", step)

        cooperation_time = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[2]')
        self.check_information_time(cooperation_time, "发起方提交审签时间", step)
        contractnumber_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[3]/div[2]/div[2]/div[2]/div[3]/div/div[2]')
        self.check_information_if(contractnumber, contractnumber_2, "合同编号", step)

        Cp().slide_("0")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[2]',"点击查看附件信息",
                                          step, "云平台‘采购方’", sys._getframe().f_lineno)
        picture_2 = Cp().xpath_href_(
            xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[1]/span'
                          '/div[1]/div/div/span/a[1]')
        self.check_information_re(picture_1, picture_2, "原始合同图片", step)

        contract_mark_1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[2]/div/div[2]')
        self.check_information_if("62284844935", contract_mark_1, "原始合同编号", step)
        settlement_date = gl.get_value('settlement_date')
        settlement = Cp().xpath_text_(
            xpath_front + '/div/div/div[3]/div[3]/div[2]/div[2]/div[2]/div[3]/div/div[2]')
        self.check_information_if(settlement_date, settlement, "结算方式", step)

    def login(self):
        driver = self.driver
        start_url = self.start_url
        driver.get(start_url)
        Cp().name_click_("ant-menu-item", "点击密码登录", "登录", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().id_clear_("手机号")
        if re.findall('test', start_url):
            Cp().id_send_("手机号", "18474793371")  # 测试
            Cp().is_toast_exist("输入正确的手机号", "登录", "云平台‘采购方’", sys._getframe().f_lineno)
        elif re.findall('10.', start_url):  # 开发
            Cp().id_send_("手机号", "18474793371")  # 开发
            Cp().is_toast_exist("输入正确的手机号", "登录", "云平台‘采购方’", sys._getframe().f_lineno)
        elif re.findall('pre', start_url):  # 预生产
            Cp().id_send_("手机号", "18474793371")  # 生产测试账号 18390552449   生产通用账号 18474793371
            Cp().is_toast_exist("输入正确的手机号", "登录", "云平台‘采购方’", sys._getframe().f_lineno)
        else:  # 生产
            Cp().id_send_("手机号", "18390552449")  # 生产测试账号 18390552449
            Cp().is_toast_exist("输入正确的手机号", "登录", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().id_clear_("密码")
        Cp().id_send_("密码", "123456")
        Cp().is_toast_exist("输入正确的密码", "登录", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().xpath_click_("//button[@class='ant-btn login-form-button ant-btn-primary']", "点击登录", "登录",
                                          "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_('//*[@id="1$Menu"]/li', "点击进入企业实名认证", "发起合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        purchaser_name = Cp().xpath_text_('//*[@id="8126-753004"]', "获取企业名称", "发起合同", "云平台‘采购方’",
                                                          sys._getframe().f_lineno)

        Cp().text_click_("云平台", "进入926云平台", "登录", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        # catalog = Cp().xpath_text_('//*[@id="root"]/div/section/div[2]/div/div/div/div/div/div/ul/li[1]/div/span/span', sys._getframe().f_lineno)
        # self.check_information_if("合同管理", catalog, "成功进入云平台", "进入926云平台")
        gl.get_value('purchaser_name',purchaser_name) # 供方企业名
        Cp().xpath_click_('//*[@id="10$Menu"]/li[1]', "点击进入云平台认证", "获取企业信息", "云平台‘采购方’",
                          sys._getframe().f_lineno)
        Cp().xpath_click_(xpath_front + '/div/div/div/div/div/div/div/div/table/tbody/tr[1]/td[4]/button',
                          "点击进入云平台认证详情", "获取企业信息", "云平台‘采购方’",
                          sys._getframe().f_lineno)
        Cp().slide_("800")
        purchaser_address = Cp().xpath_text_(
            '//*[@id="0地址"]', "获取采购方地址", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        purchaser_email = Cp().xpath_text_(
            '//*[@id="4指定邮箱"]', "获取采购方邮箱 ", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        Cp().slide_("2500")
        purchaser_bank = Cp().xpath_text_(
            '//*[@id="3开户银行（含支行）"]', "获取采购方4开户银行 ", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        purchaser_account = Cp().xpath_text_(
            '//*[@id="1企业银行账号"]', "获取银行账号 ", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        Cp().is_toast_exist("获取企业信息完毕", "获取企业信息", "云平台‘发起方’", sys._getframe().f_lineno)
        gl.set_value('purchaser_name', purchaser_name)
        gl.set_value('purchaser_address', purchaser_address)  # 获取采购方地址
        gl.set_value('purchaser_email', purchaser_email)  # 获取采购方邮箱
        gl.set_value('purchaser_bank', purchaser_bank)  # 获取采购方开户银行
        gl.set_value('purchaser_account', purchaser_account)  # 获取采购方银行账号
        print(purchaser_name,purchaser_address,purchaser_email,purchaser_bank,purchaser_account)

    def refuse_entrust(self):  # 合作方拒绝委托
        driver = Cp().driver
        print("*****合作方拒绝委托*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="0$Menu"]/li[1]', "点击进入合同签审", "拒绝前已收到的合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                                          "点击进入我方待审签",
                                          "拒绝前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)

        apply_number = gl.get_value('apply_number')
        time.sleep(1)
        apply_number_2 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘合作方待审批’创建编号", "拒绝前已收到的合同")

        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name = gl.get_value('purchaser_name')  # bing
        total_Amount = gl.get_value('total_Amount')
        self.list_contents_seven(driver, '拒绝前已收到的合同', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点",
                                 purchaser_name, agent_name, purchaser_name,
                                 '￥%s'%total_Amount, '采购方待审签')

        Cp().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[8]'
                                                        '/div/a/button', "点击查看", "拒绝前已收到的合同",
                                          "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "查看发起后的合同信息", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方审签", "受托方审签", "拒绝前已收到的合同",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")
        Cp().slide_("100")
        self.contract_content(driver, "拒绝前已收到的合同")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击操作记录",
                                          "拒绝前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        supplier_name = gl.get_value('supplier_name')
        start_url = self.start_url
        if re.findall("test", start_url):
            self.Operation_record(driver, "发起方提交合同申请", "天河软件有限公司 18216482019_s", "拒绝前已收到的合同",
                                  "查看我方签审后的操作状态", "查看我方签审后的操作时间", "我方签审后的操作者信息", "4")
        else:
            self.Operation_record(driver, "发起方提交合同申请", "%s 18216482019_s"%supplier_name, "拒绝前已收到的合同",
                                  "查看我方签审后的操作状态", "查看我方签审后的操作时间", "我方签审后的操作者信息", "4")
        Cp().xpath_click_('//*[@id="RightRouteDiv"]/div/div/div/div[2]/div/div/div[2]/button[1]', "点击拒绝", "拒绝前已收到的合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        Cp().xpath_click_('//div[@class="ant-modal-body"]/div/div[2]/div/button[1]',
                                          "选择拒绝标签1", "拒绝前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)

        Cp().xpath_click_('//div[@class="ant-modal-body"]/div/div[2]/div/button[4]', "选择拒绝标签2", "拒绝前已收到的合同","云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_('//div[@class="ant-modal-body"]/div/div[3]/textarea', "点击拒绝理由",
                                          "拒绝前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().xpath_send_('//textarea[@class="ant-input"]', "fkl")
        Cp().is_toast_exist("输入拒绝理由", "拒绝前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().xpath_click_('//div[@class="ant-modal-body"]/div/div[4]/button', "点击确认",
                                          "拒绝前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认",
                                          "拒绝前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        print("*****查看合作方拒绝后委托单信息*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="0$Menu"]/li[2]', "点击进入合同处理", "查看被拒绝的合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        Cp().xpath_click_('//div[@class="ant-tabs-nav ant-tabs-nav-animated"]/div/div[3]', "点击进入合作方待审签",
                                          "查看被拒绝的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        apply_number_2 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘合作方待审批’创建编号", "查看被拒绝的合同")

        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)方企业名
        total_Amount = gl.get_value('total_Amount')
        self.list_contents_eight(driver, '查看被拒绝的合同', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点", '合同类别',
                                 purchaser_name, agent_name, purchaser_name,
                                 '￥%s'%total_Amount, '采购方拒绝', '代理销售')

        Cp().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                                        '/div/div/table/tbody/tr[1]/td[9]/div/a/button', "点击查看",
                                          "查看被拒绝的合同",
                                          "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同处理", "合同详情", "查看被拒绝的合同", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方拒绝", "受托方审签", "查看被拒绝的合同",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")
        # 拒绝理由、拒绝详情
        cooperation_refuse_reason_ = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div[1]')
        self.check_information_if("相关标签:其他 金额部分", cooperation_refuse_reason_, "拒绝理由", "查看被拒绝的合同")
        cooperation_refuse_details_ = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div[2]')
        self.check_information_if("详细原因:fkl", cooperation_refuse_details_, "拒绝详情", "查看被拒绝的合同")
        cooperation_refuse_details = cooperation_refuse_details_[5:]
        cooperation_refuse_reason = cooperation_refuse_reason_[5:]
        gl.set_value('cooperation_refuse_details', cooperation_refuse_details)
        gl.set_value('cooperation_refuse_reason', cooperation_refuse_reason)

        Cp().slide_("100")
        self.contract_content(driver, "被我（合作）方拒绝后的合同信息")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击操作记录",
                                          "被我（合作）方拒绝后的合同信息", "云平台‘采购方’", sys._getframe().f_lineno)
        start_url = self.start_url
        if re.findall("test", start_url):
            self.Operation_record_refuse(driver, "合作方拒绝合同申请", "广州新东方分公司 18474793371_s", "被我（合作）方拒绝后的合同信息",
                                         "查看被我方拒绝后的操作状态", "查看被我方拒绝后的操作时间", "查看被我方拒绝后的操作者信息",
                                         "查看被我方拒绝后的理由", "查看被我方拒绝后的详情")
        else:
            self.Operation_record_refuse(driver, "合作方拒绝合同申请", "一广州新东方企业注册名字 18390552449_s", "被我（合作）方拒绝后的合同信息",
                                         "查看被我方拒绝后的操作状态", "查看被我方拒绝后的操作时间", "查看被我方拒绝后的操作者信息",
                                         "查看被我方拒绝后的理由", "查看被我方拒绝后的详情")

    def see_cooperation_refuse(self):  # 查看代理方拒绝的委托
        driver = self.driver
        print("*****查看代理方拒绝后的委托单信息*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="0$Menu"]/li[2]', "点击进入合同处理", "查看被代理方拒绝的合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        Cp().xpath_click_('//div[@class="ant-tabs-nav ant-tabs-nav-animated"]/div/div[3]', "点击进入合作方待处理",
                                          "查看被代理方拒绝的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        apply_number = gl.get_value('apply_number')
        apply_number_2 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘合作方待审批’创建编号", "查看被代理方拒绝的合同")

        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)方企业名
        total_Amount = gl.get_value('total_Amount')
        self.list_contents_eight(driver, '查看被代理方拒绝的合同', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点", '合同类别',
                                 purchaser_name, agent_name, purchaser_name,
                                 '￥%s'%total_Amount, '受托方拒绝', '代理销售')

        Cp().xpath_click_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[9]/div/a/button', "点击查看",
            "查看被代理方拒绝的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同处理", "合同详情", "查看被代理方拒绝的合同", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方已通过", "受托方拒绝", "查看被代理方拒绝的合同",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")
        # 拒绝理由、拒绝详情
        cooperation_refuse_reason_ = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div[1]')
        self.check_information_if("相关标签:其他 金额部分", cooperation_refuse_reason_, "拒绝理由", "查看被代理方拒绝的合同")
        cooperation_refuse_details_ = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/div[2]/div[2]')
        self.check_information_if("详细原因:fkl", cooperation_refuse_details_, "拒绝详情", "查看被代理方拒绝的合同")
        cooperation_refuse_details = cooperation_refuse_details_[5:]
        cooperation_refuse_reason = cooperation_refuse_reason_[5:]
        gl.set_value('cooperation_refuse_details', cooperation_refuse_details)
        gl.set_value('cooperation_refuse_reason', cooperation_refuse_reason)

        Cp().slide_("100")
        self.contract_content(driver, "查看被代理方拒绝的合同")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击操作记录",
                                          "查看被代理方拒绝的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        start_url = self.start_url
        if re.findall("test", start_url):
            self.Operation_record_refuse(driver, "合作方拒绝合同申请", "广州新东方分公司 18474793371_s", "查看被代理方拒绝的合同",
                                         "查看被代理方拒绝后的操作状态", "查看被代理方拒绝后的操作时间", "查看被代理方拒绝后的操作者信息",
                                         "查看被代理方拒绝后的理由", "查看被代理方拒绝后的详情")
        else:
            self.Operation_record_refuse(driver, "合作方拒绝合同申请", "一广州新东方企业注册名字 18390552449_s", "查看被代理方拒绝的合同",
                                         "查看被代理方拒绝后的操作状态", "查看被代理方拒绝后的操作时间", "查看被代理方拒绝后的操作者信息",
                                         "查看被代理方拒绝后的理由", "查看被代理方拒绝后的详情")

    def cooperation_agree_contract(self):  # 合作方同意委托
        driver = Cp().driver
        print("*****查看审签前已收到的合同*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="0$Menu"]/li[1]', "点击进入合同签审", "审签前已收到的合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                                          "点击进入我方待审签",
                                          "审签前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)

        Cp().xpath_click_(xpath_front + '/div/div[2]/div[2]/div/div/div'
                                                        '/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
                                          "审签前已收到的合同",
                                          "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "审签前已收到的合同", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方审签", "受托方审签", "审签前已收到的合同",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")
        Cp().slide_("100")
        self.contract_content(driver, "审签前已收到的合同")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击操作记录",
                                          "审签前已收到的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        start_url = self.start_url
        supplier_name = gl.get_value('supplier_name')
        if re.findall("test", start_url):
            self.Operation_record(driver, "发起方提交合同申请", "天河软件有限公司 18216482019_s", "审签前已收到的合同",
                                  "查看我方签审后的操作状态", "查看我方签审后的操作时间", "我方签审后的操作者信息", "4")
        else:
            self.Operation_record(driver, "发起方提交合同申请", "%s 18216482019_s"%supplier_name, "审签前已收到的合同",
                                  "查看我方签审后的操作状态", "查看我方签审后的操作时间", "我方签审后的操作者信息", "4")
        print("****合作方签审合同****")
        Cp().xpath_click_(xpath_front + '/div/div/div[2]/button[2]', "点击确认审签", "同意已收到的合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        Cp().xpath_keys_("//input[@class='ant-checkbox-input']", "合同已阅读", "同意已收到的合同", "云平台‘采购方’",
                                         sys._getframe().f_lineno)
        Cp().xpath_keys_('//div[@class="ant-modal-body"]/div/button', "确认审签", "同意已收到的合同",
                                         "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_send_('//div[@class="ant-col ant-col-17"]/input', "48152")
        Cp().is_toast_exist("输入验证码", "签审合同", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().xpath_keys_('//div[@class="ant-modal-footer"]/button[2]', "点击确定",
                          "签审合同", "云平台‘采购方’", sys._getframe().f_lineno)
        print("****查看合作方签审后合同信息****")
        time.sleep(2)
        Cp().xpath_click_(xpath_front_1 + '/div/span[2]/span[1]/a/span', "点击目录中的'合同签审'-进入合同签审列表",
                                          "同意已收到的合同",
                                          "云平台‘采购方’", sys._getframe().f_lineno)
        self.catalog_two(driver, "合同管理", "合同审签列表", "被我（合作）方签审后的合同信息", "合同详情一级目录", "合同详情二级目录", )
        apply_number = gl.get_value('apply_number')
        apply_number_2 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(apply_number, apply_number_2, "‘合作方待审批’创建编号", "被我（合作）方签审后的合同信息")

        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')  # 采购
        purchaser_name = gl.get_value('purchaser_name')  # bing
        self.list_contents_seven(driver, '被我（合作）方签审后的合同信息', "列表中采购方名称", "列表中代理方名称",
                                 "列表中销售方名称", "列表中合同金额", "列表中提交日期", "列表中流程节点",
                                 purchaser_name, agent_name, purchaser_name,
                                 '￥10,000.00', '受托方待审签')

        Cp().xpath_click_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
            "被我（合作）方签审后的合同信息", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "合同管理", "合同审签", "合同详情", "被我（合作）方签审后的合同信息", "合同详情一级目录", "合同详情二级目录", "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方已审签", "受托方审签", "被我（合作）方签审后的合同信息",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")
        Cp().slide_("100")
        self.contract_content(driver, "被我（合作）方签审后的合同信息")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击操作记录",
                                          "被我（合作）方签审后的合同信息", "云平台‘采购方’", sys._getframe().f_lineno)
        start_url = self.start_url
        if re.findall("test", start_url):
            self.Operation_record(driver, "合作方同意合同申请", "广州新东方分公司 18474793371_s", "被我（合作）方签审后的合同信息",
                                  "查看被我方签审后的操作状态", "查看被我方签审后的操作时间", "查看被我方签审后的操作人员", "4")
        else:
            self.Operation_record(driver, "合作方同意合同申请", "一广州新东方企业注册名字 18390552449_s", "被我（合作）方签审后的合同信息",
                                  "查看被我方签审后的操作状态", "查看被我方签审后的操作时间", "查看被我方签审后的操作人员", "4")

    def see_cooperation_adopt(self):
        print("*****校验代理方通过审批后的合同信息****")
        driver = self.driver
        Cp().xpath_click_('//*[@id="0$Menu"]/li[3]', "进入合同签订", "校验代理方通过审批后的合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
        self.catalog_two(driver, "合同管理", "合同签订列表", "校验代理方通过审批后的合同", "合同审签列表页一级目录", "合同审签列表页二级目录")
        self.list_three(driver, "全部", "代理采购", "代理销售", "校验代理方通过审批后的合同", "合同签审-全部列表",
                        "合同签审-我方待审批列表", "合同签审-合作方待审批列表")

        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                                          "进入代理销售",
                                          "校验代理方通过审批后的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        contractnumber_number_3 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(contractnumber, contractnumber_number_3, "校验合同编号是否一致", "校验代理方通过审批后的合同")

        a_time_3 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[6]')
        self.check_information_time(a_time_3, "‘校验提交时间是否一致", "校验代理方通过审批后的合同")
        state_3 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[7]/div')
        self.check_information_if("受托方已通过", state_3, "校验状态", "校验代理方通过审批后的合同")
        Cp().xpath_click_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
            "校验代理方通过审批后的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同签订", "合同详情", "校验代理方通过审批后的合同", "合同详情一级目录", "合同详情二级目录",
                           "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方已审签", "受托方已审签", "校验代理方通过审批后的合同",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cp().slide_("100")
        self.contract_content(driver, "校验代理方通过审批后的合同")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击操作记录",
                                          "校验代理方通过审批后的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        if re.findall('test', self.start_url):
            self.Operation_record(driver, "代理商已审签", '深圳市九二六供应链网络有限公司代采分公司1 13245678999_s', "校验代理方通过审批后的合同",
                                  "查看代理方签审后的操作状态", "查看代理方签审后的操作时间", "查看代理方签审后的操作者信息", "4")
        else:
            self.Operation_record(driver, "代理商已审签", '深圳市九二六供应链网络有限公司 18373847538_s', "校验代理方通过审批后的合同",
                                  "查看代理方签审后的操作状态", "查看代理方签审后的操作时间", "查看代理方签审后的操作者信息", "4")
        print("*****查看代理方签审后云票额度信息*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入额度管理首页", "查看代理方签审后云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)

        totalCreditQuota_purchaser = gl.get_value('totalCreditQuota_purchaser')  # 甲 采购总授信云票"
        totalCirculationQuota_purchaser = gl.get_value('totalCirculationQuota_purchaser')  # 甲 采购总流转云票"
        # totalQuota_purchaser = gl.get_value('totalQuota_purchaser')  # 甲 总云票 （授信+流转）
        totalOccupyCreditQuota_purchaser = gl.get_value('totalOccupyCreditQuota_purchaser')  # jia 已占用授信云票
        totalOccupyCirculationQuota_purchaser = gl.get_value('totalOccupyCirculationQuota_purchaser')  # jia 已占用流转云票
        # totalFrozenCreditQuota_purchaser = gl.get_value('totalFrozenCreditQuota_purchaser')  # jia 获取已冻结授信云票
        # totalFrozenCirculationQuota_purchaser = gl.get_value('totalFrozenCirculationQuota_purchaser')  # jia 已冻结流转云票
        totalOccupancyCreditQuota_purchaser = gl.get_value('totalOccupancyCreditQuota_purchaser')  # jia 可用总授信(总-已用)
        totalOccupancyCirculationQuota_purchaser = gl.get_value(
            'totalOccupancyCirculationQuota_purchaser')  # jia 余总流转(总-已用

        estimateReduceQuota_purchaser = Cp().xpath_text_(xpath_front + '/div/div[3]/div/div[2]/div[2]')
        Cp().is_toast_exist("获取预计减少云票", "查看代理方签审后云票额度信息", "云平台‘采购方’", sys._getframe().f_lineno)
        surplusAvailableTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupancyCreditQuota_purchaser, surplusAvailableTotalCreditQuota_1, "可用授信",
                                  "查看代理方签审后云票额度信息")
        occupyTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[1]/p[2]')
        self.check_information_re(totalOccupyCreditQuota_purchaser, occupyTotalCreditQuota_1, "已用授信", "查看代理方签审后云票额度信息")
        totalCreditQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[1]/div[3]')
        self.check_information_re(totalCreditQuota_purchaser, totalCreditQuota_1, "总授信", "查看代理方签审后云票额度信息")

        estimateAddQuota_purchaser = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div[1]/div[2]')  # 预增云票
        Cp().is_toast_exist("获取预增云票", "查看代理方签审后云票额度信息", "云平台‘采购方’", sys._getframe().f_lineno)

        totalCirculationQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[2]/div[3]')
        totalCirculationQuota_1 = re_sub_(totalCirculationQuota_1)
        # print('totalCirculationQuota_purchase:%s', totalCirculationQuota_purchaser)
        # print('totalCirculationQuota_1:%s', totalCirculationQuota_1)
        self.check_information_re(totalCirculationQuota_purchaser, totalCirculationQuota_1, "总流转", "查看代理方签审后云票额度信息")

        surplusTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[4]')
        surplusTotalCirculationQuota_1 = re_sub_(surplusTotalCirculationQuota_1)
        self.check_information_re(totalOccupancyCirculationQuota_purchaser, surplusTotalCirculationQuota_1,
                                  "剩余流转", "查看代理方签审后云票额度信息")
        surplusAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        surplusAvailableTotalCirculationQuota_check = int(surplusTotalCirculationQuota_1) * 0.8
        self.check_information_re(surplusAvailableTotalCirculationQuota_1,
                                  str(surplusAvailableTotalCirculationQuota_check),
                                  "可用流转", "查看代理方签审后云票额度信息")
        occupyAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupyCirculationQuota_purchaser, occupyAvailableTotalCirculationQuota_1,
                                  "已用流转", "查看代理方签审后云票额度信息")
        loanAbilityQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[3]/p[2]')
        self.check_information_re(totalCirculationQuota_purchaser, loanAbilityQuota_1, "可贷现", "查看代理方签审后云票额度信息")

        gl.set_value("estimateAddQuota_purchaser", estimateAddQuota_purchaser)  # 预增云票
        gl.set_value("estimateReduceQuota_purchaser", estimateReduceQuota_purchaser)  # 预计减少云票

    def refuse_delivery_application(self):  # 代采方拒绝发货申请
        driver = self.driver
        print("*****代采方查看拒绝前云票额度信息*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入额度管理首页", "代采方查看拒绝申请前云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        total_Amount = gl.get_value('total_Amount')  # 货品总价
        estimateReduceQuota_purchaser = gl.get_value("estimateReduceQuota_purchaser")  # 预计减少云票
        totalCreditQuota_purchaser = gl.get_value('totalCreditQuota_purchaser')  # 甲 采购总授信云票"
        totalCirculationQuota_purchaser = gl.get_value('totalCirculationQuota_purchaser')  # 甲 采购总流转云票"
        totalOccupyCreditQuota_purchaser = gl.get_value('totalOccupyCreditQuota_purchaser')  # jia 已占用授信云票
        totalOccupyCirculationQuota_purchaser = gl.get_value('totalOccupyCirculationQuota_purchaser')  # jia 已占用流转云票
        totalOccupancyCreditQuota_purchaser = gl.get_value('totalOccupancyCreditQuota_purchaser')  # jia 可用总授信(总-已用)
        totalOccupancyCirculationQuota_purchaser = gl.get_value(
            'totalOccupancyCirculationQuota_purchaser')  # jia 余总流转(总-已用
        print(total_Amount)
        print(estimateReduceQuota_purchaser)
        estimateReduceQuota_purchaser = re_sub_(estimateReduceQuota_purchaser)
        estimateReduceQuota_check = int(total_Amount) + int(estimateReduceQuota_purchaser)
        # estimateReduceQuota = 1000
        estimateReduceQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[3]/div/div[2]/div[2]')
        estimateReduceQuota_1 = re_sub_('estimateReduceQuota_1')
        self.check_information_if(str(estimateReduceQuota_check), estimateReduceQuota_1, "预计减少额度", "代采方查看拒绝申请前云票额度信息")
        surplusAvailableTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupancyCreditQuota_purchaser, surplusAvailableTotalCreditQuota_1, "可用授信",
                                  "代采方查看拒绝申请前云票额度信息")
        occupyTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[1]/p[2]')
        self.check_information_re(totalOccupyCreditQuota_purchaser, occupyTotalCreditQuota_1, "已用授信",
                                  "代采方查看拒绝申请前云票额度信息")
        totalCreditQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[1]/div[3]')
        self.check_information_re(totalCreditQuota_purchaser, totalCreditQuota_1, "总授信", "代采方查看拒绝申请前云票额度信息")

        estimateAddQuota = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div[1]/div[2]')  # 预增云票
        Cp().is_toast_exist("获取预增云票", "代采方查看拒绝申请前云票额度信息", "云平台‘采购方’", sys._getframe().f_lineno)

        totalCirculationQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[2]/div[3]')
        totalCirculationQuota_1 = re_sub_(totalCirculationQuota_1)
        self.check_information_re(totalCirculationQuota_purchaser, totalCirculationQuota_1, "总流转", "代采方查看拒绝申请前云票额度信息")

        surplusTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[4]')
        surplusTotalCirculationQuota_1 = re_sub_(surplusTotalCirculationQuota_1)
        self.check_information_re(totalOccupancyCirculationQuota_purchaser, surplusTotalCirculationQuota_1,
                                  "剩余流转", "代采方查看拒绝申请前云票额度信息")
        surplusAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        surplusAvailableTotalCirculationQuota_check = int(surplusTotalCirculationQuota_1) * 0.8
        self.check_information_re(str(surplusAvailableTotalCirculationQuota_check),
                                  surplusAvailableTotalCirculationQuota_1,
                                  "可用流转", "代采方查看拒绝申请前云票额度信息")
        occupyAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[1]/p[2]')
        self.check_information_re(totalOccupyCirculationQuota_purchaser, occupyAvailableTotalCirculationQuota_1,
                                  "已用流转", "代采方查看拒绝申请前云票额度信息")
        loanAbilityQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[3]/p[2]')
        totalOccupancyCirculationQuota_purchaser_check = int(totalOccupancyCirculationQuota_purchaser) * 0.5
        self.check_information_re(str(totalOccupancyCirculationQuota_purchaser_check), loanAbilityQuota_1, "可贷现",
                                  "代采方查看拒绝申请前云票额度信息")

        time.sleep(1)
        Cp().xpath_click_('//*[@id="3$Menu"]/li[6]', "点击进入预计减少云票", "代采方查看拒绝申请前云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        estimateReduceQuota_1 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/span')
        estimateReduceQuota_1 = re_sub_(estimateReduceQuota_1)  # 显示为12,500.00 正则筛选
        estimateReduceQuota_purchaser_check = int(estimateReduceQuota_purchaser) + int(total_Amount)
        self.check_information_re(str(estimateReduceQuota_purchaser), estimateReduceQuota_1, "预计减少额度",
                                  "代采方查看拒绝申请前云票额度信息")
        invoiceApplySn = gl.get_value('invoiceApplySn')  # DF 发货单
        invoiceApplySn_0 = Cp().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_0, "发货申请单号", "代采方查看拒绝申请前云票额度信息")
        deliveryGoodTime_1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[3]/div')
        self.check_information_time(deliveryGoodTime_1, "发货申请提交时间", "代采方查看拒绝申请前云票额度信息")
        estimateChangeQuota_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[4]/span')
        estimateChangeQuota_2 = re_sub_(estimateChangeQuota_2)  # 显示为12,500.00 正则筛选
        self.check_information_re(str(total_Amount), estimateChangeQuota_2, "预计变化的云票", "代采方查看拒绝申请前云票额度信息")
        totalAmount_1 = Cp().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[5]/span')
        totalAmount_1 = re_sub_(totalAmount_1)  # 显示为12,500.00 正则筛选
        self.check_information_re(str(total_Amount), totalAmount_1, "发货单货品总价", "代采方查看拒绝申请前云票额度信息")

        print("*****代采方查看拒绝前发货申请信息*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入代采发货申请", "代采方拒绝发货申请", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        self.catalog_two(driver, "代采管理", "收货申请", "代采方拒绝发货申请", "发货申请列表页一级目录", "发货申请列表页二级目录")
        self.list_six(driver, "全部", "内部待同意", "代理方待审批", "代理方已通过", "内部已拒绝", "代理方已拒绝", "代采方拒绝发货申请", "代采管理-所有发货单列表",
                      "代采管理-客户待审批列表", "代采管理-代理方待审批列表", "代采管理-代理方已通过列表", "代采管理-客户未通过列表", "代采管理-代理方未通过列表")
        Cp().xpath_click_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击进入内部待同意", "代采方拒绝发货申请", "云平台‘采购方’",
            sys._getframe().f_lineno)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        invoiceApplySn_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看发货单信息", "代采方拒绝发货申请")

        purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)方企业名
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        receiving_party_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中发货单位", "代采方拒绝发货申请")

        agent_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "代采方拒绝发货申请")

        contract_sum = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum, "列表中发货金额", "代采方拒绝发货申请")
        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('内部待同意', state_1, "查看发货单信息", "发起发货申请")
        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击内部待同意-查看",
            "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "发货申请", "发货申请详情", "代采方拒绝发货申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 发起申请', '采购方 待审批', "代理方 待审核", "代采方拒绝发货申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name = gl.get_value('purchaser_name')  # bing
        purchaserName_2 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_2, "获取详情页中发货方名称", "代采方拒绝发货申请")

        purchaserName_page_1 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaserName_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代采方拒绝发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_6 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_6, "新页面中采购方企业名称信息", "代采方拒绝发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaserName_2 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_2, "获取详情页中收货方名称", "代采方拒绝发货申请")

        purchaserName_page_2 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaserName_page_2)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代采方拒绝发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_6 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_6, "新页面中销售方企业名称信息", "代理方查看销售出货后的出货信息")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)方电话
        purchaserPhone = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中发货方号码", "代采方拒绝发货申请")

        purchaser_address = gl.get_value('purchaser_address')
        purchaserAdress_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "发货地址-详情页", "代采方拒绝发货申请")
        purchaser_address = gl.get_value('purchaser_address')
        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址：详情页", "代采方拒绝发货申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中收货方号码", "代采方拒绝发货申请")
        Cp().slide_("380")
        forwarding_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "代采方拒绝发货申请")
        #
        receiving_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "代采方拒绝发货申请")
        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_re(str(total_Amount), price_sum, "获取详情页中商品总价", "代采方拒绝发货申请")

        our_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        our_service_charge = gl.get_value('our_service_charge')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "代采方拒绝发货申请")

        their_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        their_service_charge = gl.get_value('their_service_charge')
        self.check_information_if(their_service_charge, their_service_charge_1, "获取详情页中他方服务费金额", "代采方拒绝发货申请")
        Cp().slide_("580")
        time.sleep(0.5)
        submission_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]')
        self.check_information_time(submission_time, "获取详情页中提交时间", "代采方拒绝发货申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "获取详情页中账期", "代采方拒绝发货申请")

        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]')
        self.check_information_re(contractnumber, Contract_number_2, "获取详情页中合同编号", "代采方拒绝发货申请")

        record_state = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("供应商已提交", record_state, "拒绝发货申请前的操作状态", "代采方拒绝发货申请")

        record_operator = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
        self.check_information_re("18216482019", record_operator, "拒绝发货申请前的操作者信息", "代采方拒绝发货申请")

        record_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time, "拒绝发货申请前的操作时间", "代采方拒绝发货申请")
        Cp().slide_("686")
        print("********拒绝发货申请*********")
        Cp().xpath_click_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[6]/span/button[2]',
                                              "点击拒绝", "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        Cp().xpath_click_('//div[@class="ant-modal-body"]/div/div[2]/div/button[1]',
                          "选择拒绝标签1", "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)

        Cp().xpath_click_('//div[@class="ant-modal-body"]/div/div[2]/div/button[4]'
                          '', "选择拒绝标签2", "代采方拒绝发货申请", "云平台‘采购方’",
                          sys._getframe().f_lineno)
        time.sleep(2)
        Cp().xpath_click_('//div[@class="ant-modal-body"]/div/div[2]/div[2]/textarea',
                                          "点击拒绝理由", "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().xpath_send_('//textarea[@class="ant-input"]', "fkl")
        Cp().is_toast_exist("输入拒绝理由", "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().xpath_click_('//div[@class="ant-modal-footer"]/span/button[2]', "点击确认",
                                          "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认",
                                          "代采方拒绝发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        print("*****查看我方拒绝后发货申请*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入代采发货申请", "查看我方拒绝后发货申请", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[5]', "点击进入内部已拒绝", "查看我方拒绝后发货申请",
            "云平台‘采购方’", sys._getframe().f_lineno)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')  # 采购
        purchaser_name = gl.get_value('purchaser_name')  # bing
        invoiceApplySn_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看发货单信息", "查看我方拒绝后发货申请")

        receiving_party_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中fa货单位", "查看我方拒绝后发货申请")

        agent_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "查看我方拒绝后发货申请")

        contract_sum = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum, "列表中发货金额", "查看我方拒绝后发货申请")

        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('内部已拒绝', state_1, "查看发货单信息", "查看我方拒绝后发货申请")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击内部已拒绝-查看",
            "查看代理拒绝后发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "发货申请", "发货申请详情", "查看我方拒绝后发货申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 发起申请', '采购方 未通过', "代理方 待审核", "查看我方拒绝后发货申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')  # 采购
        purchaser_name = gl.get_value('purchaser_name')  # bing
        purchaserName_3 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_3, "获取详情页中发货方名称", "查看我方拒绝后发货申请")

        purchaserName_page_2 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaserName_page_2)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看我方拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中采购方企业名称信息", "查看我方拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaserName_4 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_4, "获取详情页中收货方名称", "查看我方拒绝后发货申请")

        purchaserName_page_3 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaserName_page_3)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看我方拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中销售方企业名称信息", "查看我方拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)方电话
        purchaserPhone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone_1, "获取详情页中发货方号码", "查看我方拒绝后发货申请")

        purchaser_address = gl.get_value('purchaser_address')  # 采购（甲）方地址
        purchaser_address = gl.get_value('purchaser_address')
        purchaserAdress_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "发货地址-详情页", "查看我方拒绝后发货申请")

        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址：详情页", "查看我方拒绝后发货申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone_1, "获取详情页中收货方号码", "查看我方拒绝后发货申请")
        Cp().slide_("380")
        forwarding_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "查看我方拒绝后发货申请")
        #
        receiving_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "查看我方拒绝后发货申请")
        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_re(str(total_Amount), price_sum, "获取详情页中商品总价", "查看我方拒绝后发货申请")

        our_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        our_service_charge = gl.get_value('our_service_charge')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "查看我方拒绝后发货申请")

        their_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        their_service_charge = gl.get_value('their_service_charge')
        self.check_information_if(their_service_charge, their_service_charge_1, "获取详情页中他方服务费金额", "查看我方拒绝后发货申请")
        Cp().slide_("580")
        time.sleep(0.5)
        submission_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]')
        self.check_information_time(submission_time, "获取详情页中提交时间", "查看我方拒绝后发货申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "获取详情页中账期", "查看我方拒绝后发货申请")

        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]')
        self.check_information_re(contractnumber, Contract_number_2, "获取详情页中合同编号", "查看我方拒绝后发货申请")

        record_state = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("采购商拒绝", record_state, "拒绝后发货申请后的操作状态", "查看我方拒绝后发货申请")

        record_operator = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
        self.check_information_re("18474793371", record_operator, "拒绝后发货申请后的操作人", "查看我方拒绝后发货申请")

        failureTag = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_re("其他 金额部分", failureTag, "拒绝后发货申请后的拒绝标签", "查看我方拒绝后发货申请")

        remark = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[4]')
        self.check_information_re("fkl", remark, "拒绝后发货申请后的拒绝理由", "查看我方拒绝后发货申请")

        record_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[5]')
        self.check_information_time(record_time, "拒绝后发货申请后的操作时间", "查看我方拒绝后发货申请")
        print("*****代采方查看拒绝发货申请后云票额度信息*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入代采发货申请", "代采方查看拒绝后云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        total_Amount = gl.get_value('total_Amount')
        estimateReduceQuota_purchaser = gl.get_value("estimateReduceQuota_purchaser")  # 预计减少云票
        totalCreditQuota_purchaser = gl.get_value('totalCreditQuota_purchaser')  # 甲 采购总授信云票"
        totalCirculationQuota_purchaser = gl.get_value('totalCirculationQuota_purchaser')  # 甲 采购总流转云票"
        totalOccupyCreditQuota_purchaser = gl.get_value('totalOccupyCreditQuota_purchaser')  # jia 已占用授信云票
        totalOccupyCirculationQuota_purchaser = gl.get_value('totalOccupyCirculationQuota_purchaser')  # jia 已占用流转云票
        totalOccupancyCreditQuota_purchaser = gl.get_value('totalOccupancyCreditQuota_purchaser')  # jia 可用总授信(总-已用)
        totalOccupancyCirculationQuota_purchaser = gl.get_value(
            'totalOccupancyCirculationQuota_purchaser')  # jia 余总流转(总-已用

        estimateReduceQuota_2 = Cp().xpath_text_(xpath_front + '/div/div[3]/div/div[2]/div[2]')
        self.check_information_if(estimateReduceQuota_purchaser, estimateReduceQuota_2, "预计减少额度", "代采方查看拒绝后云票额度信息")
        surplusAvailableTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupancyCreditQuota_purchaser, surplusAvailableTotalCreditQuota_1, "可用授信",
                                  "代采方查看拒绝后云票额度信息")
        occupyTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[1]/p[2]')
        self.check_information_re(totalOccupyCreditQuota_purchaser, occupyTotalCreditQuota_1, "已用授信", "代采方查看拒绝后云票额度信息")
        totalCreditQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[1]/div[3]')
        self.check_information_re(totalCreditQuota_purchaser, totalCreditQuota_1, "总授信", "代采方查看拒绝后云票额度信息")

        estimateAddQuota = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div[1]/div[2]')  # 预增云票
        Cp().is_toast_exist("获取预增云票", "代采方查看拒绝后云票额度信息", "云平台‘采购方’", sys._getframe().f_lineno)

        totalCirculationQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[2]/div[3]')
        totalCirculationQuota_1 = re_sub_(totalCirculationQuota_1)
        self.check_information_re(totalCirculationQuota_purchaser, totalCirculationQuota_1, "总流转", "代采方查看拒绝后云票额度信息")

        surplusTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[4]')
        surplusTotalCirculationQuota_1 = re_sub_(surplusTotalCirculationQuota_1)
        self.check_information_re(totalOccupancyCirculationQuota_purchaser, surplusTotalCirculationQuota_1,
                                  "剩余流转", "代采方查看拒绝后云票额度信息")
        surplusAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        surplusAvailableTotalCirculationQuota_1 = surplusAvailableTotalCirculationQuota_1[0:1]
        surplusAvailableTotalCirculationQuota_check = int(surplusTotalCirculationQuota_1) * 0.8
        self.check_information_re(surplusAvailableTotalCirculationQuota_1,
                                  str(surplusAvailableTotalCirculationQuota_check),
                                  "可用流转", "代采方查看拒绝后云票额度信息")
        occupyAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupyCirculationQuota_purchaser, occupyAvailableTotalCirculationQuota_1,
                                  "已用流转", "代采方查看拒绝后云票额度信息")
        loanAbilityQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[3]/p[2]')
        self.check_information_re(totalCirculationQuota_purchaser, loanAbilityQuota_1, "可贷现", "代采方查看拒绝后云票额度信息")

        time.sleep(1)
        Cp().xpath_click_('//*[@id="3$Menu"]/li[6]', "点击进入预计减少云票", "代采方查看拒绝后云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        estimateReduceQuota_2 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/span')
        self.check_information_re(estimateReduceQuota_purchaser, estimateReduceQuota_2, "预计减少额度", "代采方查看拒绝后云票额度信息")

    def delivery_application(self):  # 代采方通过发货申请
        driver = self.driver
        print("*****代采方通过发货申请*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入代采发货申请", "代采方通过发货申请", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        self.catalog_two(driver, "代采管理", "收货申请", "代采方通过发货申请", "发货申请列表页一级目录", "发货申请列表页二级目录")
        self.list_six(driver, "全部", "内部待同意", "代理方待审批", "代理方已通过", "内部已拒绝", "代理方已拒绝", "代采方通过发货申请", "代采管理-所有发货单列表",
                      "代采管理-客户待审批列表", "代采管理-代理方待审批列表", "代采管理-代理方已通过列表", "代采管理-客户未通过列表", "代采管理-代理方未通过列表")
        Cp().xpath_click_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击进入内部待同意", "代采方通过发货申请", "云平台‘采购方’",
            sys._getframe().f_lineno)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        invoiceApplySn_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看发货单信息", "代采方通过发货申请")
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')  # 采购
        purchaser_name = gl.get_value('purchaser_name')  # bing
        receiving_party_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中fa货单位", "代采方通过发货申请")

        agent_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "代采方通过发货申请")

        contract_sum = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum, "列表中发货金额", "代采方通过发货申请")
        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('内部待同意', state_1, "查看发货单信息", "发起发货申请")
        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击内部待同意-查看",
            "代采方通过发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "发货申请", "发货申请详情", "代采方通过发货申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 发起申请', '采购方 待审批', "代理方 待审核", "代采方通过发货申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')  # 采购
        purchaser_name = gl.get_value('purchaser_name')  # bing
        purchaserName_4 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_4, "获取详情页中发货方名称", "代采方通过发货申请")

        purchaserName_page_3 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaserName_page_3)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代采方通过发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中采购方企业名称信息", "代采方通过发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaserName_4 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_4, "获取详情页中收货方名称", "代采方通过发货申请")

        purchaserName_page_3 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaserName_page_3)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代采方通过发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_3 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_3, "新页面中销售方企业名称信息", "代采方通过发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)方电话
        purchaserPhone = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中发货方号码", "代采方通过发货申请")

        purchaser_address = gl.get_value('purchaser_address')
        purchaser_address = gl.get_value('purchaser_address')

        purchaserAdress_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "发货地址-详情页", "代采方通过发货申请")

        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址：详情页", "代采方通过发货申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中收货方号码", "代采方通过发货申请")
        Cp().slide_("380")
        forwarding_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "代采方通过发货申请")
        #
        receiving_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "代采方通过发货申请")
        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_re("¥%s"%total_Amount, price_sum, "获取详情页中商品总价", "代采方通过发货申请")

        our_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        our_service_charge = gl.get_value('our_service_charge')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "代采方通过发货申请")

        their_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        their_service_charge = gl.get_value('their_service_charge')
        self.check_information_if(their_service_charge, their_service_charge_1, "获取详情页中他方服务费金额", "代采方通过发货申请")
        Cp().slide_("580")
        time.sleep(0.5)
        submission_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]')
        self.check_information_time(submission_time, "获取详情页中提交时间", "代采方通过发货申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "代采方通过发货申请")

        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]')
        self.check_information_re(contractnumber, Contract_number_2, "获取详情页中合同编号", "代采方通过发货申请")

        record_state = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("供应商已提交", record_state, "通过发货申请前的操作状态", "代采方通过发货申请")

        record_operator = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
        self.check_information_re("18216482019", record_operator, "通过发货申请前的操作者信息", "代采方通过发货申请")

        record_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time, "通过发货申请前的操作时间", "代采方通过发货申请")
        Cp().slide_("720")
        Cp().xpath_keys_ENTER('//div[@class="ant-row"]/div/div[2]/div/div[2]/div[6]/span/button[1]',
                                              "点击通过",
                                              "代采方通过发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        # Cp().xpath_click_('/html/body/div[3]/div/div[2]/div/div[2]/div/div/div[2]/button[2]', "确认通过",
        #                              "代采方通过发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().xpath_keys_ENTER('//div[@class="ant-modal-confirm-btns"]/button[2]', "确认通过",
                                              "代采方通过发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        # driver.find_element_by_xpath(
        #     'div[@class="ant-modal-body"]/div/div[2]/button[2]', "确认通过",
        #     "代采方通过发货申请", "云平台‘采购方’", sys._getframe().f_lineno).send_keys()

        time.sleep(3)
        print("*****代采方查看通过后发货申请*****")
        Cp().slide_("0")
        time.sleep(2)
        Cp().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入代采发货申请", "代采方查看通过后发货申请", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击进入代理方待审批", "代采方查看通过后发货申请",
            "云平台‘采购方’", sys._getframe().f_lineno)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name = gl.get_value('purchaser_name')  # bing
        invoiceApplySn_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看发货单信息", "代采方查看通过后发货申请")

        receiving_party_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中fa货单位", "代采方查看通过后发货申请")

        agent_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "代采方查看通过后发货申请")

        contract_sum = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum, "列表中发货金额", "代采方查看通过后发货申请")

        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('代理方待审批', state_1, "查看发货单信息", "代采方查看通过后发货申请")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击代理方待审批-查看",
            "代采方查看通过后发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "发货申请", "发货申请详情", "代采方查看通过后发货申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 已审批', '采购方 已同意', "代理方 待审核", "代采方查看通过后发货申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')  # 采购
        purchaser_name = gl.get_value('purchaser_name')  # bing

        purchaserName_5 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_5, "获取详情页中发货方名称", "代采方查看通过后发货申请")

        purchaserName_page_4 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaserName_page_4)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代采方查看通过后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_4 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_4, "新页面中采购方企业名称信息", "代采方查看通过后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaserName_5 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_5, "获取详情页中收货方名称", "代采方查看通过后发货申请")

        purchaserName_page_6 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaserName_page_6)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "代采方查看通过后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_4 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_4, "新页面中销售方企业名称信息", "代采方查看通过后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)方电话
        purchaserPhone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone_1, "获取详情页中发货方号码", "代采方查看通过后发货申请")

        purchaser_address = gl.get_value('purchaser_address')
        purchaser_address = gl.get_value('purchaser_address')

        purchaserAdress_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "发货地址-详情页", "代采方查看通过后发货申请")

        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址：详情页", "代采方查看通过后发货申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone_1, "获取详情页中收货方号码", "代采方查看通过后发货申请")
        Cp().slide_("380")
        forwarding_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "代采方查看通过后发货申请")
        #
        receiving_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "代采方查看通过后发货申请")
        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_re("¥%s"%total_Amount, price_sum, "获取详情页中商品总价", "代采方查看通过后发货申请")

        our_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        our_service_charge = gl.get_value('our_service_charge')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "代采方查看通过后发货申请")

        their_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        their_service_charge = gl.get_value('their_service_charge')
        self.check_information_if(their_service_charge, their_service_charge_1, "获取详情页中他方服务费金额", "代采方查看通过后发货申请")
        Cp().slide_("580")
        time.sleep(0.5)
        submission_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]')
        self.check_information_time(submission_time, "获取详情页中提交时间", "代采方查看通过后发货申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "获取详情页中账期", "代采方查看通过后发货申请")

        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]')
        self.check_information_re(contractnumber, Contract_number_2, "获取详情页中合同编号", "代采方查看通过后发货申请")

        record_state = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("采购商已同意", record_state, "通过后发货申请后的操作状态", "代采方查看通过后发货申请")

        record_operator = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
        if re.findall("test", self.start_url):
            self.check_information_re("18474793371", record_operator, "通过后发货申请后的操作人", "代采方查看通过后发货申请")
        else:
            self.check_information_re("18390552449_s", record_operator, "通过后发货申请后的操作人", "代采方查看通过后发货申请")

        record_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time, "通过后发货申请后的操作时间", "代采方查看通过后发货申请")
        print("*****代采方查看己方通过发货申请后云票额度信息*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入代采发货申请", "代采方查看己方通过发货申请后云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        total_Amount = gl.get_value('total_Amount')
        estimateReduceQuota_purchaser = gl.get_value("estimateReduceQuota_purchaser")  # 预计减少云票
        totalCreditQuota_purchaser = gl.get_value('totalCreditQuota_purchaser')  # 甲 采购总授信云票"
        totalCirculationQuota_purchaser = gl.get_value('totalCirculationQuota_purchaser')  # 甲 采购总流转云票"
        totalOccupyCreditQuota_purchaser = gl.get_value('totalOccupyCreditQuota_purchaser')  # jia 已占用授信云票
        totalOccupyCirculationQuota_purchaser = gl.get_value('totalOccupyCirculationQuota_purchaser')  # jia 已占用流转云票
        totalOccupancyCreditQuota_purchaser = gl.get_value('totalOccupancyCreditQuota_purchaser')  # jia 可用总授信(总-已用)
        totalOccupancyCirculationQuota_purchaser = gl.get_value(
            'totalOccupancyCirculationQuota_purchaser')  # jia 余总流转(总-已用

        estimateReduceQuota_2 = Cp().xpath_text_(xpath_front + '/div/div[3]/div/div[2]/div[2]')
        estimateReduceQuota_2 = re_sub_(estimateReduceQuota_2)
        total_Amount = gl.get_value('total_Amount')
        estimateReduceQuota_purchaser = re_sub_(estimateReduceQuota_purchaser)
        estimateReduceQuota_purchaser_check = int(total_Amount) + int(estimateReduceQuota_purchaser)
        self.check_information_if(estimateReduceQuota_purchaser_check, estimateReduceQuota_2, "预计减少额度",
                                  "代采方查看己方通过发货申请后云票额度信息")
        surplusAvailableTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupancyCreditQuota_purchaser, surplusAvailableTotalCreditQuota_1, "可用授信",
                                  "代采方查看己方通过发货申请后云票额度信息")
        occupyTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[1]/p[2]')
        self.check_information_re(totalOccupyCreditQuota_purchaser, occupyTotalCreditQuota_1, "已用授信",
                                  "代采方查看己方通过发货申请后云票额度信息")
        totalCreditQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[1]/div[3]')
        self.check_information_re(totalCreditQuota_purchaser, totalCreditQuota_1, "总授信", "代采方查看己方通过发货申请后云票额度信息")

        estimateAddQuota = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div[1]/div[2]')  # 预增云票
        Cp().is_toast_exist("获取预增云票", "代采方查看己方通过发货申请后云票额度信息", "云平台‘采购方’", sys._getframe().f_lineno)

        totalCirculationQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[2]/div[3]')
        totalCirculationQuota_1 = re_sub_(totalCirculationQuota_1)
        self.check_information_re(totalCirculationQuota_purchaser, totalCirculationQuota_1, "总流转",
                                  "代采方查看己方通过发货申请后云票额度信息")

        surplusTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[4]')
        surplusTotalCirculationQuota_1 = re_sub_(surplusTotalCirculationQuota_1)
        self.check_information_re(totalOccupancyCirculationQuota_purchaser, surplusTotalCirculationQuota_1,
                                  "剩余流转", "代采方查看己方通过发货申请后云票额度信息")
        surplusAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        surplusAvailableTotalCirculationQuota_check = int(surplusTotalCirculationQuota_1) * 0.8
        self.check_information_re(surplusAvailableTotalCirculationQuota_1,
                                  str(surplusAvailableTotalCirculationQuota_check),
                                  "可用流转", "代采方查看己方通过发货申请后云票额度信息")
        occupyAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupyCirculationQuota_purchaser, occupyAvailableTotalCirculationQuota_1,
                                  "已用流转", "代采方查看己方通过发货申请后云票额度信息")
        loanAbilityQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[3]/p[2]')
        self.check_information_re(totalCirculationQuota_purchaser, loanAbilityQuota_1, "可贷现", "代采方查看己方通过发货申请后云票额度信息")

        time.sleep(1)
        Cp().xpath_click_('//*[@id="3$Menu"]/li[6]', "点击进入预计减少云票", "代采方查看己方通过发货申请后云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        estimateReduceQuota_purchaser = gl.get_value("estimateReduceQuota_purchaser")  # 预计减少云票
        estimateReduceQuota_1 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/span')
        estimateReduceQuota_1 = re_sub_(estimateReduceQuota_1)  # 显示为12,500.00 正则筛选
        total_Amount = gl.get_value('total_Amount')
        estimateReduceQuota_purchaser_check = int(total_Amount) + int(estimateReduceQuota_purchaser)
        self.check_information_re(str(estimateReduceQuota_purchaser_check), estimateReduceQuota_1, "预计减少额度",
                                  "代采方查看己方通过发货申请后云票额度信息")
        invoiceApplySn = gl.get_value('invoiceApplySn')  # DF 发货单
        invoiceApplySn_0 = Cp().xpath_text_(
            xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_0, "发货申请单号", "代采方查看己方通过发货申请后云票额度信息")

    def refuse_application_1(self):
        driver = self.driver
        print("*****查看代理拒绝后发货申请*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击进入代采发货申请", "查看代理拒绝后发货申请", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[6]', "点击进入代理方已拒绝", "查看代理拒绝后发货申请",
            "云平台‘采购方’", sys._getframe().f_lineno)
        invoiceApplySn = gl.get_value('invoiceApplySn')
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name = gl.get_value('purchaser_name')  # bing
        invoiceApplySn_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看发货单信息", "查看代理拒绝后发货申请")

        receiving_party_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中fa货单位", "查看代理拒绝后发货申请")

        agent_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "查看代理拒绝后发货申请")

        contract_sum = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum, "列表中发货金额", "查看代理拒绝后发货申请")

        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('代理方已拒绝', state_1, "查看发货单信息", "查看代理拒绝后发货申请")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击内部已拒绝-查看",
            "查看代理拒绝后发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "发货申请", "发货申请详情", "查看代理拒绝后发货申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 已审批', '采购方 已同意', "代理方 未通过", "查看代理拒绝后发货申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')  # 采购
        purchaser_name = gl.get_value('purchaser_name')  # bing

        purchaserName_5 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_5, "获取详情页中发货方名称", "查看代理拒绝后发货申请")

        purchaserName_page_4 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaserName_page_4)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_4 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_4, "新页面中采购方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaserName_5 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_5, "获取详情页中收货方名称", "查看代理拒绝后发货申请")

        purchaserName_page_6 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaserName_page_6)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_4 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_4, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)方电话
        purchaserPhone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone_1, "获取详情页中发货方号码", "查看代理拒绝后发货申请")

        purchaser_address = gl.get_value('purchaser_address')

        purchaser_address = gl.get_value('purchaser_address')

        purchaserAdress_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "发货地址-详情页", "查看代理拒绝后发货申请")

        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址：详情页", "查看代理拒绝后发货申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone_1, "获取详情页中收货方号码", "查看代理拒绝后发货申请")
        Cp().slide_("380")
        forwarding_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "查看代理拒绝后发货申请")
        #
        receiving_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "查看代理拒绝后发货申请")
        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_re("¥%s"%total_Amount, price_sum, "获取详情页中商品总价", "查看代理拒绝后发货申请")

        our_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        our_service_charge = gl.get_value('our_service_charge')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "查看代理拒绝后发货申请")

        their_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        their_service_charge = gl.get_value('their_service_charge')
        self.check_information_if(their_service_charge, their_service_charge_1, "获取详情页中他方服务费金额", "查看代理拒绝后发货申请")
        Cp().slide_("580")
        time.sleep(0.5)
        submission_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]')
        self.check_information_time(submission_time, "获取详情页中提交时间", "查看代理拒绝后发货申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "获取详情页中账期", "查看代理拒绝后发货申请")

        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]')
        self.check_information_re(contractnumber, Contract_number_2, "获取详情页中合同编号", "查看代理拒绝后发货申请")

        record_state = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("代理驳回", record_state, "拒绝后发货申请后的操作状态", "查看代理拒绝后发货申请")
        if re.findall("test", self.start_url):
            record_operator = Cp().xpath_text_(
                '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
            self.check_information_re("13245678999_s", record_operator, "拒绝后发货申请后的操作人", "查看代理拒绝后发货申请")
        else:
            record_operator = Cp().xpath_text_(
                '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
            self.check_information_re("18373847538_s", record_operator, "拒绝后发货申请后的操作人", "查看代理拒绝后发货申请")
        failureTag = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_re("其他 金额部分", failureTag, "拒绝后发货申请后的拒绝标签", "查看代理拒绝后发货申请")

        remark = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[4]')
        self.check_information_re("fkl", remark, "拒绝后发货申请后的拒绝理由", "查看代理拒绝后发货申请")

        record_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[5]')
        self.check_information_time(record_time, "拒绝后发货申请后的操作时间", "查看代理拒绝后发货申请")

        print("*****查看代理拒绝发货申请后云票额度信息*****")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入代采发货申请", "查看代理拒绝发货申请后云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        estimateReduceQuota_purchaser = gl.get_value("estimateReduceQuota_purchaser")  # 预计减少云票
        estimateReduceQuota_2 = Cp().xpath_text_(xpath_front + '/div/div[3]/div/div[2]/div[2]')
        estimateReduceQuota_2 = re_sub_(estimateReduceQuota_2)
        self.check_information_if(estimateReduceQuota_purchaser, estimateReduceQuota_2, "预计减少额度", "查看代理拒绝发货申请后云票额度信息")
        time.sleep(1)
        Cp().xpath_click_('//*[@id="3$Menu"]/li[6]', "点击进入预计减少云票", "查看代理拒绝发货申请后云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        estimateReduceQuota_2 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/span')
        estimateReduceQuota_2 = re_sub_(estimateReduceQuota_2)
        self.check_information_re(estimateReduceQuota_purchaser, estimateReduceQuota_2, "预计减少额度", "查看代理拒绝发货申请后云票额度信息")

    def see_application_adopt(self):  # 查看被代理方通过的发货申请
        print("*********查看被代理方通过的发货申请***********")
        driver = self.driver
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[1]', "点击发货申请", "查看被代理方通过的发货申请", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击代理方已通过",
                                          "查看被代理方通过的发货申请", "云平台‘采购方’", sys._getframe().f_lineno)

        invoiceApplySn = gl.get_value('invoiceApplySn')
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name = gl.get_value('purchaser_name')  # bing
        invoiceApplySn_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_re(invoiceApplySn, invoiceApplySn_1, "查看被代理方通过的发货申请", "发起发货申请")

        receiving_party_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(purchaser_name, receiving_party_1, "列表中fa货单位", "查看被代理方通过的发货申请")

        agent_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_1, "列表中代理方", "查看被代理方通过的发货申请")

        contract_sum = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum, "列表中发货金额", "查看被代理方通过的发货申请")
        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('代理方已通过', state_1, "查看发货单信息", "查看被代理方通过的发货申请")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button',
            "点击查看", "查看被代理方通过的发货申请", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "发货申请", "发货申请详情", "查看被代理方通过的发货申请", "发货申请详情页一级目录",
                           "发货申请详情页二级目录", "发货申请详情页三级目录")
        self.navigation_three(driver, '销售方 已审批', '采购方 已同意', "代理方 已同意", "查看被代理方通过的发货申请",
                              "发货申请第一步导航信息", "发货申请第二步导航信息", "发货申请第三步导航信息")
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名 purchaser_name jia
        purchaser_name = gl.get_value('purchaser_name')  # 采购
        purchaser_name = gl.get_value('purchaser_name')  # bing
        purchaserName_5 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_5, "获取详情页中发货方名称", "查看代理拒绝后发货申请")

        purchaserName_page_4 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaserName_page_4)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_4 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_4, "新页面中采购方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaserName_5 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaserName_5, "获取详情页中收货方名称", "查看代理拒绝后发货申请")

        purchaserName_page_6 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaserName_page_6)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_4 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_4, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)方电话
        purchaserPhone = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中发货方号码", "查看被代理方通过的发货申请")

        purchaser_address = gl.get_value('purchaser_address')

        purchaser_address = gl.get_value('purchaser_address')

        purchaserAdress_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress_1, "发货地址-详情页", "查看被代理方通过的发货申请")

        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址：详情页", "查看被代理方通过的发货申请")

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaserPhone = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaserPhone, "获取详情页中收货方号码", "查看被代理方通过的发货申请")

        forwarding_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[1]/div[2]')
        self.check_information_if("40.00", forwarding_proportion, "获取详情页中销售方服务费比例", "查看被代理方通过的发货申请")
        #
        receiving_proportion = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[1]/div[2]')
        self.check_information_if("60.00", receiving_proportion, "获取详情页中采购方服务费比例", "查看被代理方通过的发货申请")
        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_re(str(total_Amount), price_sum, "获取详情页中商品总价", "查看被代理方通过的发货申请")
        Cp().slide_("580")
        time.sleep(0.5)
        our_service_charge = gl.get_value('our_service_charge')
        our_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]')
        self.check_information_if(our_service_charge, our_service_charge_1, "获取详情页中我方服务费金额", "查看被代理方通过的发货申请")

        their_service_charge = gl.get_value('their_service_charge')
        their_service_charge_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div[2]/div[2]')
        self.check_information_if(their_service_charge, their_service_charge_1, "详情页中他方服务费金额", "查看被代理方通过的发货申请")

        submission_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]')
        self.check_information_time(submission_time, "详情页中提交时间", "查看被代理方通过的发货申请")
        settlement_date = gl.get_value('settlement_date')
        settlement_date_1 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(settlement_date, settlement_date_1, "获取详情页中账期", "查看被代理方通过的发货申请")

        contractnumber = gl.get_value('contractnumber')
        Contract_number_2 = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]')
        self.check_information_re(contractnumber, Contract_number_2, "获取详情页中合同编号", "查看被代理方通过的发货申请")

        record_state = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if("代理通过", record_state, "发货申请后的操作状态", "查看被代理方通过的发货申请")
        if re.findall("test", self.start_url):
            record_operator = Cp().xpath_text_(
                '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
            self.check_information_re("13245678999_s", record_operator, "发货申请后的操作人", "查看被代理方通过的发货申请")
        else:
            record_operator = Cp().xpath_text_(
                '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]')
            self.check_information_re("18373847538_s", record_operator, "发货申请后的操作人", "查看被代理方通过的发货申请")

        record_time = Cp().xpath_text_(
            '//div[@class="ant-row"]/div/div[2]/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time, "发货申请后的操作时间", "查看被代理方通过的发货申请")
        print("*********查看代理方通过发货申请后的收货管理***********")

        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[2]', "点击出货管理", "查看代理方通过发货申请后的收货管理", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击待收货",
                                          "查看代理方通过发货申请后的收货管理", "云平台‘采购方’", sys._getframe().f_lineno)
        try:
            invoiceApplySn2 = Cp().xpath_text_(
                xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]').find_element_by_xpath()
            self.check_information_if(invoiceApplySn, invoiceApplySn2, "列表页发货编号", "查看代理方通过发货申请后的收货管理")
        except:
            pass
        print("*********查看代理方通过发货申请后的合同履行***********")
        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="0$Menu"]/li[4]', "进入合同签订", "查看代理方通过发货申请后的合同", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
        self.catalog_two(driver, "合同管理", "合同履行列表", "查看代理方通过发货申请后的合同", "合同履行列表页一级目录", "合同履行列表页二级目录")
        self.list_three(driver, "全部", "代理采购", "代理销售", "查看代理方通过发货申请后的合同", "合同履行-全部列表",
                        "合同履行-我方待审批列表", "合同履行-合作方待审批列表")

        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]',
                                          "进入代理销售",
                                          "查看代理方通过发货申请后的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(1)
        contractnumber_number_3 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[1]')
        self.check_information_if(contractnumber, contractnumber_number_3, "校验合同编号是否一致", "查看代理方通过发货申请后的合同")

        a_time_3 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[6]')
        self.check_information_time(a_time_3, "‘校验提交时间是否一致", "查看代理方通过发货申请后的合同")
        state_3 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[7]/div')
        self.check_information_if("受托方已通过", state_3, "校验状态", "查看代理方通过发货申请后的合同")
        Cp().xpath_click_(
            xpath_front + '/div/div[2]/div[2]/div/div/div/div/div/table/tbody/tr[1]/td[8]/div/a/button', "点击查看",
            "查看代理方通过发货申请后的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        # 校验目录、导航
        self.catalog_three(driver, "合同管理", "合同履行", "合同详情", "查看代理方通过发货申请后的合同", "合同详情一级目录", "合同详情二级目录",
                           "合同详情三级目录")
        self.navigation_three(driver, "销售方已审签", "采购方已审签", "受托方已审签", "查看代理方通过发货申请后的合同",
                              "合同签审第一步导航信息", "合同签审第二步导航信息", "合同签审第三步导航信息")

        Cp().slide_("100")
        self.contract_content(driver, "校验代理方通过审批后的合同")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[5]',
                                          "点击操作记录",
                                          "查看代理方通过发货申请后的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名

        if re.findall("test", self.start_url):
            self.Operation_record(driver, "代理商已审签", '深圳市九二六供应链网络有限公司代采分公司1 13245678999_s', "查看代理方通过发货申请后的合同",
                                  "查看代理方通过发货申请后的操作状态", "查看通过发货申请后的操作时间", "查看代理方通过发货申请后的操作者", "5")
        else:
            self.Operation_record(driver, "代理商已审签", '深圳市九二六供应链网络有限公司 18373847538_s', "查看代理方通过发货申请后的合同",
                                  "查看代理方通过发货申请后的操作状态", "查看通过发货申请后的操作时间", "查看代理方通过发货申请后的操作者", "5")
        Cp().xpath_click_(xpath_front + '/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击履行记录",
                                          "查看代理方通过发货申请后的合同", "云平台‘采购方’", sys._getframe().f_lineno)
        self.performance_record(driver, "校验代理方通过审批后的合同")  # 校验合同履行信息

        print("*********查看代理方通过发货申请后的已用额度***********")

        Cp().slide_("0")
        Cp().xpath_click_('//*[@id="3$Menu"]/li[1]', "点击进入代采发货申请", "查看代理方通过发货申请后的已用额度", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        total_Amount = gl.get_value('total_Amount')
        estimateReduceQuota_purchaser = gl.get_value("estimateReduceQuota_purchaser")  # 预计减少云票
        totalCreditQuota_purchaser = gl.get_value('totalCreditQuota_purchaser')  # 甲 采购总授信云票"
        totalCirculationQuota_purchaser = gl.get_value('totalCirculationQuota_purchaser')  # 甲 采购总流转云票"
        totalOccupyCreditQuota_purchaser = gl.get_value('totalOccupyCreditQuota_purchaser')  # jia 已占用授信云票
        totalOccupyCirculationQuota_purchaser = gl.get_value('totalOccupyCirculationQuota_purchaser')  # jia 已占用流转云票
        totalOccupancyCreditQuota_purchaser = gl.get_value('totalOccupancyCreditQuota_purchaser')  # jia 可用总授信(总-已用)
        totalOccupancyCirculationQuota_purchaser = gl.get_value(
            'totalOccupancyCirculationQuota_purchaser')  # jia 余总流转(总-已用)

        estimateReduceQuota_2 = Cp().xpath_text_(xpath_front + '/div/div[3]/div/div[2]/div[2]')
        self.check_information_if(estimateReduceQuota_purchaser, estimateReduceQuota_2, "预计减少额度", "查看代理方签审后云票额度信息")
        surplusAvailableTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[2]/p[2]')
        surplusAvailableTotalCreditQuota_check = int(totalOccupancyCreditQuota_purchaser) - int(total_Amount)
        self.check_information_re(str(surplusAvailableTotalCreditQuota_check), surplusAvailableTotalCreditQuota_1,
                                  "可用授信", "查看代理方签审后云票额度信息")
        occupyTotalCreditQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[1]/div[2]/div[1]/p[2]')
        occupyTotalCreditQuota_check = int(totalOccupyCreditQuota_purchaser) + int(total_Amount)
        self.check_information_re(str(occupyTotalCreditQuota_check), occupyTotalCreditQuota_1, "已用授信", "查看代理方签审后云票额度信息")
        totalCreditQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[1]/div[3]')
        self.check_information_re(totalCreditQuota_purchaser, totalCreditQuota_1, "总授信", "查看代理方签审后云票额度信息")

        estimateAddQuota = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div[1]/div[2]')  # 预增云票
        Cp().is_toast_exist("获取预增云票", "查看代理方签审后云票额度信息", "云平台‘采购方’", sys._getframe().f_lineno)

        totalCirculationQuota_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div/div[2]/div[3]')
        totalCirculationQuota_1 = re_sub_(totalCirculationQuota_1)
        self.check_information_re(totalCirculationQuota_purchaser, totalCirculationQuota_1, "总流转", "查看代理方签审后云票额度信息")

        surplusTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[4]')
        surplusTotalCirculationQuota_1 = re_sub_(surplusTotalCirculationQuota_1)
        self.check_information_re(totalOccupancyCirculationQuota_purchaser, surplusTotalCirculationQuota_1,
                                  "剩余流转", "查看代理方签审后云票额度信息")
        surplusAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        surplusAvailableTotalCirculationQuota_check = int(surplusTotalCirculationQuota_1) * 0.8
        surplusAvailableTotalCirculationQuota_check = int(surplusAvailableTotalCirculationQuota_check)
        self.check_information_re(str(surplusAvailableTotalCirculationQuota_check),
                                  surplusAvailableTotalCirculationQuota_1,
                                  "可用流转", "查看代理方签审后云票额度信息")
        occupyAvailableTotalCirculationQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[2]/p[2]')
        self.check_information_re(totalOccupyCirculationQuota_purchaser, occupyAvailableTotalCirculationQuota_1,
                                  "已用流转", "查看代理方签审后云票额度信息")
        loanAbilityQuota_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div/div[2]/div[2]/div[3]/p[2]')
        self.check_information_re(totalCirculationQuota_purchaser, loanAbilityQuota_1, "可贷现", "查看代理方签审后云票额度信息")

        time.sleep(1)
        Cp().xpath_click_('//*[@id="3$Menu"]/li[6]', "点击进入预计减少云票", "查看代理方签审后云票额度信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(2)
        estimateReduceQuota_2 = Cp().xpath_text_(xpath_front + '/div/div/div[1]/span')
        estimateReduceQuota_2 = re_sub_(estimateReduceQuota_2)
        self.check_information_re(estimateReduceQuota_purchaser, estimateReduceQuota_2, "预计减少额度", "查看代理方签审后云票额度信息")
        try:
            invoiceApplySn_0 = Cp().xpath_text_(
                xpath_front + '/div/div/div[2]/div/div/div/div/div/table/tbody/tr/td[1]')
            if invoiceApplySn == invoiceApplySn_0:
                sys.exit()
        except Exception as e:
            pass

    def receiving_goods(self):  # 采购方收货
        driver = self.driver
        Cp().slide_("0")
        print("*****采购方收货*****")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[2]', "点击进入代采收货管理", "采购方收货", "云平台‘采购方’",
                                          sys._getframe().f_lineno)

        time.sleep(1)
        self.catalog_two(driver, "代采管理", "收货单列表", "采购方收货", "收货单列表页一级目录", "收货单列表页二级目录")
        self.list_five(driver, "所有收货单", "待收货", "待品检", "待入库", "已入库", "采购方收货", "代采管理-全部列表",
                       "代采管理-待收货列表", "代采管理-待品检列表", "代采管理-待入库列表", "代采管理-已入库列表")

        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]', "点击待收货",
                                          "代采方收货", "云平台‘收到’方", sys._getframe().f_lineno)
        invoiceSn = gl.get_value('invoiceSn')
        invoiceSn2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]', sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn2, "列表页发货编号", "采购方收货")

        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[3]')
        self.check_information_if(purchaser_name, purchaser_name_2, "列表中fa货单位", "采购方收货")

        agent_name = gl.get_value('agent_name')
        purchaser_name = gl.get_value('purchaser_name')
        agent_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_2, "列表中代理方", "采购方收货")

        contract_sum1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum1, "列表中发货金额", "采购方收货")
        state_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('待收货', state_2, "查看发货单状态", "采购方收货")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button'
            , "点击待收货-查看", "采购方收货", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "收货单列表", "收货单详情", "采购方收货", "采购管理详情页一级目录",
                           "采购管理详情页二级目录", "采购管理详情页三级目录")
        navigation_1 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[1]/div[3]/div')
        self.check_information_if('待收货', navigation_1, '收货详情第一步导航信息', '采购方收货')
        navigation_2 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[2]/div[3]/div')
        self.check_information_if('待品检', navigation_2, '收货详情第二步导航信息', '采购方收货')
        navigation_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[3]/div[3]/div')
        self.check_information_if("待入库", navigation_3, '收货详情第三步导航信息', '采购方收货')
        navigation_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[4]/div[3]/div')
        self.check_information_if("入库完成", navigation_3, '收货详情第四步导航信息', '采购方收货')
        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)  #方电话

        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "发货单位", "采购方收货")

        purchaser_name_page_1 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_address = gl.get_value('purchaser_address')
        purchaserAdress = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress, "发货单位：详情页", "采购方收货")

        purchaser_phone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "发货单位电话", "采购方收货")
        total_Amount = gl.get_value('total_Amount')

        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位-详情页", "采购方收货")

        purchaser_name_page_1 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "查看代理拒绝后发货申请",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "查看代理拒绝后发货申请")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_address = gl.get_value('purchaser_address')
        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址-详情页", "采购方收货")

        purchaser_phone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "收货单位电话：详情页", "采购方收货")

        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p', sys._getframe().f_lineno)
        price_sum = re_int1(price_sum)
        self.check_information_if(str(total_Amount), price_sum, "获取详情页中商品总价", "采购方收货")
        try:
            Cp().slide_("555", sys._getframe().f_lineno)
            logistiCpSn = gl.get_value('logistiCpSn')  # 物流公司信息
            companyName = gl.get_value('companyName')  # 物流单号信息
            logistiCp_img = gl.get_value('logistiCp_img')  # 详情页中物流单图片
            invoiceApply_img = gl.get_value('invoiceApply_img')  # 详情页中出货单图片
            companyName_1 = driver.find_element_by_xpath(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[1]/div[1]/div[2]').text
            self.check_information_if(companyName, companyName_1, "详情页中物流公司信息", "采购方收货")
            print("校验是否为物流配送，获取物流公司信息：%s " % companyName)
            logistiCpSn_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[1]/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(logistiCpSn, logistiCpSn_1, "详情页中物流单号信息", "采购方收货")
            logistiCp_img_1 = Cp().xpath_src_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_re(logistiCp_img, logistiCp_img_1, "详情页中物流单图片",
                                      "采购方收货")
            invoiceApply_img_1 = Cp().xpath_src_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_if(invoiceApply_img, invoiceApply_img_1, "详情页中出货单图片",
                                      "采购方收货")
            Cp().slide_("1900", sys._getframe().f_lineno)
            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "采购方收货")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "采购方收货")

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "采购方收货")

            shipment_time = gl.get_value('shipment_time')
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中出货时间", "采购方收货")

            purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)  #方926链号
            record_state1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商待收货', record_state1, "操作记录中未出货状态", '采购方收货')

            record_operator1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li[1]/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '采购方收货')

            record_time1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '采购方收货')

            shipment_time = gl.get_value('shipment_time')  # 出货时间
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中出货时间", "采购方收货")

            Cp().xpath_keys_ENTER(xpath_front_2 + '/div/div[2]/div[6]/span/button[2]', "点击确认收货",
                                                  "采购方收货",
                                                  "云平台‘采购方’", sys._getframe().f_lineno)
            Cp().xpath_click_(
                '//div[@class="ant-modal-confirm-btns"]/button[2]',
                "再次确认收货", "采购方收货", "云平台‘采购方’", sys._getframe().f_lineno)
            time.sleep(2)
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[5]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中收货时间", "采购方收货")

        except Exception:
            Cp().slide_("555", sys._getframe().f_lineno)
            distribution_mode = gl.get_value('distribution_mode')
            distribution_mode_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(distribution_mode, distribution_mode_1, "详情页中出货单编号", "采购方收货")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "采购方收货")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "采购方收货")

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "采购方收货")

            shipment_time = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time, "详情页中出货时间", "采购方收货")

            purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)  #方926链号
            record_state1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商待收货', record_state1, "操作记录中未出货状态", '采购方收货')

            record_operator1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '采购方收货')

            record_time1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '采购方收货')

            Cp().xpath_keys_ENTER('//button[2]', "点击确认收货", "采购方收货", "云平台‘采购方’",
                                                  sys._getframe().f_lineno)
            Cp().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认收货",
                                              "采购方收货", "云平台‘采购方’", sys._getframe().f_lineno)
            time.sleep(2)
            Cp().slide_("500")
            shipment_time = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[5]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中收货时间", "采购方收货")

    # 采购方品检
    def inspection(self):
        driver = self.driver
        Cp().slide_("0")
        print("*****采购方品检*****")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[2]', "点击进入代采收货管理", "采购方品检", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        self.catalog_two(driver, "代采管理", "收货单列表", "采购方品检", "收货单列表页一级目录", "收货单列表页二级目录")
        self.list_five(driver, "所有收货单", "待收货", "待品检", "待入库", "已入库", "采购方品检", "代采管理-全部列表",
                       "代采管理-待收货列表", "代采管理-待品检列表", "代采管理-待入库列表", "代采管理-已入库列表")

        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]',
                                          "点击进入待品检", "采购方品检", "云平台‘采购方’", sys._getframe().f_lineno)
        invoiceSn = gl.get_value('invoiceSn')
        invoiceSn2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_if(invoiceSn, invoiceSn2, "列表页发货编号", "采购方品检")

        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[3]')
        self.check_information_if(purchaser_name, purchaser_name_2, "列表中fa货单位", "采购方品检")

        agent_name = gl.get_value('agent_name')
        purchaser_name = gl.get_value('purchaser_name')
        agent_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_2, "列表中代理方", "采购方品检")

        contract_sum1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum1, "列表中发货金额", "采购方品检")
        state_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('待品检', state_2, "查看发货单状态", "采购方品检")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button'
            , "点击待品检-查看", "采购方品检", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "品检单列表", "品检单详情", "采购方品检", "采购管理详情页一级目录",
                           "采购管理详情页二级目录", "采购管理详情页三级目录")
        navigation_1 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[1]/div[3]/div')
        self.check_information_if('待收货', navigation_1, '收货详情第一步导航信息', '采购方品检')
        navigation_2 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[2]/div[3]/div')
        self.check_information_if('待品检', navigation_2, '收货详情第二步导航信息', '采购方品检')
        navigation_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[3]/div[3]/div')
        self.check_information_if("待入库", navigation_3, '收货详情第三步导航信息', '采购方品检')
        navigation_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[4]/div[3]/div')
        self.check_information_if("入库完成", navigation_3, '收货详情第四步导航信息', '采购方品检')
        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)  #方电话

        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "发货单位", "采购方品检")

        purchaser_name_page_1 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "采购方品检",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "采购方品检")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_address = gl.get_value('purchaser_address')
        purchaserAdress = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress, "发货单位：详情页", "采购方品检")

        purchaser_phone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "发货单位电话", "采购方品检")
        total_Amount = gl.get_value('total_Amount')

        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位-详情页", "采购方品检")

        purchaser_name_page_1 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "采购方品检",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "采购方品检")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_address = gl.get_value('purchaser_address')
        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址-详情页", "采购方品检")

        purchaser_phone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "收货单位电话：详情页", "采购方品检")

        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p', sys._getframe().f_lineno)
        price_sum = re_int1(price_sum)
        self.check_information_if(str(total_Amount), str(price_sum), "获取详情页中商品总价", "采购方品检")
        try:
            Cp().slide_("555", sys._getframe().f_lineno)
            logistiCpSn = gl.get_value('logistiCpSn')  # 物流公司信息
            companyName = gl.get_value('companyName')  # 物流单号信息
            logistiCp_img = gl.get_value('logistiCp_img')  # 详情页中物流单图片
            invoiceApply_img = gl.get_value('invoiceApply_img')  # 详情页中出货单图片
            companyName_1 = driver.find_element_by_xpath(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[1]/div[1]/div[2]').text
            self.check_information_if(companyName, companyName_1, "详情页中物流公司信息", "采购方品检")
            print("校验是否为物流配送，获取物流公司信息：%s " % companyName)
            logistiCpSn_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[1]/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(logistiCpSn, logistiCpSn_1, "详情页中物流单号信息", "采购方品检")
            logistiCp_img_1 = Cp().xpath_src_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_re(logistiCp_img, logistiCp_img_1, "详情页中物流单图片", "采购方品检")
            invoiceApply_img_1 = Cp().xpath_src_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_if(invoiceApply_img, invoiceApply_img_1, "详情页中出货单图片", "采购方品检")
            Cp().slide_("1900", sys._getframe().f_lineno)

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "采购方品检")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "采购方品检")

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "采购方品检")

            shipment_time = gl.get_value('shipment_time')
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中出货时间", "采购方品检")

            purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)  #方926链号
            record_state1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已收货', record_state1, "操作记录中出货状态", '采购方品检')

            record_operator1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '采购方品检')

            record_time1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '采购方品检')

            shipment_time = gl.get_value('shipment_time')  # 出货时间
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中出货时间", "采购方品检")

            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[5]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中收货时间", "采购方品检")

            Cp().xpath_keys_ENTER(xpath_front_2 + '/div/div[2]/div[6]/span/button[2]', "点击确认品检",
                                                  "采购方品检",
                                                  "云平台‘采购方’", sys._getframe().f_lineno)
            Cp().xpath_click_(
                '//div[@class="ant-modal-confirm-btns"]/button[2]',
                "再次确认品检", "采购方品检", "云平台‘采购方’", sys._getframe().f_lineno)
            time.sleep(2)

            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[6]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中品检时间", "采购方品检")

        except Exception:
            Cp().slide_("555", sys._getframe().f_lineno)
            distribution_mode = gl.get_value('distribution_mode')
            distribution_mode_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(distribution_mode, distribution_mode_1, "详情页中出货单编号", "采购方品检")

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "采购方品检")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "采购方品检")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "采购方品检")

            shipment_time = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "采购方品检")

            purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)  #方926链号
            record_state1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已收货', record_state1, "操作记录中未出货状态", '采购方品检')

            record_operator1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '采购方品检')

            record_time1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '采购方品检')

            shipment_time = gl.get_value('shipment_time')  # 出货时间
            shipment_time_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中出货时间", "采购方品检")

            shipment_time = gl.get_value('shipment_time')  # 收货时间
            shipment_time_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[5]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中收货时间", "采购方品检")

            Cp().xpath_keys_ENTER('//button[2]', "点击确认品检", "采购方品检", "云平台‘采购方’",
                                                  sys._getframe().f_lineno)
            Cp().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认品检",
                                              "采购方品检", "云平台‘采购方’", sys._getframe().f_lineno)

            time.sleep(2)
            Cp().slide_("500")
            shipment_time_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[6]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中收货时间", "采购方品检")

    # 采购方入库
    def warehousing(self):  # Warehousing
        driver = self.driver
        Cp().slide_("0")
        print("*****采购方入库*****")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[2]', "点击进入代采收货管理", "采购方入库", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        self.catalog_two(driver, "代采管理", "收货单列表", "采购方入库", "收货单列表页一级目录", "收货单列表页二级目录")
        self.list_five(driver, "所有收货单", "待收货", "待品检", "待入库", "已入库", "采购方入库", "代采管理-全部列表",
                       "代采管理-待收货列表", "代采管理-待品检列表", "代采管理-待入库列表", "代采管理-已入库列表")

        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]',
                                          "点击进入待入库", "采购方入库", "云平台‘采购方’", sys._getframe().f_lineno)
        invoiceSn = gl.get_value('invoiceSn')
        invoiceSn2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[2]')
        self.check_information_if(invoiceSn, invoiceSn2, "列表页发货编号", "采购方入库")

        purchaser_name = gl.get_value('purchaser_name')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[3]')
        self.check_information_if(purchaser_name, purchaser_name_2, "列表中fa货单位", "采购方入库")

        agent_name = gl.get_value('agent_name')
        purchaser_name = gl.get_value('purchaser_name')
        agent_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]')
        self.check_information_if(agent_name, agent_2, "列表中代理方", "采购方入库")

        contract_sum1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]')
        total_Amount = gl.get_value('total_Amount')
        self.check_information_if('￥%s.00'%total_Amount, contract_sum1, "列表中发货金额", "采购方入库")
        state_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]')
        self.check_information_if('待入库', state_2, "查看发货单状态", "采购方入库")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button'
            , "点击待品检-查看", "采购方入库", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        self.catalog_three(driver, "代采管理", "收货单列表", "收货单详情", "采购方入库", "采购管理详情页一级目录",
                           "采购管理详情页二级目录", "采购管理详情页三级目录")
        navigation_1 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[1]/div[3]/div')
        self.check_information_if('待收货', navigation_1, '收货详情第一步导航信息', '采购方入库')
        navigation_2 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[2]/div[3]/div')
        self.check_information_if('待品检', navigation_2, '收货详情第二步导航信息', '采购方入库')
        navigation_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[3]/div[3]/div')
        self.check_information_if("待入库", navigation_3, '收货详情第三步导航信息', '采购方入库')
        navigation_3 = Cp().xpath_text_(
            xpath_front + '/div/div[1]/div/div/div/div/div/div[4]/div[3]/div')
        self.check_information_if("入库完成", navigation_3, '收货详情第四步导航信息', '采购方入库')

        purchaser_phone = gl.get_value('purchaser_phone')  # 甲（采购）方电话
        purchaser_phone = gl.get_value('purchaser_phone')  # 丙（销售)  #方电话

        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]')
        self.check_information_if(purchaser_name, purchaser_name_1, "发货单位", "采购方入库")

        purchaser_name_page_1 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "采购方入库",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "采购方入库")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_address = gl.get_value('purchaser_address')
        purchaserAdress = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]')
        self.check_information_if(purchaser_address, purchaserAdress, "发货单位：详情页", "采购方入库")

        purchaser_phone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[3]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "发货单位电话", "采购方入库")
        total_Amount = gl.get_value('total_Amount')

        purchaser_name_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        self.check_information_if(purchaser_name, purchaser_name_1, "收货单位-详情页", "采购方入库")

        purchaser_name_page_1 = Cp().xpath_href_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[4]/div[2]/a')
        new_execute_script(purchaser_name_page_1)
        self.catalog_three(driver, "客户管理", "客户列表", "客户详情", "采购方入库",
                           "客户管理页一级目录", "客户管理页二级目录", '客户管理页三级目录')
        purchaser_name_2 = Cp().xpath_text_(
            xpath_front + '/div/div/div[1]/h2', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaser_name_2, "新页面中销售方企业名称信息", "采购方入库")
        # 定位回原来的页面
        driver.switch_to.window(driver.window_handles[0])

        purchaser_address = gl.get_value('purchaser_address')
        purchaser_address_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[5]/div[2]')
        self.check_information_if(purchaser_address, purchaser_address_1, "收货地址-详情页", "采购方入库")

        purchaser_phone_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[6]/div[2]')
        self.check_information_if(purchaser_phone, purchaser_phone_1, "收货单位电话：详情页", "采购方入库")

        price_sum = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[2]/div/p', sys._getframe().f_lineno)
        price_sum = re_int1(price_sum)
        self.check_information_if(str(total_Amount), str(price_sum), "获取详情页中商品总价", "采购方入库")
        try:
            Cp().slide_("555", sys._getframe().f_lineno)
            logistiCpSn = gl.get_value('logistiCpSn')  # 物流公司信息
            companyName = gl.get_value('companyName')  # 物流单号信息
            logistiCp_img = gl.get_value('logistiCp_img')  # 详情页中物流单图片
            invoiceApply_img = gl.get_value('invoiceApply_img')  # 详情页中出货单图片
            companyName_1 = driver.find_element_by_xpath(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[1]/div[1]/div[2]').text
            self.check_information_if(companyName, companyName_1, "详情页中物流公司信息", "采购方入库")
            print("校验是否为物流配送，获取物流公司信息：%s " % companyName)
            logistiCpSn_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[1]/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(logistiCpSn, logistiCpSn_1, "详情页中物流单号信息", "采购方入库")
            logistiCp_img_1 = Cp().xpath_src_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[2]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_re(logistiCp_img, logistiCp_img_1, "详情页中物流单图片", "采购方入库")
            invoiceApply_img_1 = Cp().xpath_src_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div[3]/div/div/div/div[1]/img', sys._getframe().f_lineno)
            self.check_information_if(invoiceApply_img, invoiceApply_img_1, "详情页中出货单图片", "采购方入库")
            Cp().slide_("1900", sys._getframe().f_lineno)

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "采购方入库")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "采购方入库")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "采购方入库")

            shipment_time = gl.get_value('shipment_time')
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中出货时间", "采购方入库")

            purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)  #方926链号
            record_state1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已品鉴', record_state1, "操作记录中未出货状态", '采购方入库')

            record_operator1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '采购方入库')

            record_time1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '采购方入库')

            shipment_time = gl.get_value('shipment_time')  # 出货时间
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中出货时间", "采购方入库")

            shipment_time = gl.get_value('shipment_time')  # 收货时间
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[5]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中收货时间", "采购方入库")

            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[6]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中品检时间", "采购方入库")

            Cp().xpath_keys_ENTER(xpath_front_2 + '/div/div[2]/div[6]/span/button[2]', "点击确认入库",
                                                  "采购方入库",
                                                  "云平台‘采购方’", sys._getframe().f_lineno)
            Cp().xpath_click_(
                '//div[@class="ant-modal-confirm-btns"]/button[2]',
                "再次确认入库", "采购方入库", "云平台‘采购方’", sys._getframe().f_lineno)
            time.sleep(3)
            shipment_time = gl.get_value('shipment_time')
            shipment_time_1 = Cp().xpath_text_(
                xpath_front_2 + '/div/div[2]/div[4]/div[2]/div/div/div[7]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中入库时间", "采购方入库")

        except Exception:
            Cp().slide_("555", sys._getframe().f_lineno)
            distribution_mode = gl.get_value('distribution_mode')
            distribution_mode_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[3]/div[2]/div/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(distribution_mode, distribution_mode_1, "详情页中出货单编号", "采购方入库")

            invoiceSn = gl.get_value('invoiceSn')  # 出货单编号 DO
            invoiceSn_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[1]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(invoiceSn, invoiceSn_1, "详情页中出货单编号", "采购方入库")

            settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
            settlement_date_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[2]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(settlement_date, settlement_date_1, "详情页中账期", "采购方入库")

            contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
            contractnumber_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[3]/div[2]', sys._getframe().f_lineno)
            self.check_information_if(contractnumber, contractnumber_1, "详情页中合同编号", "采购方入库")

            shipment_time = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[4]/div[2]', sys._getframe().f_lineno)
            self.check_information_if('', shipment_time, "详情页中出货时间", "采购方入库")

            purchaser_name = gl.get_value('purchaser_name')  # 丙（销售)  #方926链号
            record_state1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[1]', sys._getframe().f_lineno)
            self.check_information_if('采购商已品鉴', record_state1, "操作记录中未出货状态", '采购方入库')

            record_operator1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[2]', sys._getframe().f_lineno)
            self.check_information_if(purchaser_name, record_operator1, "操作记录中发起申请操作人", '采购方入库')

            record_time1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[5]/div[2]/div/ul/li/div[3]/div/div[3]', sys._getframe().f_lineno)
            self.check_information_time(record_time1, "操作记录中发起申请时间", '采购方入库')

            shipment_time_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[5]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中收货时间", "采购方入库")

            shipment_time_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[6]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中品检时间", "采购方入库")

            Cp().xpath_keys_ENTER('//button[2]', "点击确认入库", "采购方入库", "云平台‘采购方’",
                                                  sys._getframe().f_lineno)
            Cp().xpath_click_('//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认入库",
                                              "采购方入库", "云平台‘采购方’", sys._getframe().f_lineno)
            time.sleep(3)
            Cp().slide_("500")
            shipment_time_1 = Cp().xpath_text_(
                xpath_front + '/div/div[2]/div[4]/div[2]/div/div/div[7]/div[2]', sys._getframe().f_lineno)
            self.check_information_time(shipment_time_1, "详情页中入库时间", "采购方入库")

    def invoice(self):  # 采购方收票
        driver = self.driver
        print("*****采购方收票*****")
        Cp().slide_("200")
        Cp().xpath_click_('//*[@id="2$Menu"]/li[3]', "点击进入代采收票管理", "采购方收票", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[2]'
                                          , "点击进入待收票", "采购方收票", "云平台‘采购方’", sys._getframe().f_lineno)
        self.catalog_two(driver, "代采管理", "收票信息", "点击进入待收票", "收票信息列表页一级目录", "收票信息列表页二级目录")
        self.list_three(driver, "全部", "待收票", "已收票", "代采方通过收货申请", "代采管理-全部列表", "代采管理-待收票列表", "代采管理-已收票列表")

        time.sleep(2)
        purchaser_name = gl.get_value('purchaser_name')
        agent_name = gl.get_value('agent_name')
        total_Amount = gl.get_value('total_Amount')
        send_receiptSn = gl.get_value('send_receiptSn')
        send_receiptSn_ = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[2]', sys._getframe().f_lineno)
        self.check_information_re(send_receiptSn, send_receiptSn_, "列表页寄票编号", '采购方收票')
        purchaserName = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[3]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaserName, "列表页发货单位", '采购方收票')
        agentName = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[4]', sys._getframe().f_lineno)
        self.check_information_if(agent_name, agentName, "列表页寄票单位", '采购方收票')
        totalAmount = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[5]', sys._getframe().f_lineno)
        self.check_information_re(str(total_Amount), totalAmount, "列表页寄票金额", '采购方收票')
        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[6]', sys._getframe().f_lineno)
        self.check_information_if('采购商待收票', state_1, "列表页寄票状态", '采购方收票')
        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr/td[7]/button', "点击进入待收票-查看",
            "采购方收票", "云平台‘采购方’", sys._getframe().f_lineno)

        time.sleep(2)
        self.catalog_three(driver, "代采管理", "收票信息", "收票详情", "采购方收票", "收票信息列表页一级目录"
                           , "收票信息列表页二级目录", "收票信息列表页三级目录")
        navigation_1 = Cp().xpath_text_(xpath_front + '/div/div[1]/div/div/div/div/div[1]/div[3]/div')
        self.check_information_if('待收发票', navigation_1, "出货详情第一步导航信息", "采购方收票")
        navigation_2 = Cp().xpath_text_(xpath_front + '/div/div[1]/div/div/div/div/div[2]/div[3]/div')
        self.check_information_if('已收发票', navigation_2, "出货详情第二步导航信息", "采购方收票")

        send_receiptSn = gl.get_value('send_receiptSn')
        send_receiptSn_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[1]/div[2]',
            sys._getframe().f_lineno)
        self.check_information_if(send_receiptSn, send_receiptSn_1, "详情页寄票编号", '采购方收票')
        purchaser_name = gl.get_value('purchaser_name')
        purchaserName = Cp().xpath_text_(xpath_front + '/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]',
                                                        sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaserName, "详情页寄票单位", '采购方收票')

        contractnumber = gl.get_value('contractnumber')
        contractSn_1 = Cp().xpath_text_(xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]',
                                                        sys._getframe().f_lineno)
        self.check_information_if(contractnumber, contractSn_1, "详情页代理合同", '采购方收票')

        invoiceSn = gl.get_value('invoiceSn')
        invoiceSn_1 = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/a',
            sys._getframe().f_lineno)
        self.check_information_if(invoiceSn, invoiceSn_1, "详情页发货编号", '采购方收票')

        Cp().xpath_click_(xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/a',
                                          "点击详情页发货编号", '采购方收票', "云平台‘发起方’", sys._getframe().f_lineno)
        time.sleep(1)
        self.catalog_three(driver, "代销管理", "出货单列表", "出货单详情", "采购方收票",
                           "出货管理页一级目录", "出货管理页二级目录", '出货管理页三级目录')
        driver.back()
        time.sleep(1)

        invoiceReceiptSn = Cp().xpath_text_(
            xpath_front + '/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]',
            sys._getframe().f_lineno)
        self.check_information_if(send_receiptSn, invoiceReceiptSn, "详情页寄票单号", '采购方收票')

        Cp().xpath_click_(xpath_front + '/div/div[2]/div[4]/button', "点击确认收票", "采购方收票", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        Cp().xpath_click_(
            '//div[@class="ant-modal-confirm-btns"]/button[2]', "再次确认收票", "采购方收票",
            "云平台‘采购方’", sys._getframe().f_lineno)

        time.sleep(2)
        Cp().xpath_click_('//*[@id="2$Menu"]/li[3]', "点击进入代采收票管理", "采购方收票", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        time.sleep(1)
        Cp().xpath_click_(xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]'
                                          , "点击进入yi收票", "采购方收票", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        send_receiptSn = gl.get_value('send_receiptSn')
        purchaser_name = gl.get_value('purchaser_name')
        agent_name = gl.get_value('agent_name')
        total_Amount = gl.get_value('total_Amount')
        send_receiptSn_2 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[2]', sys._getframe().f_lineno)
        self.check_information_re(send_receiptSn, send_receiptSn_2, "列表页寄票编号", '采购方收票')
        purchaserName = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]', sys._getframe().f_lineno)
        self.check_information_if(purchaser_name, purchaserName, "列表页发货单位", '采购方收票')
        agentName = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[4]', sys._getframe().f_lineno)
        self.check_information_if(agent_name, agentName, "列表页寄票单位", '采购方收票')
        totalAmount = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]', sys._getframe().f_lineno)
        self.check_information_re(str(total_Amount), totalAmount, "列表页寄票金额", '采购方收票')
        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]', sys._getframe().f_lineno)
        self.check_information_if('采购商已收票', state_1, "列表页寄票状态", '采购方收票')

    def payment(self):
        driver = self.driver
        print("*****采购方付款*****")
        Cp().slide_("200")
        Cp().xpath_click_('//*[@id="4$Menu"]/li[1]', "点击进入代采付款列表", "采购方付款", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        Cp().xpath_click_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[3]', "点击进入待付款", "采购方付款", "云平台‘采购方’",
            sys._getframe().f_lineno)

        self.catalog_two(driver, "收款付款", "付款列表", "点击进入待付款", "付款页一级目录", "付款页二级目录")
        self.list_four(driver, "全部", "已逾期", "待付款", "已付款", "采购方付款", "收款付款-全部列表",
                       "收款付款-已逾期列表", "收款付款-待付款列表", "收款付款-已付款列表")

        invoicePaymentSn = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[2]')
        self.check_information_re("FK", invoicePaymentSn, "付款编号", "采购方付款")

        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        payeeName_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[3]')
        self.check_information_if(payeeName_1, agent_name, "收款单位", "采购方付款")

        total_Amount = gl.get_value('total_Amount')  # 货品总价
        invoiceTotalAmount = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[4]')
        self.check_information_re(str(total_Amount), invoiceTotalAmount, "货单金额", "采购方付款")

        time1_check = datetime.date.today()  # 获取当前时间
        settlement_date = gl.get_value("settlement_date")  # 结算方式 票到XX天
        settlement_date_int = re_sub_(settlement_date)  # 显示为12,500.00 正则筛选
        settlementTime = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[5]')
        time2_check = time1_check + datetime.timedelta(days=int(settlement_date_int))
        self.check_information_if(str(time2_check), settlementTime, "账款到期日", "采购方付款")

        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]')
        self.check_information_if('采购商待付款', state_1, "状态", "采购方付款")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击待付款-查看", "采购方付款",
            "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)

        self.catalog_three(driver, "收款付款", "付款列表", "付款详情", "采购方付款", "付款页一级目录", "付款页二级目录", '付款页一级目录')

        total_Amount = gl.get_value('total_Amount')  # 货品总价
        invoiceTotalAmount_ = Cp().xpath_text_(xpath_front + '/div/form/div/div[1]/div[1]/span')
        invoiceTotalAmount_ = re_sub_(invoiceTotalAmount_)
        self.check_information_re(str(total_Amount),invoiceTotalAmount_,  "货品总价-详情页", "采购方付款")

        state_2 = Cp().xpath_text_(xpath_front + '/div/form/div/div[1]/div[2]/span')
        self.check_information_if('采购商待付款', state_2, "状态", "采购方付款")

        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        payeeName_2 = Cp().xpath_text_('//*[@id="payeeName"]')
        self.check_information_if(payeeName_2, agent_name, "收款单位-详情页", "采购方付款")

        invoiceTotalAmount_2 = Cp().xpath_text_('//*[@id="invoiceTotalAmount"]')
        invoiceTotalAmount_2 = re_sub_(invoiceTotalAmount_2)
        self.check_information_re(str(total_Amount), invoiceTotalAmount_2, "货单金额-详情页", "采购方付款")

        deliveryDate = Cp().xpath_text_('//*[@id="deliveryDate"]/div')
        self.check_information_if(str(time1_check), deliveryDate, "出货日期", "采购方付款")

        settlementTime_1 = Cp().xpath_text_('//*[@id="settlementTime"]/div')
        self.check_information_if(str(time2_check), settlementTime_1, "账款到期日", "采购方付款")

        contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
        contractSn_1 = Cp().xpath_text_('//*[@id="contractSn"]')
        self.check_information_if(contractnumber, contractSn_1, "代理合同", "采购方付款")

        invoiceApplySn = gl.get_value('invoiceApplySn')  # DF 发货单
        invoiceSn_1 = Cp().xpath_text_('//*[@id="invoiceSn"]')
        self.check_information_if(invoiceApplySn, invoiceSn_1, "货单编号", "采购方付款")

        operation_record = Cp().xpath_text_(xpath_front + '/div/form/div/div[3]/div[3]/div/div[2]')
        self.check_information_if('暂无记录...', operation_record, "未付款前操作记录", "采购方付款")

        Cp().xpath_click_(
            xpath_front + '/div/form/div/div[5]/button', "未上传图片点击提交", "采购方付款", "云平台‘采购方’", sys._getframe().f_lineno)
        tips_info = Cp().xpath_text_(
            xpath_front + '/div/form/div/div[2]/div/div[2]/div/div/div[4]/div/div/div[2]/div/div')
        self.check_information_if('请上传付款凭证', tips_info, "提示信息", "采购方付款")
        time.sleep(1)

        Cp().xpath_send_(
            xpath_front + '/div/form/div/div[2]/div/div[2]/div/div/div[4]/div/div/div[2]/div/span/div/span/div/span/'
                          'input[@type="file"]', "E:\shangwo\图片信息\合同1.jpg")  # 上传图片
        Cp().is_toast_exist("上传图片", "采购方付款", "云平台‘采购方’", sys._getframe().f_lineno)
        time.sleep(2)
        Cp().xpath_click_(
            xpath_front + '/div/form/div/div[5]/button', "已上传图片点击提交", "采购方付款", "云平台‘采购方’", sys._getframe().f_lineno)
        Cp().xpath_click_(xpath_front + '/div/form/div/div[5]/button', "确认提交", "采购方付款",
                                          "云平台‘采购方’", sys._getframe().f_lineno)

        print("******查看已付款的付款单信息******")
        Cp().xpath_click_('//*[@id="4$Menu"]/li[1]', "点击进入代采付款列表", "查看已付款的付款单信息", "云平台‘采购方’",
                                          sys._getframe().f_lineno)
        Cp().xpath_click_(
            xpath_front + '/div/div[1]/div/div[1]/div/div/div/div/div[1]/div[4]', "点击进入已付款", "查看已付款的付款单信息", "云平台‘采购方’",
            sys._getframe().f_lineno)

        state_1 = Cp().xpath_text_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]')
        self.check_information_if('代理商待收款', state_1, "状态", "查看已付款的付款单信息")

        Cp().xpath_click_(
            xpath_front + '/div/div[3]/div/div/div/div/div/div/table/tbody/tr[1]/td[7]/button', "点击待付款-查看",
            "查看已付款的付款单信息",
            "云平台‘采购方’", sys._getframe().f_lineno)

        self.catalog_three(driver, "收款付款", "付款列表", "付款详情", "查看已付款的付款单信息", "付款页一级目录", "付款页二级目录", '付款页一级目录')

        total_Amount = gl.get_value('total_Amount')  # 货品总价
        invoiceTotalAmount_ = Cp().xpath_text_(xpath_front + '/div/form/div/div[1]/div[1]/span')
        invoiceTotalAmount_ = re_sub_(invoiceTotalAmount_)
        self.check_information_re(str(total_Amount),invoiceTotalAmount_,  "货品总价-详情页", "查看已付款的付款单信息")

        state_2 = Cp().xpath_text_(xpath_front + '/div/form/div/div[1]/div[2]/span')
        self.check_information_if('代理商待收款', state_2, "状态", "查看已付款的付款单信息")

        agent_name = gl.get_value('agent_name')  # 乙（代理)方企业名
        payeeName_2 = Cp().xpath_text_('//*[@id="payeeName"]')
        self.check_information_if(payeeName_2, agent_name, "收款单位-详情页", "查看已付款的付款单信息")

        invoiceTotalAmount_2 = Cp().xpath_text_('//*[@id="invoiceTotalAmount"]')
        invoiceTotalAmount_2 = re_sub_(invoiceTotalAmount_2)
        self.check_information_re(str(total_Amount), invoiceTotalAmount_2, "货单金额-详情页", "查看已付款的付款单信息")

        deliveryDate = Cp().xpath_text_('//*[@id="deliveryDate"]/div')
        self.check_information_if(str(time1_check), deliveryDate, "出货日期", "查看已付款的付款单信息")

        settlementTime_1 = Cp().xpath_text_('//*[@id="settlementTime"]/div')
        self.check_information_if(str(time2_check), settlementTime_1, "账款到期日", "查看已付款的付款单信息")

        contractnumber = gl.get_value('contractnumber')  # 合同编号 CT
        contractSn_1 = Cp().xpath_text_('//*[@id="contractSn"]')
        self.check_information_if(contractnumber, contractSn_1, "代理合同", "查看已付款的付款单信息")

        invoiceApplySn = gl.get_value('invoiceApplySn')  # DF 发货单
        invoiceSn_1 = Cp().xpath_text_('//*[@id="invoiceSn"]')
        self.check_information_if(invoiceApplySn, invoiceSn_1, "货单编号", "查看已付款的付款单信息")

        record_state1 = Cp().xpath_text_(
            xpath_front + '/div/form/div/div[3]/div[3]/div/ul/li/div[3]/div/div[1]')
        self.check_information_if('采购商付款', record_state1, '操作记录-状态', "查看已付款的付款单信息")

        record_time1 = Cp().xpath_text_(
            xpath_front + '/div/form/div/div[3]/div[3]/div/ul/li/div[3]/div/div[3]')
        self.check_information_time(record_time1, '操作记录-时间', "查看已付款的付款单信息")

        purchaser_name = gl.get_value('purchaser_name')  # 甲（采购）方企业名
        record_operator1 = Cp().xpath_text_(
            xpath_front + '/div/form/div/div[3]/div[3]/div/ul/li/div[3]/div/div[2]')
        self.check_information_if(purchaser_name, record_operator1, '操作记录-操作者', "查看已付款的付款单信息")

    def run(self):  # 采购方登录
        # self.driver.get(self.start_url)
        self.login()

    def run1(self):  # 合作方同意委托
        self.cooperation_agree_contract()

    def run1_1(self):  # 合作方拒绝委托
        self.refuse_entrust()

    def run1_1_1(self):  # 合作方查看委托
        self.see_cooperation_refuse()

    def run1_2(self):
        self.see_cooperation_adopt()  # 校验代理方通过审批后的合同信息

    def run2(self):  # 代采方通过发货申请
        self.delivery_application()

    def run2_1(self):  # 代采方拒绝发货申请
        self.refuse_delivery_application()

    def run2_2(self):  # 代采方查看被代理方拒绝的发货申请
        self.refuse_application_1()

    def run2_3(self):  # 代采方查看被代理方tongugo的发货申请
        self.see_application_adopt()

    def run3(self):  # 采购方收货
        self.receiving_goods()

    def run3_1(self):  # 采购方品检
        self.inspection()

    def run3_2(self):  # 采购方入库
        self.warehousing()

    def run4(self):  # 采购方收票
        self.invoice()

    def run5(self):  # 采购方付款
        self.payment()

    def run_excel(self):
        Cp().excel_write()  # 写入excel


if __name__ == '__main__':
    caigou = PC_926_purchaser()
    caigou.run()  # 采购方登录
    caigou.run1_1()  # 合作方拒绝委托
    caigou.run1()  # 合作方同意委托
    caigou.run1_2()  # 校验代理方通过审批后的合同信息
    caigou.run1_1_1()  # 代采方查看被代理方拒绝的委托信息
    caigou.run2_1()  # 代采方拒绝发货申请
    # caigou.run2()  # 代采方通过发货申请
    # caigou.run2_2()  # 代采方查看被代理方拒绝的发货申请
    # caigou.run2_3()  # 代采方查看被代理方tongugo的发货申请
    # caigou.run3()  # 采购方收货
    caigou.run3_1()  # 采购方品检
    caigou.run3_2()  # 采购方入库
    # caigou.run4()  # 采购方收票
    caigou.run5()  # 采购方付款
    # caigou.run_excel()
