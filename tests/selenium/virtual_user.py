import pytest
import time
import selenium
import sys
import csv
import getpass
import random

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC


class Build_user:

    def user1_execute(self):
        username = "virtualUser" + str(random.uniform(200, 10000))
        self.user1_login(username)
        self.user1_step1()
        self.user1_step2()
        self.user1_step3_rollback()
        self.user1_step3_testing()
        self.user1_step4_viewAndLogOut(username)

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

        self.smallSpacer()
        print("select age 25")
        slider = self.driver.find_element(By.XPATH, r'/html/body/div/form/div[1]/input')
        self.action.click_and_hold(slider).perform()
        self.action.drag_and_drop_by_offset(slider, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("select female")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/form/div[2]/label[2]"))).click()

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
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/form/div[3]/ul/li[3]/label"))).click()
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
        time.sleep(8)
        self.bigSpacer()
        print("Step3 rollback: Directly go to step4 to see report and come back")

        self.smallSpacer()
        print("save model parameter and go to the step4")
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[10]/button"))).click()

        self.smallSpacer()
        print("scroll down")
        self.scroll_down()

        time.sleep(3)
        self.smallSpacer()
        print("scroll up")
        self.scroll_up()

        self.smallSpacer()
        print("Go back to step3")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/form[1]/button"))).click()

    def user1_step3_testing(self):
        time.sleep(8)
        self.bigSpacer()
        print("Step3: Change parameter")

        self.smallSpacer()
        print("Go and see historical record")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[2]/button"))).click()

        self.smallSpacer()
        print("Go back to step3")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/form[1]/button"))).click()

        self.smallSpacer()
        print("Change Shank")
        slider1 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[9]/div/input")))
        self.action.click_and_hold(slider1).perform()
        self.action.drag_and_drop_by_offset(slider1, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("Change Thigh")
        slider2 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[8]/div/input")))
        self.action.click_and_hold(slider2).perform()
        self.action.drag_and_drop_by_offset(slider2, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("Change Arms pan")
        slider3 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[7]/div/input")))
        self.action.click_and_hold(slider3).perform()
        self.action.drag_and_drop_by_offset(slider3, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("Change Arm girth")
        slider4 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[6]/div/input")))
        self.action.click_and_hold(slider4).perform()
        self.action.drag_and_drop_by_offset(slider4, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("Change Hip")
        slider5 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[5]/div/input")))
        self.action.click_and_hold(slider5).perform()
        self.action.drag_and_drop_by_offset(slider5, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("Change Waist")
        slider6 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[4]/div/input")))
        self.action.click_and_hold(slider6).perform()
        self.action.drag_and_drop_by_offset(slider6, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("Change Chest")
        slider7 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[3]/div/input")))
        self.action.click_and_hold(slider7).perform()
        self.action.drag_and_drop_by_offset(slider7, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("Change Weight")
        slider8 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[2]/div/input")))
        self.action.click_and_hold(slider8).perform()
        self.action.drag_and_drop_by_offset(slider8, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

        self.smallSpacer()
        print("Change Height")
        slider9 = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[1]/div/input")))
        self.action.click_and_hold(slider9).perform()
        self.action.drag_and_drop_by_offset(slider9, xoffset=100, yoffset=0).perform()
        self.action.release().perform()

    def user1_step4_viewAndLogOut(self, username):
        time.sleep(2)
        self.bigSpacer()
        print("Step4: See comparing of data")

        self.smallSpacer()
        print("Save and see new data")
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/form[1]/div[10]/button"))).click()

        self.smallSpacer()
        print("Check camera top button")
        time.sleep(3)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div[1]/button[1]"))).click()

        self.smallSpacer()
        print("Check camera bottom button")
        time.sleep(4)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div[1]/button[2]"))).click()

        self.smallSpacer()
        print("Check camera top side button")
        time.sleep(4)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div[1]/button[3]"))).click()

        self.smallSpacer()
        print("Check camera bottom side button")
        time.sleep(4)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div[1]/button[4]"))).click()

        self.smallSpacer()
        print("Check camera Back button")
        time.sleep(4)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[3]/div[1]/button[5]"))).click()

        self.smallSpacer()
        time.sleep(4)
        print("scroll down")
        self.scroll_down()

        time.sleep(3)
        self.smallSpacer()
        print("scroll up")
        self.scroll_up()

        self.smallSpacer()
        print("Log out")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/form[2]/button"))).click()

        self.smallSpacer()
        print("Enter user name")
        time.sleep(4)
        username_field = self.driver.find_element(By.XPATH, r'/html/body/div/div[1]/form[1]/input')
        username_field.send_keys(username)

        # Submit request
        self.smallSpacer()
        print("Log in")
        time.sleep(4)
        self.driver.find_element(By.XPATH, r'/html/body/div/div[1]/form[1]/button').click()
        print("Login with virtual_user1 successfully!!\n")

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
                "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return "
                "lenOfPage;")
            if lastCount == lenOfPage:
                match = True

    def scroll_up(self):
        self.driver.execute_script(
            "window.scrollTo(0, 0)")
        time.sleep(2)

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

        # change the path of driver to yours
        # windows
        self.driver = webdriver.Chrome(options=options, executable_path='./chromedriver.exe')

        # # Macos chrome 106
        # self.driver = webdriver.Chrome(options=options, executable_path='./chromedriver106')

        # Macos chrom 107
        # self.driver = webdriver.Chrome(options=options, executable_path='./chromedriver107')

        self.action = ActionChains(self.driver, 50)
        self.time_sleep = 0
        self.wait = ui.WebDriverWait(self.driver, 20)
