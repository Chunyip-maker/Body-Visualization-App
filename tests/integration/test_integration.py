import pytest

from controller import *
from flask import  url_for, request, current_app
from unittest.mock import MagicMock
from unittest.mock import patch
from controller import model

@pytest.mark.integration_test
class TestIntegration:
    def setup(self):
        """在执行具体方法前先被调用"""
        self.app = app

        self.mock_database = self.create_mock_database()

        model.set_database(self.mock_database)

        self.app.config['SECRET_KEY'] = '123'
        self.context = app.app_context()
        self.context.push()
        # 利用flask提供的测试客户端进行测试
        self.client = app.test_client()

        # 激活测试标志
        app.config['TESTING'] = True

        current_app.config["DEBUG"]
        self.MODEL_OBJ = {
        "modelname":"alisa",
        "age":18,
        "gender":"Female",
        "height":"175",
        "weight":50,
        "thigh":55,
        "shank":34,
        "hip":64,
        "Arm girth":30,
            "Arms pan" : 40,
        "waist":62,
        "chest":72,
            'hair_colour':1,
            'skin_colour':2,
            'top':3,
            'bot':4,
            "clothing_style":5
        }

    def create_mock_database(self):
        # mock __init__ mehthod
        def newinit(self):
            pass
        with patch.object(SQLDatabase, '__init__', newinit):
            mock_database = SQLDatabase()

        # mock other methods
        mock_database.execute = MagicMock(return_value = None)
        mock_database.commit = MagicMock(return_value = None)
        mock_database.database_setup = MagicMock(return_value=100)
        mock_database.check_table_is_empty = MagicMock(return_value = True)
        mock_database.check_model_existence = MagicMock(return_value = False)
        mock_database.add_model = MagicMock(return_value = True)
        mock_database.add_new_body_measurement_record_with_time = MagicMock(return_value = True)
        mock_database.add_model_appearance = MagicMock(return_value = True)
        mock_database.add_age_group_parameters_range = MagicMock(return_value = True)
        mock_database.search_model_age_and_gender = MagicMock(return_value = [(18,"female")])
        mock_database.search_model_texture_file_path = MagicMock(return_value = ("some_path",))
        mock_database.search_last_one_body_measurement_record= MagicMock(return_value=[("2021-09-10 00:05:09",9,8,7,6,5,4,3,2,1)])
        mock_database.search_body_parameters_range = MagicMock(return_value=[("tennager female",130,180,30,90,75,95,60,80,75,95,20,35,35,50,40,58,22,40)])
        mock_database.get_two_newest_body_measurement= MagicMock(return_value=[("Isabelle","2021-09-09 00:05:09",1,2,3,4,5,6,7,8,9),
                                                                                   ("Isabelle","2021-09-10 00:05:09",9,8,7,6,5,4,3,2,1)])
        mock_database.get_all_body_measurement_records = MagicMock(return_value = [("Isabelle","2021-09-09 00:05:09",1,2,3,4,5,6,7,8,9),
                                                                                   ("Isabelle","2021-09-10 00:05:09",9,8,7,6,5,4,3,2,1)])
        mock_database.get_last_twenty_body_measurement_records = MagicMock(return_value = [("Isabelle","2021-09-09 00:05:09",1,2,3,4,5,6,7,8,9),
                                                                                   ("Isabelle","2021-09-10 00:05:09",9,8,7,6,5,4,3,2,1)])

        return mock_database

    def test_register_index(self):
        with self.client:
            response = self.client.get(url_for('register_page'), follow_redirects=True)
            assert response.status_code == 200
            # no redirect, stay in register page, but render the template of index.html
            assert response.request.path ==url_for('register_page')

    def test_login_index(self):
        with self.client:
            response = self.client.get(url_for('login_page'), follow_redirects=True)
            assert response.status_code == 200
            # no redirect, stay in register page, but render the template of index.html
            assert response.request.path ==url_for('login_page')

    # integration of the register module, age & gender
    def test_register_step1(self):
        with self.client:
            response = self.client.get(url_for('register_page'))
            # 未登录用户，首先跳转至/login
            assert response.status_code == 200

            # 提交后进入Step1
            response = self.client.post(url_for('register_page'), data=self.MODEL_OBJ, follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step1')

            # 验证此时尚未入库,前面注册不成功
            response = self.client.get(url_for('index'), follow_redirects = True)
            assert response.status_code == 200
            assert response.request.path == url_for('login_page')

    # integration of the register module, age & gender module, and appearance customizatio module
    def test_register_step1_step2(self):
        with self.client:
            response = self.client.get(url_for('register_page'))
            # 未登录用户，首先跳转至/login
            assert response.status_code == 200

            # 提交后进入Step1
            response = self.client.post(url_for('register_page'), data=self.MODEL_OBJ, follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step1')

            # 在step1提交年龄性别数据,进入step2
            response = self.client.post(url_for('complete_step1'), data=self.MODEL_OBJ, follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step2')

            # 验证此时尚未入库,前面注册不成功
            response = self.client.get(url_for('index'), follow_redirects = True)
            assert response.status_code == 200
            assert response.request.path == url_for('login_page')

    # intgration of the register module, age & gender set-up module, and appearance customization module
    def test_register_step1_step2_step3_(self):

        with self.client:
            response = self.client.get(url_for('register_page'))
            # 未登录用户，首先跳转至/login
            assert response.status_code == 200

            # 提交后进入Step1
            response = self.client.post(url_for('register_page'), data=self.MODEL_OBJ,follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step1')

            # 在step1提交年龄性别数据
            response = self.client.post(url_for('complete_step1'),data=self.MODEL_OBJ,follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step2')

            # 在step2提交外形数据
            response = self.client.post(url_for('complete_step2'), data=self.MODEL_OBJ,follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step3')

            # 在step3选定身体参数并入库
            try:
                response = self.client.post(url_for('complete_step3'), data=self.MODEL_OBJ,follow_redirects=True)
            except IndexError:
                assert response.status_code == 200


            # 确认入库
            response = self.client.get(url_for('register_page'), follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step3')

    def test_register_step1_step2_step3_step4(self):
        with self.client:
            response = self.client.get(url_for('register_page'))
            # 未登录用户，首先跳转至/login
            assert response.status_code == 200

            # 提交后进入Step1
            response = self.client.post(url_for('register_page'), data=self.MODEL_OBJ,follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step1')

            # 在step1提交年龄性别数据
            response = self.client.post(url_for('complete_step1'),data=self.MODEL_OBJ,follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step2')

            # 在step2提交外形数据
            response = self.client.post(url_for('complete_step2'), data=self.MODEL_OBJ,follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step3')

            # 在step3选定身体参数并入库,进入step4
            try:
                response = self.client.post(url_for('complete_step3'), data=self.MODEL_OBJ,follow_redirects=True)
            except IndexError:
                assert response.status_code == 200

            # 确认入库
            response = self.client.get(url_for('register_page'), follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step3')

    # integration of the login module( which jumps to step3), step3, and report generation
    def test_login_step3(self):
        self.mock_database.check_model_existence = MagicMock(return_value=True)

        with self.client:
            # 从主页登陆
            response = self.client.get(url_for('index'),follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('login_page')

            # 登陆成功，直接跳去step3
            response = self.client.post(url_for('login_page'), data=self.MODEL_OBJ,follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step3')

    def test_login_step3_step4(self):
        self.mock_database.check_model_existence = MagicMock(return_value=True)

        with self.client:
            # 从主页登陆
            response = self.client.get(url_for('index'), follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('login_page')

            # 登陆成功，直接跳去step3
            response = self.client.post(url_for('login_page'), data=self.MODEL_OBJ, follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step3')

            # 选择参数，进入step4/historic report
            try:
                response = self.client.post(url_for('complete_step3'), data=self.MODEL_OBJ, follow_redirects=True)
            except IndexError:
                assert response.status_code == 200

    def test_index_step3(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        with self.client:
            response = self.client.get(url_for('index'), follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step3')


    def test_index_step3_step4(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        with self.client:
            response = self.client.get(url_for('index'), follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == url_for('complete_step3')

            # 选择参数，进入step4 / historic report
            try:
                response = self.client.post(url_for('complete_step3'), data=self.MODEL_OBJ, follow_redirects=True)
            except IndexError:
                assert response.status_code == 200

