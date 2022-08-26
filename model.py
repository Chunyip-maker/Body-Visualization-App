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
