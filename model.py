import os
import datetime
from sql import SQLDatabase


class Model:
    def __init__(self):
        self.database = SQLDatabase()

        # Create the tables in the database
        self.database.database_setup()

    def check_model_already_exists(self, model_name):
        result = self.database.check_model_existence(model_name)
        return result

    def add_a_basic_human_model(self, model_name, age, gender):
        self.database.add_model(model_name, age, gender)

    def check_user_input(self, string):
        if len(string) == 0:
            return False
        if len(string) > 50:
            return False
        for i in [";", "#", "&", "'", "<", ">", "-", " "]:
            ## find special characters
            if i in string:
                return False
        return True

    def add_new_body_measurment_record(self, model_name, height, weight,
                                       thigh, shank, hip, upper_arm, waist, chest
                                       ):
        if model_name is None or height is None or weight is None:
            return
        if thigh is None or shank is None or hip is None:
            return
        if upper_arm is None or waist is None or chest is None:
            return

        update_time = str(datetime.datetime.now()).split('.')[0]  # 参数入库的时间戳
        result = self.database.add_new_body_measurement_record_with_time(model_name, update_time, height, weight, thigh,
                                                                         shank, hip, upper_arm, waist, chest)
        return result

    def add_model_appearance(self, model_name, hair_color, skin_color, top_dress, bottom_dress, basic_model_name):

        result = self.database.add_model_appearance(model_name, hair_color, skin_color, top_dress, bottom_dress,
                                                    basic_model_name)
        return result

    def define_basic_model(self, age, gender):
        if age is None or gender is None:
            return
        age = int(age)
        result = ""
        if age < 20:
            result += "teenager_"
        elif age < 40:
            result += "adult_"
        elif age < 55:
            result += "middle_age_"
        else:
            result += "old_"

        if gender == "male":
            result += "male"
        else:
            result += "female"

        return result

    def search_basic_model_file_path(self, model_name):
        return self.database.search_basic_model_file_path(model_name)

    def search_model_texture_file_path(self, model_name):
        return self.database.search_model_texture_file_path(model_name)

    def search_last_two_body_measurement_records(self, model_name):
        return self.database.search_last_two_body_measurement_records(model_name)

    # def split_mesh_name(self, texture_name):
    #     tmp = texture_name.strip().split(',')
    #     i = 1
    #     result = []
    #     while i < len(tmp):
    #         result.append(tmp[i])
    #         i += 2
    #     return ','.join(result)

model = Model()
# print(str(datetime.datetime.now()).split('.')[0])
# print(model.database.search_last_two_body_measurement_records('admin'))
# print(model.database.search_basic_model_file_path('admin'))
print(model.search_model_texture_file_path('admin'))
