import pytest
import time
import selenium
import sys
import csv
import getpass


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC


class Build_user:

    def user1_execute(self):
        username = "virtual_user1"
        self.user1_login(username)
        self.user1_step1()
        self.user1_step2()
        self.user1_step3_rollback()

    def user1_login(self, username):
        self.bigSpacer()
        time.sleep(1)
        print("Loading website")
        self.driver.get("http://127.0.0.1:5000")

        self.smallSpacer()
        print("Click sign up")
        self.driver.find_element(By.XPATH, r'/html/body/div/div[3]/button').click()

        self.smallSpacer()
        print("Enter a invalid name with a empty string")
        self.driver.find_element(By.XPATH, r'/html/body/div/div[1]/form[2]/button').click()
        print("You can see the alert dialog now")

        self.smallSpacer()
        print("Now enter a valid username again")
        self.driver.find_element(By.XPATH, r'/html/body/div/div[3]/button').click()
        username_field = self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[1]/form[2]/input')
        username_field.clear()
        username_field.send_keys(username)

        # Submit request
        self.smallSpacer()
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[1]/form[2]/button').click()
        print("Login with virtual_user1 successfully!!\n")

    def user1_step1(self):
        self.bigSpacer()
        print("Step1: select female")

        # self.smallSpacer()
        # print("select age 25")
        # slider = self.driver.find_element(By.XPATH, r'/html/body/div/form/div[1]/input')
        # self.action.click_and_hold(slider).perform()
        # self.action.drag_and_drop_by_offset(slider, xoffset=100, yoffset=0).perform()
        # self.action.drag_and_drop_by_offset(slider, xoffset=-0.01, yoffset=0).perform()
        # self.action.release().perform()

        self.smallSpacer()
        print("select female")
        self.driver.find_element(By.XPATH, r'/html/body/div/form/div[2]/input[2]').click()

        self.smallSpacer()
        print("click next step")
        self.driver.find_element(By.XPATH, r'/html/body/div/form/button').click()
        print("user1 select age and gender successfully!!\n")

    def user1_step2(self):
        time.sleep(6)
        self.bigSpacer()
        print("Step2: Testing buttons")

        # 两个style还没测，具体代码已经写好block了
        # self.smallSpacer()
        # print("Testing hair style")
        # self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[1]/ul/li[3]/label"))).click()
        # time.sleep(4)
        # self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[1]/ul/li[2]/label"))).click()
        # time.sleep(4)
        # self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[1]/ul/li[3]/label"))).click()
        # time.sleep(4)
        #
        # self.smallSpacer()
        # print("test cloth style")
        # self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[2]/ul/li[3]/label"))).click()
        # time.sleep(4)

        self.smallSpacer()
        print("Testing hair color buttons")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[3]/ul/li[3]/label"))).click()
        time.sleep(self.time_sleep)
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[3]/ul/li[4]/label').click()
        time.sleep(self.time_sleep)
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[3]/ul/li[2]/label').click()

        self.smallSpacer()
        print("Testing shirt buttons")
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[4]/ul/li[3]/label').click()
        time.sleep(self.time_sleep)
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[4]/ul/li[4]/label').click()
        time.sleep(self.time_sleep)
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[4]/ul/li[2]/label').click()

        self.smallSpacer()
        print("Testing Trousers buttons")
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[5]/ul/li[3]/label').click()
        time.sleep(self.time_sleep)
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[5]/ul/li[4]/label').click()
        time.sleep(self.time_sleep)
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[5]/ul/li[2]/label').click()

        self.smallSpacer()
        print("Testing Skin Colour buttons")
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[6]/ul/li[3]/label').click()
        time.sleep(self.time_sleep)
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[6]/ul/li[4]/label').click()
        time.sleep(self.time_sleep)
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/div[6]/ul/li[2]/label').click()

        self.smallSpacer()
        print("click next step")
        self.driver.find_element(By.XPATH, r'/html/body/div[2]/div[3]/form/button').click()
        print("user1 select style and clothing successfully!!\n")

    def user1_step3_rollback(self):
        self.bigSpacer()

    def user1_step4(self):
        self.bigSpacer()

    def smallSpacer(self):
        time.sleep(self.time_sleep)
        print("-----------------------------------------------")

    def bigSpacer(self):
        time.sleep(self.time_sleep)
        print(" ")
        print("===============================================")
        print("===============================================")
        print(" ")

    def scroll_down(self):
        lenOfPage = self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match = False
        while (match == False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            if lastCount == lenOfPage:
                match = True

    def close(self):
        self.bigSpacer()
        print("YOU PASS ALL THE TEST!")
        time.sleep(3)
        self.driver.close()

    def __init__(self):
        # # ---------------headless mode----------------#
        # options = webdriver.Chrome()
        # options.add_argument("--headless")
        # driver = webdriver.Chrome('./geckodriver.exe', chrome_options=options)
        # ----------------Normal mode-----------------#
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        # to supress the error messages/logs
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')
        self.action = ActionChains(self.driver, 50)
        self.time_sleep = 1
        self.wait = ui.WebDriverWait(self.driver, 20)

def get_track(distance):
    # 移动轨迹
    track = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 计算间隔
    t = 0.2
    # 初速度
    v = 1
    while current:
        if current:
            # 加速度为2
            a = 4
        else:
            # 加速度为-2
            a = -3
        v0 = v
        # 当前速度
        v = v0 + a * t
        # 移动距离
        move = v0 * t + 1 / 2 * a * t * t
        # 当前位移
        current += move
        # 加入轨迹
        track.append(round(move))
    return track
