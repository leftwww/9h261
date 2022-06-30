from selenium import webdriver
import time

class UTT_update():
    start_url = 'http://10.10.1.254/noAuth/login.html'
    driver = webdriver.Chrome()
    driver.implicitly_wait(1.5)

    def login(self):
        # 登陆
        driver = self.driver
        start_url = self.start_url
        driver.get(start_url)

        driver.find_element_by_xpath('//*[@id="wrap"]/form/div[1]/input').send_keys('admin')
        driver.find_element_by_xpath('/html/body/div[1]/form/div[2]/input').send_keys('sZ5P4pAZ')
        driver.find_element_by_xpath('//*[@id="login_btn"]').click()

    def update_(self):
        # 点击更新
        time.sleep(1)
        driver = self.driver
        driver.find_element_by_xpath('/html/body/div/div[2]/div[1]/ul/li[3]/div/h4/span').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="sidebar"]/ul/li[3]/div/ul/li[1]/a').click()
        time.sleep(1)
        #  button[1] = 更新； button[3] =刷新
        driver.find_element_by_xpath('//*[@id="otherBtns"]/button[1]').click()
        time.sleep(1)
        driver.quit()


if __name__ == '__main__':
    utt = UTT_update()
    utt.login()
    utt.update_()
