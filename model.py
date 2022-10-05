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
                                       thigh, shank, hip, arm_girth, arm_pan, waist, chest
                                       ):
        if model_name is None or height is None or weight is None:
            return
        if thigh is None or shank is None or hip is None:
            return
        if arm_girth is None or arm_pan is None or waist is None or chest is None:
            return

        update_time = str(datetime.datetime.now()).split('.')[0]  # 参数入库的时间戳
        result = self.database.add_new_body_measurement_record_with_time(model_name, update_time, height, weight, thigh,
                                                                         shank, hip, arm_girth, arm_pan, waist, chest)
        return result

    def add_model_appearance(self, model_name, hair_color, skin_color, top_dress, bottom_dress, basic_model_name):

        result = self.database.add_model_appearance(model_name, hair_color, skin_color, top_dress, bottom_dress,
                                                    basic_model_name)
        return result

    def define_basic_model(self, age, gender):
        if age is None or gender is None:
            return
        if age == 'None' or gender == 'None':
            return
        age = int(age)
        result = ""
        if age < 20:
            result += "teenager_"
        elif age < 40:
            result += "adult_"
        elif age < 55:
            result += "middle_"
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

    def search_last_one_body_measurement_records(self, model_name):
        model_parameters = self.database.search_last_one_body_measurement_record(model_name)
        if len(model_parameters) == 0:
            return None
        return model_parameters[0]

    def search_body_parameters_range(self, model_name):
        age_and_gender = self.database.search_model_age_and_gender(model_name)
        if len(age_and_gender)==0:
            return None
        age_group = self.define_basic_model(age_and_gender[0][0],age_and_gender[0][1])
        body_parameters_range = self.database.search_body_parameters_range(age_group)
        if len(body_parameters_range) ==0:
            return None
        return body_parameters_range[0]

    def define_new_model_body_parameters(self,model_name):
        general_body_parameters = [0]
        body_parameters_range = self.search_body_parameters_range(model_name)
        i =1
        while (i< 18):
            general_body_parameters.append((body_parameters_range[i]+body_parameters_range[i+1])/2)
            i+=2
        return general_body_parameters



    # def search_body_parameters_range(self,age_group):
    #     result = self.database.search_body_parameters_range(age_group)
    #     print(result)

    # def split_mesh_name(self, texture_name):
    #     tmp = texture_name.strip().split(',')
    #     i = 1
    #     result = []
    #     while i < len(tmp):
    #         result.append(tmp[i])
    #         i += 2
    #     return ','.join(result)


# model = Model()
# print(model.define_new_model_body_parameters('admin'))
# model.search_model_age_and_gender('admin')
# model.search_body_parameters_range('middle_male')
# print(model.search_body_parameters_range('admin'))

# print(str(datetime.datetime.now()).split('.')[0])
# print(model.database.search_last_two_body_measurement_records('admin'))
# print(model.database.search_last_one_body_measurement_record('admin')[0])

# print(model.database.search_basic_model_file_path('admin'))
# print(model.search_model_texture_file_path('admin'))
