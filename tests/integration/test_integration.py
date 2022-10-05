import pytest

from controller import *
from flask import  url_for, request, current_app


class TestIntegration:
    def setup(self):
        """在执行具体方法前先被调用"""
        self.app = app
        self.app.config['SECRET_KEY'] = '123'
        self.context = app.app_context()
        self.context.push()
        # 利用flask提供的测试客户端进行测试
        self.client = app.test_client()

        # 激活测试标志
        app.config['TESTING'] = True

        current_app.config["DEBUG"]

    def test_login_with_no_existing_account(self):
        # First try to login with an account but no such account ever existed
        pass
