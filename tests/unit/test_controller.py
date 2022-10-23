import pytest

from controller import *
from flask import  url_for, current_app
from unittest.mock import MagicMock
from unittest.mock import patch
from controller import model

@pytest.mark.unit_test
class Test_Controller():
    MODEL_OBJ = {
        "modelname":"alisa",
        "age":18,
        "gender":"Female",
        "height":"175",
        "weight":50,
        "thigh":55,
        "shank":34,
        "hip":64,
        "upper_arm":30,
        "waist":62,
        "chest":72
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
        mock_database.search_last_one_body_measurement_record= MagicMock(return_value=[("2022-10-10 23:13:13",163,45,67,60,78,28,24,50,33)])
        mock_database.search_body_parameters_range = MagicMock(return_value=[("tennager male",130,180,30,90,75,95,60,80,75,95,20,35,35,50,40,58,22,40)])
        mock_database.get_two_newest_body_measurement= MagicMock(return_value=[("Isabelle","2021-09-09 00:05:09",1,2,3,4,5,6,7,8,9)])
        mock_database.get_all_body_measurement_records = MagicMock(return_value = [("isabelle","2021-09-09 00:05:09",1,2,3,4,5,6,7,8,9)])
        mock_database.get_last_twenty_body_measurement_records = MagicMock(return_value = [("isabelle","2021-09-09 00:05:09",1,2,3,4,5,6,7,8,9)])

        return mock_database

    def setup(self):
        """Called before any test case"""
        self.app = app
        self.mock_database = self.create_mock_database()

        model.set_database(self.mock_database)

        self.app.config['SECRET_KEY']='123'
        self.context = app.app_context()
        self.context.push()
        self.client = app.test_client()

        app.config['TESTING'] = True

        current_app.config["DEBUG"]



    def test_index(self):
        with self.client:
            response = self.client.get(url_for('index'), follow_redirects=True)
            # check the status code
            # self.assertEqual(200, response.status_code)
            assert response.status_code == 200

    def test_index(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        response = self.client.get(url_for('index'))
        assert response.status_code == 302

    def test_index_previous_not_logged_in(self):
        with self.client.session_transaction() as session:
            session['logged_in']=False

        response = self.client.get(url_for('index'))
        assert response.status_code == 302

    def test_register_page_post(self):
        with self.client:
            response = self.client.post(url_for('register_page'),data=Test_Controller.MODEL_OBJ)
            assert response.status_code == 302


    def test_register_page_get(self):
        with self.client:
            response = self.client.get(url_for('register_page'))
            # self.assertEqual(200, response.status_code)
            assert response.status_code == 200

    def test_register_page_get_logged_in(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True

        response = self.client.get(url_for('register_page'))
        # self.assertEqual(200, response.status_code)
        assert response.status_code == 302

    def test_login_page_get(self):
        with self.client:
            response = self.client.get(url_for('login_page'))
            # check the status code
            assert response.status_code == 200

    def test_login_page_logged_in(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True

        response = self.client.get(url_for('login_page'))
        assert response.status_code == 302


    def test_login_page_post(self):
        with self.client:
            response = self.client.post(url_for('register_page'),data=Test_Controller.MODEL_OBJ)
            assert response.status_code == 302

    def test_logout(self):
        with self.client:
            response = self.client.get(url_for("logout"))
            assert response.status_code == 302

    def test_logout_previous_logged_in(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        response = self.client.get(url_for("logout"))
        assert response.status_code == 302

    def test_complete_step1_logged_in(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        response = self.client.get(url_for('complete_step1'))
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

    def test_complete_step2_get_logged_in(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        response = self.client.get(url_for('complete_step2'))
        assert response.status_code == 302


    def test_complete_step2_get(self):
        with self.client:
            response = self.client.get(url_for('complete_step2'))
            # check the status code
            assert response.status_code == 200

    def test_complete_step2_post(self):
        with self.client:
            response = self.client.post(url_for("complete_step2"), data=Test_Controller.MODEL_OBJ)
            assert response.status_code == 302


    def test_complete_step3_get(self):
        with self.client:
            response = self.client.get(url_for('complete_step3'))
            # check the status code
            assert response.status_code == 302

    def test_complete_step3_get_logged_in(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        response = self.client.get(url_for('complete_step3'))
        assert response.status_code == 200


    def test_complete_step3_post_logged_in(self):
        # with self.client:
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        response = self.client.post(url_for('complete_step3'),data=Test_Controller.MODEL_OBJ)
        assert response.status_code == 302

    def test_complete_step4_get(self):
        response = self.client.get(url_for('complete_step4'))
        assert response.status_code == 302

    def test_complete_step4_get_logged_in(self):
        with self.client.session_transaction() as session:
            session['logged_in'] = True
        response = self.client.get(url_for('complete_step4'))
        assert response.status_code == 200

    def test_complete_step4_get_logged_in_cookie_set(self):
        self.client.set_cookie('localhost',"model_name", "test_1_name")
        self.client.set_cookie('localhost',"gender", "male")
        self.client.set_cookie('localhost', "age", "15")
        with self.client.session_transaction() as session:
            session['logged_in'] = True

        response = self.client.get(url_for('complete_step4'))

        assert response.status_code == 200


if __name__ == '__main__':
    pytest.main(["-s", "test_controller.py"])



