import pytest

from controller import *
from flask import  url_for, request, current_app

import json

class Test_Controller():
    MODEL_OBJ = {
        "modelname":"alisa",
        "age":18,
        "gender":"Female"
    }

    def setup(self):
        """在执行具体方法前先被调用"""
        self.app = app
        self.context = app.app_context()
        self.context.push()
        # 利用flask提供的测试客户端进行测试
        self.client = app.test_client()

        # 激活测试标志
        app.config['TESTING'] = True

        current_app.config["DEBUG"]

    def test_index(self):
        with self.client:
            response = self.client.get(url_for('index'), follow_redirects=True)
            # check the status code
            # self.assertEqual(200, response.status_code)
            assert response.status_code == 200


    def test_register_page_post(self):
        with self.client:
            response = self.client.post(url_for('register_page'),data=Test_Controller.MODEL_OBJ)
            assert response.status_code == 302

    def test_register_page_get(self):
        with self.client:
            response = self.client.get(url_for('register_page'))
            # self.assertEqual(200, response.status_code)
            assert response.status_code == 200

    def test_login_page_get(self):
        with self.client:
            response = self.client.get(url_for('login_page'))
            # check the status code
            assert response.status_code == 200

    def test_login_page_post(self):
        with self.client:
            response = self.client.post(url_for('register_page'),data=Test_Controller.MODEL_OBJ)
            assert response.status_code == 302

    def test_logout(self):
        with self.client:
            response = self.client.get(url_for("logout"))
            login_status = session["logged_in"]
            assert login_status == False
            assert response.status_code == 302

    def test_complete_step_1_get(self):
        with self.client:
            response = self.client.get(url_for('complete_step1'))
            # check the status code
            assert response.status_code == 200

    def test_complete_step1_post(self):
        with self.client:
            response = self.client.post(url_for("complete_step1"), data=Test_Controller.MODEL_OBJ)
            assert response.status_code == 302

    def test_complete_step2_get(self):
        with self.client:
            response = self.client.get(url_for('complete_step2'))
            # check the status code
            assert response.status_code == 200

    def test_complete_step2_post(self):
        with self.client:
            response = self.client.post(url_for("complete_step2"), data=Test_Controller.MODEL_OBJ)
            assert response.status_code == 200

    def test_complete_step3_get(self):
        with self.client:
            response = self.client.get(url_for('complete_step3'))
            # check the status code
            assert response.status_code == 200

    def test_complete_step4_get(self):
        with self.client:
            response = self.client.post(url_for("complete_step3"))
            assert response.status_code == 200

if __name__ == '__main__':
    pytest.main(["-s", "test_controller.py"])



