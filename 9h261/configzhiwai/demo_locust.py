from locust import HttpLocust, TaskSet, task
from selenium import webdriver
from multiprocessing import Process
from function import get_authorization, public
from config import http_

import os,time,hashlib

def md5Encode(str_):
    m = hashlib.md5()
    str_ = str(str_)
    m.update(str_.encode('utf-8'))
    print(m.hexdigest())
    return m.hexdigest()

header = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Authorization': Authorization,
            'Referer': 'http://926-web-test.926.net.cn/',
            'Origin': 'http://926-web-test.926.net.cn',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            # 'User-Agent': 'Mozilla5.0 (Windows NT 10.0; Win64; x64) AppleWebKit537.36 (KHTML, like Gecko) Chrome74.0.3729.131 Safari537.36',

        }


token_s = public.get_token(http_.supplier_phone, md5Encode(123456))
token_p = public.get_token(http_.purchaser_phone, md5Encode(123456))
token_a = public.get_token(http_.agent_phone, md5Encode(123456))

# 定义用户行为，继承TaskSet类，用于描述用户行为
# (这个类下面放各种请求，请求是基于requests的，每个方法请求和requests差不多，请求参数、方法、响应对象和requests一样的使用，url这里写的是路径)
# client.get===>requests.get
# client.post===>requests.post
class test_926(TaskSet):
    # task装饰该方法为一个事务方法的参数用于指定该行为的执行权重。参数越大，每次被虚拟用户执行概率越高，不设置默认是1，
    # @task(2)
    # def test_login(self):
        # 定义requests的请求头
        # r是包含所有响应内容的一个对象
        # # todo 登陆云企
        # r = self.client.post('/api/v1/erp/account/mobile', timeout=30, headers=header,data='admin=&appKey=S00101&format=json&openId=&password=%s&phone=%s&sessionKey=&sign=ad1cfca383aa909cea7c0' \
        #    '763c3414462&signMethod=01&sysTag=S00102&timestamp=15577429794&version=1.0' % (123456, 18216482019))
        # print("login:%s" % r.json())
        # d = r.json()
        # openid = d['data']['openId']
        # sesskey = d['data']['sessKey']
        # account_sn = d['data']['accountSn']
        # print("sesskey = ",sesskey)
        # # r = self.client.post("/api/v1/erp/account/login", timeout=30, headers=header)
        # # print("login:%s" % r.json())

        # todo 这里可以使用assert断言请求是否正确，也可以使用if判断
        # assert r.status_code == 200

        # time.sleep(2)
        # # # todo 进入云平台 or 代理交易助手
        # r2 = self.client.post('/api/v1/user/login', timeout=30, headers=header,
        #                       data='accountSn=%s&openId=%s&sessionKey=%s&sign=64d6dc7d4d76bc203babf0faad51ae16&sysTag=S00102' % (
        #                           account_sn, openid, sesskey))
        # print("111111111111")
        # print('accountSn=%s&openId=%s&sessionKey=%s&sign=64d6dc7d4d76bc203babf0faad51ae16&sysTag=S00102' % (
        #                           account_sn, openid, sesskey))
        # print("login2:%s" % r2.json())
        # b = r2.json()
        # sessionKey = b['data']['sessionKey']
    #
    @task(1)
    # def test_login(self):
    #     # # # todo 接口
    #     r_bill_info = self.client.post('/api/v1/provider/quota/lending/apply/bill/info', timeout=30, headers=header,
    #                                     data='id=2&lendingPrice=1&sessionKey=%s&sign=0ba29a17c57695b9cf86917228df1830' % token_a)
    #     print("r_bill_info:%s" % r_bill_info.json())
    #     # r = self.client.post("/api/v1/provider/quota/lending/apply/page", timeout=30, headers=header)
    #     # 这里可以使用assert断言请求是否正确，也可以使用if判断
    #     # assert r.status_code == 200
    def test_login(self):
        # # # todo 接口

        r_bill_info = self.client.post('/api/v1/provider/quota/lending/apply/bill/info', timeout=30, headers=header,
                                        data='id=2&lendingPrice=1&sessionKey=%s&sign=0ba29a17c57695b9cf86917228df1830' % token_a)
        print("r_bill_info:%s" % r_bill_info.json())
        # r = self.client.post("/api/v1/provider/quota/lending/apply/page", timeout=30, headers=header)
        # 这里可以使用assert断言请求是否正确，也可以使用if判断
        # assert r.status_code == 200

# 这个类类似设置性能测试，继承HttpLocust
class websitUser(HttpLocust):
    # 指向一个上面定义的用户行为类
    task_set = test_926
    # 执行事物之间用户等待时间的下界，单位毫秒，相当于lr中的think time
    host = 'http://163.177.128.179:63095'  #todo 进入云企后的host
    # host = 'http://163.177.128.179:63201' #todo 登陆云企的host
    min_wait = 5000
    max_wait = 9000

if __name__ == '__main__':
    # host = 'http://120.79.223.2:2001'
    driver = webdriver.Chrome()
    driver.get('http://localhost:8089/')
    print("+++++++++++++")

    os.system('locust -f demo_locust.py --web-host="127.0.0.1"')
    os.system('locust -f demo_locust.py --host=http://163.177.128.179:63095 --web-host="127.0.0.1"')

    time.sleep(1)
    # driver.refresh()  # 刷新方法 refresh
    driver.get('http://localhost:8089/')
    print("shuaxinshuaxinshuaxinshuaxinshuaxin")

def run_os():
    os.system('locust -f demo_locust.py --host=http://163.177.128.179:63095 --web-host="127.0.0.1"')
    print("os子进程执行中>>> pid={0},ppid={1}".format(os.getpid(), os.getppid()))


def open_web():
    driver = webdriver.Chrome()
    driver.get('http://127.0.0.1:8089')
    print("driver子进程执行中>>> pid={0},ppid={1}".format(os.getpid(), os.getppid()))


if __name__ == '__main__':
    # host = 'http://120.79.223.2:2001'
    pro_list = []
    pro1 = Process(target=run_os, args=())
    pro_list.append(pro1)
    print('+++++++++++++++++++++++++')
    pro2 = Process(target=open_web, args=())
    pro_list.append(pro2)
    for i in pro_list:
        i.start()
        time.sleep(5)