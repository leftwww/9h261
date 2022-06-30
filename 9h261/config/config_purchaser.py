# -- coding: utf-8 --
# @Author : Zw
# @File : config_pc_purchaser.py

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

# from config.config_supplier import Config_pc_supplier
# from config.config_agent import Config_pc_agent
import config.config_agent
import config.config_supplier
from config import http_

from xlrd import open_workbook
from xlutils.copy import copy

import re, sys, os, time, traceback
import pyautogui as pag

def current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "-合作方-"
    return current_time


def tes1t_time():
    test_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    return test_time


def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

n = 0



class Config_pc_purchaser():
    # start_url = "http://web.926.net.cn"  # 生产
    # start_url = 'http://926-web-test.926.net.cn/#/'  # 测试
    # start_url = 'http://10.10.1.62:3002/#/'  # 测试
    # start_url = 'http://pre-web.926.net.cn/'  # 预生产
    start_url = http_.start_url
    driver = webdriver.Chrome()
    driver.implicitly_wait(0.2)
    book = open_workbook("C:\\Users\Zuow\Desktop\\test_case.xlsx")
    news = []

    # 校验页面提示信息是否为报错提示
    def is_toast_exist(self, text, model, identity, *args):
        driver = self.driver
        if type(args[0]) == int:
            args_0 = str(args[0])
        else:
            args_0 = args[0]
        object_name1 = sys._getframe().f_code.co_name
        if re.findall("click", args_0) or re.findall("key", args_0):
            time.sleep(1.0)
        else:
            time.sleep(0.1)
        news = self.news
        try:
            tips = driver.find_element_by_xpath('//div[@class="ant-message-notice"]').text
            if tips == '网络开小差了~' or tips == "网络错误":  # 出现异常
                adopt_ = "no"
                # driver.save_screenshot('C:\\Users\Zuow\Desktop' + '\\' + tips + current_time() + '.png')
                print(current_time() + "子模块为:%s" % model, "用例标题:%s" % text, "执行结果:%s" % adopt_, "捕获信息：%s" % tips)
                news.append(text)  # 用例标题
                news.append(adopt_)  # 执行结果
                news.append(tips)  # 捕获信息
                news.append(model)  # 子模块
                news.append(identity)  # 大模块
                if tips == "网络错误":
                    # 截屏功能
                    img = pag.screenshot()
                    img.save('foo.png')
                    pag.screenshot('foo.png')
                    sys.stdout = Logger('log_pc.txt')
                    print('错误行号', args[0])
                    self.excel_write()
                    sys.exit()
                elif tips == '网络开小差了~' and re.findall("click",args_0) or re.findall("key",args_0):
                    time.sleep(1)
                    driver.refresh()  # 刷新方法 refresh
                    time.sleep(15)
                    globals()[args_0](args[1], text, model, identity, object_name1)  # 再次点击 args[0]=调用的函数名 [1]xpath信息
                    # time.sleep(0.1)
            else:
                adopt_ = "pass"
                print(current_time() + "子模块为:%s" % model, "用例标题:%s" % text, "执行结果:%s" % adopt_, "捕获信息：%s" % tips)
                news.append(text)  # 用例标题
                news.append(adopt_)  # 执行结果
                news.append(tips)  # 捕获信息
                news.append(model)  # 模块
                news.append(identity)  # 大模块
                # time.sleep(0.1)

        except Exception as e:
            tips = ""
            adopt_ = "pass"
            print(current_time() + "子模块为:%s" % model, "用例标题:%s" % text, "执行结果:%s" % adopt_, "捕获信息：%s" % tips)
            news.append(text)  # 用例标题
            news.append(adopt_)  # 执行结果
            news.append(tips)  # 捕获信息
            news.append(model)  # 模块
            news.append(identity)  # 大模块
            # time.sleep(0.1)

    # 校验失败
    def is_page_exist(self, text, model, identity,*args):
        driver = self.driver
        # time.sleep(10)
        news = self.news
        adopt_ = "no"
        tips = ""
        # driver.save_screenshot('C:\\Users\Zuow\Desktop' + '\\' + tips + current_time() + '.png')  # 屏幕截图
        print(current_time() + "子模块为:%s" % model, "用例标题:%s" % text, "执行结果:%s" % adopt_, "捕获信息：%s" % tips)
        news.append(text)  # 用例标题
        news.append(adopt_)  # 执行结果
        news.append(tips)  # 捕获信息
        news.append(model)  # 模块
        news.append(identity)  # 大模块
        # time.sleep(0.1)

    def excel_write(self):
        news = self.news
        book = self.book
        #  复制
        wb = copy(book)
        # 选取表单
        s = wb.get_sheet(0)
        a = 0
        # b = int(len(news) / 2)
        # 写入数据
        # print(int(len(news)))
        while a <= int(len(news) / 5):
            a += 1
            #   2 5 8 11 14
            # a 2 3 4 5  6
            # print((a-1)*3-1)
            s.write((a + 1), 1, a)  # ID
            s.write((a + 1), 2, news[(a - 1) * 5 - 1])  # 模块
            s.write((a + 1), 3, news[(a - 1) * 5 - 2])  # 子模块
            s.write((a + 1), 6, news[(a - 1) * 5 - 5])  # 标题
            s.write((a + 1), 12, news[(a - 1) * 5 - 4])  # 状态
            s.write((a + 1), 13, news[(a - 1) * 5 - 3])  # 备注
            s.write((a + 1), 22, current_time())  # 时间
            # print(a)
        wb.save("C:\\Users\Zuow\Desktop\\test_case_purchaser.xlsx")

    def id_send_(self, data, demo, *args):
        object_name = sys._getframe().f_code.co_name
        driver = self.driver
        try:
            time.sleep(1)
            WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_id(data)).send_keys(demo)
            time.sleep(0.2)

        except Exception as e:
            try:
                driver.refresh()  # 刷新
                time.sleep(15)
                WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_id(data)).send_keys(demo)
                time.sleep(0.2)
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                sys.exit()


    def xpath_text_(self, data,*args):
        object_name = sys._getframe().f_code.co_name
        driver = self.driver
        try:
            xpath_text = WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath(data)).text
            return xpath_text
        except Exception as e:
            try:
                driver.refresh()  # 刷新
                time.sleep(15)
                xpath_text = WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath(data)).text
                return xpath_text
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()

    def xpath_href_(self, data,*args):
        object_name = sys._getframe().f_code.co_name
        driver = self.driver
        try:
            time.sleep(1)
            xpath_text = WebDriverWait(driver, 60).until(
                lambda driver: driver.find_element_by_xpath(data)).get_attribute("href")
            # time.sleep(0.2)
            return xpath_text
        except Exception as e:
            try:
                driver.refresh()  # 刷新
                time.sleep(15)
                xpath_text = WebDriverWait(driver, 60).until(
                    lambda driver: driver.find_element_by_xpath(data)).get_attribute("href")
                return xpath_text
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()

    def xpath_send_(self, data, demo, *args):
        object_name = sys._getframe().f_code.co_name
        driver = self.driver
        try:
            time.sleep(1)
            WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath(data)).send_keys(demo)
            time.sleep(0.2)

        except Exception as e:
            try:
                driver.refresh()  # 刷新
                time.sleep(15)
                WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath(data)).send_keys(demo)
                time.sleep(0.2)
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()


    def id_clear_(self, data,*args):
        object_name = sys._getframe().f_code.co_name
        driver = self.driver
        try:
            time.sleep(0.2)
            WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_id(data)).clear()
        except Exception as e:
            try:
                driver.refresh()  # 刷新
                time.sleep(15)
                WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath(data))
                time.sleep(0.2)
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()


    def xpath_clear_(self, data,*args):
        object_name = sys._getframe().f_code.co_name
        driver = self.driver
        try:
            time.sleep(0.2)
            WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath(data)).clear()
        except Exception as e:
            try:
                driver.refresh()  # 刷新
                time.sleep(15)
                WebDriverWait(driver, 60).until(lambda driver: driver.find_element_by_xpath(data)).clear()
                time.sleep(0.2)
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()

    def name_click_(self, data, text, model, identity, *args):
        object_name = sys._getframe().f_code.co_name
        global n
        driver = self.driver
        try:
            time.sleep(1)
            WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_class_name(data)).click()
            time.sleep(0.2)
            if type(args[0]) == int:  # 正常走
                self.is_toast_exist(text, model, identity, object_name, data)
            elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击
                n += 1
                print('出现开小差后重新点击')
                self.is_toast_exist(text, model, identity, object_name, data)
        except Exception as e:
            try:
                driver.refresh()  # 刷新方法 refresh
                time.sleep(15)
                WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_class_name(data)).click()
                print('获取失败后重新点击')
                time.sleep(0.2)
                if type(args[0]) == int:  # 正常走
                    self.is_toast_exist(text, model, identity, object_name, data)
                elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击
                    n += 1
                    self.is_toast_exist(text, model, identity, object_name, data)
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()
        n = 0

    def xpath_click_(self, data, text, model, identity, *args):
        object_name = sys._getframe().f_code.co_name
        global n
        driver = self.driver
        try:
            time.sleep(1)
            WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_xpath(data)).click()
            time.sleep(0.2)
            if type(args[0]) == int:  # 正常走
                self.is_toast_exist(text, model, identity, object_name, data)
            elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击
                n += 1
                print('出现开小差后重新点击')
                self.is_toast_exist(text, model, identity, object_name, data)
        except Exception as e:
            try:
                driver.refresh()  # 刷新方法 refresh
                time.sleep(15)
                WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_xpath(data)).click()
                print('获取失败后重新点击')
                time.sleep(0.2)
                if type(args[0]) == int:  # 正常走
                    self.is_toast_exist(text, model, identity, object_name, data)
                elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击
                    n += 1
                    self.is_toast_exist(text, model, identity, object_name, data)
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()
        n = 0

    def xpath_keys_(self, data, text, model, identity, *args):
        global n
        object_name = sys._getframe().f_code.co_name
        driver = self.driver
        try:
            time.sleep(1)
            WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_xpath(data)).send_keys(Keys.SPACE)  # Keys.ENTER
            time.sleep(0.2)
            if type(args[0]) == int:  # 正常走
                self.is_toast_exist(text, model, identity, object_name, data)
            elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击
                n += 1
                self.is_toast_exist(text, model, identity, object_name, data)
        except Exception as e:
            try:
                driver.refresh()  # 刷新方法 refresh
                time.sleep(15)
                WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_xpath(data)).send_keys(Keys.SPACE)  # Keys.ENTER
                time.sleep(0.2)
                if args is None:
                    self.is_toast_exist(text, model, identity, object_name, data)
                elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击:
                    n += 1
                    self.is_toast_exist(text, model, identity, object_name, data)

            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()
        n = 0

    def xpath_keys_ENTER(self, data, text, model, identity, *args):
        global n
        object_name = sys._getframe().f_code.co_name
        driver = self.driver
        try:
            time.sleep(1)
            WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_xpath(data)).send_keys(Keys.ENTER)  # Keys.ENTER
            time.sleep(0.2)
            if type(args[0]) == int:  # 正常走
                self.is_toast_exist(text, model, identity, object_name, data)
            elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击
                n += 1
                self.is_toast_exist(text, model, identity, object_name, data)
        except Exception as e:
            try:
                driver.refresh()  # 刷新方法 refresh
                time.sleep(15)
                WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_xpath(data)).send_keys(Keys.ENTER)  # Keys.ENTER
                time.sleep(0.2)
                if args is None:
                    self.is_toast_exist(text, model, identity, object_name, data)
                elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击:
                    n += 1
                    self.is_toast_exist(text, model, identity, object_name, data)

            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()
        n = 0

    def text_click_(self, data, text, model, identity, *args):
        object_name = sys._getframe().f_code.co_name
        global n
        driver = self.driver
        try:
            time.sleep(1)
            WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_link_text(data)).click()
            time.sleep(0.2)
            if type(args[0]) == int:  # 正常走
                self.is_toast_exist(text, model, identity, object_name, data)
            elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击
                n += 1
                print('出现开小差后重新点击')
                self.is_toast_exist(text, model, identity, object_name, data)
        except Exception as e:
            try:  # 没获取到重新点击
                driver.refresh()  # 刷新方法 refresh
                time.sleep(15)
                WebDriverWait(driver, 40).until(lambda driver: driver.find_element_by_link_text(data)).click()
                print('获取失败后重新点击')
                time.sleep(0.2)
                if type(args[0]) == int:  # 正常走
                    self.is_toast_exist(text, model, identity, object_name, data)
                elif args[0] == 'is_toast_exist' and n == 0:  # 出现开小差后重新点击
                    n += 1
                    self.is_toast_exist(text, model, identity, object_name, data)
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                sys.exit()

    def xpath_src_(self, data, *args):
        driver = self.driver
        try:
            time.sleep(1)
            xpath_text = WebDriverWait(driver, 40).until(
                lambda driver: driver.find_element_by_xpath(data)).get_attribute("src")
            # time.sleep(0.2)
            return xpath_text
        except Exception as e:
            try:
                driver.refresh()
                time.sleep(15)
                xpath_text = WebDriverWait(driver, 40).until(
                    lambda driver: driver.find_element_by_xpath(data)).get_attribute("src")
                # time.sleep(0.2)
                return xpath_text
            except Exception as e:
                sys.stdout = Logger('log_pc.txt')
                print('错误行号', args[0])
                print('错误信息', traceback.format_exc())
                self.excel_write()
                config.config_supplier.Config_pc_supplier().excel_write()
                config.config_agent.Config_pc_agent().excel_write()
                sys.exit()


    def slide_(self, text,*args):  # 页面滑动：0为顶部，800中间，尾部1800
        driver = self.driver
        time.sleep(1)
        try:
            js = "var q=document.documentElement.scrollTop=%s" % text
            driver.execute_script(js)
            time.sleep(1)
        except Exception as e:
            # print('C:\\Users\Zuow\Desktop' + '\\' + "报错" + current_time() + '.png')
            sys.stdout = Logger('log_pc.txt')
            print('错误行号', args[0])
            print('错误信息', traceback.format_exc())
            self.excel_write()
            config.config_supplier.Config_pc_supplier().excel_write()
            config.config_agent.Config_pc_agent().excel_write()
            sys.exit()



class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a", encoding="UTF-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
