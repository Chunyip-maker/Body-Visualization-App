import pytest

from model import *
from unittest.mock import MagicMock
from unittest.mock import patch

@pytest.mark.unit_test
class Test_Model:
    def setup(self):
        self.model = Model()
        self.mock_database =  self.create_mock_database()
        self.model.set_database(self.mock_database)

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

    def test_check_user_input(self):
        result = self.model.check_user_input("")
        assert result == False

        result = self.model.check_user_input("*"*60)
        assert result == False

        result = self.model.check_user_input("##")
        assert result == False

        result = self.model.check_user_input("12344")
        assert result == True

    def test_define_basic_model(self):
        result = self.model.define_basic_model(18,"female")
        assert result == "teenager_female"

        result = self.model.define_basic_model(35,"male")
        assert  result == "adult_male"

        result = self.model.define_basic_model(50, "male")
        assert result == "middle_male"

        result = self.model.define_basic_model(70,"male")
        assert result == "old_male"

        result = self.model.define_basic_model(None, None)
        assert result is None

        result = self.model.define_basic_model('None', 'None')
        assert result is None

    def test_zip_combined_records_none_argument(self):
        result = self.model.zip_combined_records([],[],None,None,[])
        assert result is None

        result = self.model.zip_combined_records([], [], [],[], None)
        assert result is None

    def test_add_new_body_measurment_record(self):
        result = self.model.add_new_body_measurment_record("Isabelle",1,2,3,4,5,6,7,8,9)
        assert result == True

        result = self.model.add_new_body_measurment_record("Isabelle", 1, None, 3, 4, 5, 6, 7, 8, 9 )
        assert result is None

        result = self.model.add_new_body_measurment_record("Isabelle", 1, 2, 3, None, 5, 6, 7, 8, 9)
        assert result is None

        result = self.model.add_new_body_measurment_record("Isabelle", 1, 2, 3, 4,5, 6, 7, 8, None)
        assert result is None

    def test_search_last_one_body_measurement_records(self):
        result = self.model.search_last_one_body_measurement_records("Isabelle")
        assert result == ("2022-10-10 23:13:13",163,45,67,60,78,28,24,50,33)

        self.mock_database.search_last_one_body_measurement_record= MagicMock(return_value=[])
        result = self.model.search_last_one_body_measurement_records("Isabelle")
        assert result is not None

    def test_search_body_parameters_range(self):

        self.mock_database.search_model_age_and_gender=MagicMock(return_value=[])
        result = self.model.search_body_parameters_range("Isabelle")
        assert result is None

    def test_generate_bmi_report(self):
        result = self.model.generate_bmi_report(10)
        assert result[0] == 10
        assert result[1] == 'underweight'

        result = self.model.generate_bmi_report(24)
        assert result[0] == 24
        assert result[1] == 'normal'

        result = self.model.generate_bmi_report(28)
        assert result[0] == 28
        assert result[1] == 'overweight'

        result = self.model.generate_bmi_report(35)
        assert result[0] == 35
        assert result[1] == 'obese'

    def test_generate_bfr_report(self):
        result = self.model.generate_bfr_report(24,None)
        assert result is None

        result = self.model.generate_bfr_report(4, "male")
        assert result[1] == "abnormal"

        result = self.model.generate_bfr_report(21, "male")
        assert result[1] == "healthy"

        result = self.model.generate_bfr_report(24, "male")
        assert result[1] == "healthy"

        result = self.model.generate_bfr_report(9, "female")
        assert result[1] == "abnormal"

        result = self.model.generate_bfr_report(10, "female")
        assert result[1] == "healthy"

        result = self.model.generate_bfr_report(32, "female")
        assert result[1] == "obese"

    def test_generate_parameter_change_report(self):
        result = self.model.generate_parameter_change_report("Isabelle", None)
        assert result is None

        latest_records = [
            {"update_time":"2022-10-11 21:31:39",
            "height":175,
             "weight":55,
             "thigh":56,
             "shank":33,
             "hip":74,
             "arm_girth":33,
             "arm_pan":32,
             "waist":65,
             "chest":55},
            {"update_time":"2022-10-13 08:21:39",
                "height": 175,
             "weight": 55,
             "thigh": 56,
             "shank": 33,
             "hip": 74,
             "arm_girth": 33,
             "arm_pan": 32,
             "waist": 65,
             "chest": 55}
        ]
        result = self.model.generate_parameter_change_report("Isabelle", latest_records)
        assert result is not None



    def test_get_historic_body_measurement_records_to_be_displayed(self):
        self.mock_database.get_all_body_measurement_records = MagicMock(
            return_value=[("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9),
                          ("isabelle", "2021-09-09 00:05:09", 1, 2, 3, 4, 5, 6, 7, 8, 9)])
        result = self.model.get_historic_body_measurement_records_to_be_displayed("Isabelle")
        assert result is not None
