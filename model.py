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
        if model_name is None:
            return
        return self.database.search_model_texture_file_path(model_name)

    def search_last_one_body_measurement_records(self, model_name):
        if model_name is None:
            return
        model_parameters = self.database.search_last_one_body_measurement_record(model_name)
        if len(model_parameters) == 0:
            return self.define_new_model_body_parameters(model_name)
        return model_parameters[0]

    def search_body_parameters_range(self, model_name):
        if model_name is None:
            return
        age_and_gender = self.search_model_age_and_gender(model_name)
        if len(age_and_gender)==0:
            return None
        age_group = self.define_basic_model(age_and_gender[0][0],age_and_gender[0][1])
        body_parameters_range = self.database.search_body_parameters_range(age_group)
        if len(body_parameters_range) ==0:
            return None
        return body_parameters_range[0]

    def search_model_age_and_gender(self, model_name):
        age_and_gender = self.database.search_model_age_and_gender(model_name)
        return age_and_gender

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
            entry["update_time"] = self.convert_time(raw_result[1])
            # entry["update_time"] = raw_result[1]
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
                entry["update_time"] = self.convert_time(raw_result[1])
                # entry["update_time"] = raw_result[1]
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
                entry["update_time"] = self.convert_time(raw_result[1])
                # entry["update_time"] = raw_result[1]
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
            entry["update_time"] = self.convert_time(raw_result[1])
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

    def convert_time(self, datetime_from_sql):

        result = datetime.datetime.strptime(datetime_from_sql, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d, %H:%M")
        return result

    def calculate_bmi(self, historic_records):
        if historic_records is None:
            return
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
        if model_gender is None or model_age is None or historic_records is None:
            return
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

    def calculate_body_fat_rate(self, historic_records, bmi_records,model_gender,model_age):
        if model_age is None or model_gender is None :
            return
        if historic_records is None or bmi_records is None:
            return
        result = []
        for i in range(len(historic_records)):
            record = historic_records[i]
            record_bmi = bmi_records[i]
            weight = float(record["weight"])
            waist = float(record["waist"])
            model_age = int(model_age)
            if model_gender == "male":
                body_fat_rate = 1.2*record_bmi + 0.23*model_age - 16.2
                body_fat_rate = int(round(body_fat_rate, 0))
                result.append(body_fat_rate)
            elif model_gender == "female":
                body_fat_rate = 1.2 * record_bmi + 0.23 * model_age - 5.4
                body_fat_rate = int(round(body_fat_rate, 0))
                result.append(body_fat_rate)
            else:
                pass
        return result

    def fetch_specified_body_measurement(self, body_measurement_key, historic_records):
        if historic_records is None or body_measurement_key is None:
            return
        result = []
        for i in range(len(historic_records)):
            record = historic_records[i]
            result.append(record[body_measurement_key])
        return result

    def zip_combined_records(self, update_time_list,weight_list, bmi_list, bmr_list, body_fat_rate_list):
        if update_time_list is None or weight_list is None:
            return
        if bmi_list is None or bmr_list is None:
            return
        if body_fat_rate_list is None:
            return
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

    def generate_parameter_change_report(self, model_name,latest_records):
        if model_name is None or latest_records is None:
            return

        result = ""
        old_record = latest_records[0]
        new_record = latest_records[1]

        old_time = latest_records[0]["update_time"]
        new_time = latest_records[1]["update_time"]

        # intro paragraph
        intro = "Hi, {model_name}! Your body change from {old_time} to {new_time} is summarized as below:\n\n".format(
            model_name=model_name,
            old_time=old_time,
            new_time=new_time
        )
        result += intro

        # paragraph to display parameters that have changes
        second_paragraph = ""
        parameters =["height", "weight", "thigh", "shank","hip", "arm_girth","arm_pan","waist", "chest"]
        temp = [] # store the parameter of which the value is not changed
        unit_map = {"height":"cm","weight":"kg","thigh":"cm","shank":"cm","hip":"cm","arm_girth":"cm","arm_pan":"cm","waist":"cm", "chest":"cm"}
        for key in parameters:
            if old_record[key] == new_record[key]:
                temp.append(key)
            else:
                if old_record[key] < new_record[key]:
                    row = "{parameter} : Increase by {diff}{unit}, from {old_value}{unit} to {new_value}{unit}\n".format(
                        parameter=key.replace("_"," ").upper(),
                        diff=new_record[key]-old_record[key],
                        old_value=old_record[key],
                        new_value=new_record[key],
                        unit=unit_map[key]
                    )
                else:
                    row = "{parameter} : Decrease by {diff}{unit}, from {old_value}{unit} to {new_value}{unit}\n".format(
                        parameter=key.replace("_"," ").upper(),
                        diff=old_record[key] - new_record[key],
                        old_value=old_record[key],
                        new_value=new_record[key],
                        unit=unit_map[key]
                    )
                second_paragraph += row

        if second_paragraph != "":
            result += second_paragraph+"\n"

        #paragraph to display parameters that have no changes
        third_paragraph = ""
        for key in temp:
            row = "{parameter} : Remain unchanged at {old_value}{unit}\n".format(
                parameter=key.replace("_", " ").upper(),
                old_value=old_record[key],
                unit=unit_map[key]
            )
            third_paragraph += row
        result += third_paragraph

        return result

    def generate_bmi_report(self, bmi):
        result = []
        category = ""
        if bmi < 18.5:
            category = "underweight"
        elif bmi <= 24.9:
            category = "normal"
        elif bmi <= 29.9:
            category = "overweight"
        else:
            category = "obese"
        result.append ("Your current body mass index (BMI) is {bmi}. This BMI falls within a {category} range. ".format(
            bmi=bmi,
            category=category
        ))
        result.append("Body mass index (BMI) is a person’s weight in kilograms "+
                      "divided by the square of height in meters. BMI is an "+
                      "inexpensive and easy screening method for weight "+
                      "categories—underweight, healthy weight, overweight,"+
                      " and obesity. If your BMI is below 18.5, it falls within"+
                      " the underweight. If your BMI is 18.5 to 24.9, it falls within "+
                      "the normal or Healthy Weight range. "+
                      "If your BMI is 25.0 to 29.9, it falls within the overweight range. "+
                      "If your BMI is 30.0 or higher, it falls within the obese range")
        return result

    def generate_bmr_report(self,bmr):
        result = []
        result.append("As for your basal metabolic rate (BMR), you are currently suggested to take in at least {bmr} calories from your daily meal".format(
            bmr=bmr
        ))
        result.append("Basal Metabolic Rate is the number of calories required to keep your body functioning at rest. BMR is also known as your body\'s metabolism; therefore, any increase to your metabolic weight, such as exercise, will increase your BMR.Most people\'s BMR is between 1000 – 2000.")
        return result

    def generate_bfr_report(self,body_fat_rate, gender):
        result = []
        if gender is None:
            return
        if gender == "male":
            if body_fat_rate < 5:
                category = "abnormal"
            elif body_fat_rate <= 24:
                category = "healthy"
            else:
                category = "obese"
        elif gender == "female":
            if body_fat_rate < 10:
                category = "abnormal"
            elif body_fat_rate <= 31:
                category = "healthy"
            else:
                category = "obese"
        result.append("Your current body fat rate is {bfr}%. This body fate rate falls within the {category} range.".format(
            bfr=body_fat_rate,
            category=category
        ))
        result.append("The body fat rate of a human or other living being is the total mass of fat divided by total body mass, multiplied by 100; body fat includes essential body fat and storage body fat. Essential body fat is necessary to maintain life and reproductive functions. The percentage of essential body fat for women is greater than that for men, due to the demands of childbearing and other hormonal functions.For a man, 2–5% fat is essential, 2–24% fat is considered healthy, and more than 25% classifies as obesity. For a woman, 10–13% fat is essential, 10–31% fat is healthy, and more than 32% classifies as obesity.")
        return result

if __name__ == "__main__":
    a = 23.7751
    print(int(round(a,0)))
    # print("Datetime with out seconds",datetime.datetime.strptime("2022-10-12 21:30:30","%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d, %H:%M"))