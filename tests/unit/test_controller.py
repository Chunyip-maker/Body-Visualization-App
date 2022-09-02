import pytest

from controller import *
from flask import  url_for, request, current_app

import json

class Test_Controller():
    MODEL_OBJ = {
        "modelname":"alisa"
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
            response = self.client.post(url_for('register_page'),data=MyTestCase.MODEL_OBJ)
            # status_code = 302: redirected to another page
            # self.assertEqual(302, response.status_code)
            assert response.status_code == 302

    def test_register_page_post(self):
        with self.client:
            response = self.client.get(url_for('register_page'))
            # self.assertEqual(200, response.status_code)
            assert response.status_code == 200




if __name__ == '__main__':
    pytest.main(["-s", "test_controller.py"])



