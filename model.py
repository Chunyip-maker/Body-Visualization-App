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
        self.database.add_basic_model(model_name, age, gender)

    def check_user_input(self,string):
        if len(string) == 0:
            return False
        if len(string) > 50:
            return False
        for i in [";", "#", "&", "'", "<", ">", "-", " "]:
            ## find special characters
            if i in string:
                return False
        return True

    def add_new_body_measurment_record(self, model_name, update_time, height, weight,
                                       thigh, shank, hip, upper_arm, fore_arm, waist, chest
                                       ):
        result=self.database.add_new_body_measurement_record_with_time(model_name,update_time,height,weight,thigh,
                                            shank,hip,upper_arm,fore_arm,waist,chest)
        return result

