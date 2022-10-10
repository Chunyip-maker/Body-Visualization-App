import os
import datetime
from sql import SQLDatabase
import numpy as np
import time

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

    def add_model_appearance(self, model_name, hair_color, skin_color, top_dress, bottom_dress, basic_model_path):

        result = self.database.add_model_appearance(model_name, hair_color, skin_color, top_dress, bottom_dress,
                                                    basic_model_path)
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

    def search_model_texture_file_path(self, model_name):
        return self.database.search_model_texture_file_path(model_name)

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

    # 返回 a list of records,最多两个record，最新的和次新的，每个record以字典形式存储body measurement
    def get_at_most_two_newest_body_measurement_record(self, model_name):
        if model_name is None:
            return
        raw_results = self.database.get_two_newest_body_measurement(model_name)
        result = []
        for i in range(len(raw_results)):
            raw_result = raw_results[i] # raw_result is a tuple from the 2d tuple returned by SQL query
            entry = {}

            # convert time
            entry["update_time"] = self.convert_time_to_remain_date(raw_result[1])
            entry["height"] = float(raw_result[2])
            entry["weight"] = float(raw_result[3])
            entry["thigh"] = float(raw_result[4])
            entry["shank"] = float(raw_result[5])
            entry["hip"] = float(raw_result[6])
            entry["arm_girth"]= float(raw_result[7])
            entry["arm_pan"] = float(raw_result[8])
            entry["waist"] = float(raw_result[9])
            entry["chest"] = float(raw_result[10])

            result.insert(0, entry)

        # print(result)
        return result

    # 如果历史数据少于等于十个，都返回
    # 如果历史数据个数多于十个，均匀取数共计十个
    # 返回a list of record,每个record以字典形式存储body_measurement,第一个为最新的数据，最后一个为最老的数据
    def get_historic_body_measurement_records_to_be_displayed(self, model_name):
        if model_name is None:
            return
        raw_results = self.database.get_all_body_measurement_records(model_name)
        result = []
        if len(raw_results) <= 10:
            for i in range(len(raw_results)):
                raw_result = raw_results[i]
                entry = {}
                # entry["update_time"] = self.convert_time_to_remain_date(raw_result[1])
                entry["update_time"] = raw_result[1]
                entry["height"] = float(raw_result[2])
                entry["weight"] = float(raw_result[3])
                entry["thigh"] = float(raw_result[4])
                entry["shank"] = float(raw_result[5])
                entry["hip"] = float(raw_result[6])
                entry["arm_girth"] = float(raw_result[7])
                entry["arm_pan"] = float(raw_result[8])
                entry["waist"] = float(raw_result[9])
                entry["chest"] = float(raw_result[10])
                result.insert(0, entry)
        else:
            # select records evenly spaced out by timestamp
            selected_indices = np.round(np.linspace(0, len(raw_results) - 1, 10)).astype(int)
            for idx in selected_indices:
                raw_result = raw_results[idx]
                entry = {}
                # entry["update_time"] = self.convert_time_to_remain_date(raw_result[1])
                entry["update_time"] = raw_result[1]
                entry["height"] = float(raw_result[2])
                entry["weight"] = float(raw_result[3])
                entry["thigh"] = float(raw_result[4])
                entry["shank"] = float(raw_result[5])
                entry["hip"] = float(raw_result[6])
                entry["arm_girth"] = float(raw_result[7])
                entry["arm_pan"] = float(raw_result[8])
                entry["waist"] = float(raw_result[9])
                entry["chest"] = float(raw_result[10])
                result.insert(0, entry)
        # for each in result:
        #     print(each)
        #     print()
        return result

    def get_last_twenty_body_measurement_records_to_be_displayed(self,model_name):
        if model_name is None:
            return
        result = []
        raw_results = self.database.get_last_twenty_body_measurement_records(model_name)
        for i in range(len(raw_results)):
            raw_result = raw_results[i] # raw_result is a tuple from the 2d tuple returned by SQL query
            entry = {}

            # convert time
            entry["update_time"] = raw_result[1]
            entry["height"] = float(raw_result[2])
            entry["weight"] = float(raw_result[3])
            entry["thigh"] = float(raw_result[4])
            entry["shank"] = float(raw_result[5])
            entry["hip"] = float(raw_result[6])
            entry["arm_girth"]= float(raw_result[7])
            entry["arm_pan"] = float(raw_result[8])
            entry["waist"] = float(raw_result[9])
            entry["chest"] = float(raw_result[10])

            result.append(entry)

        return result

    def convert_time_to_remain_date(self, datetime_from_sql):
        f = "%Y-%m-%d %H:%M:%S"
        result = str(datetime.datetime.strptime(datetime_from_sql, f).date())
        return result

    def calculate_bmi(self, historic_records):
        result = []
        for record in historic_records:
            weight = record["weight"]
            height = record["height"]/100
            bmi = round(weight/(height*height),2)
            result.append(bmi)

        return result

    def calculate_bmr(self, historic_records, model_gender, model_age):
        # Men: BMR = 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) – (5.677 x age in years)
        # Women: BMR = 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) – (4.330 x age in years)
        result = []
        model_age = int(model_age)
        for record in historic_records:
            weight = float(record["weight"])
            height = float(record["height"])
            if model_gender == "male":
                bmr = 88.362+(13.397*weight)+(4.799*height)-(5.677*model_age)
                result.append(int(bmr))
            elif model_gender == "female":
                bmr = 447.593+(9.247*weight)+(3.098*height)-(4.330*model_age)
                result.append(int(bmr))
            else:
                pass
        return result

    def calculate_body_fat_rate(self, historic_records, model_gender):
        result = []
        for record in historic_records:
            weight = float(record["weight"])
            waist = float(record["waist"])
            if model_gender == "male":
                a = waist * 0.74
                b = weight * 0.082 + 34.89
                fat_weight = a - b
                body_fat_rate = round((fat_weight / weight) * 100, 2)
                result.append(body_fat_rate)
            elif model_gender == "female":
                a = waist * 0.74
                b = weight * 0.082 + 44.74
                fat_weight = a - b
                body_fat_rate = round((fat_weight / weight) * 100, 2)
                result.append(body_fat_rate)
            else:
                pass
        return result

    def fetch_specified_body_measurement(self, body_measurement_key, historic_records):
        result = []
        for i in range(len(historic_records)):
            record = historic_records[i]
            result.append(record[body_measurement_key])
        return result

    def zip_combined_records(self, update_time_list,weight_list, bmi_list, bmr_list, body_fat_rate_list):
        result = []
        length = len(update_time_list)
        for i in range(length):
            record = {}
            record["update_time"] = update_time_list[i]
            record["weight"] = weight_list[i]
            record["bmi"] = bmi_list[i]
            record["bmr"] = bmr_list[i]
            record["body_fat_rate"] = body_fat_rate_list[i]
            result.append(record)
        return result

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

if __name__ == "__main__":

    ts = "2022-10-08 10:46:25"
    f = "%Y-%m-%d %H:%M:%S"
    print(str(datetime.datetime.strptime(ts,f).date()))