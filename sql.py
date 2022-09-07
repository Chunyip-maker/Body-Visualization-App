import sqlite3
import json


# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg="models.sqlite"):
        self.conn = sqlite3.connect(database_arg, check_same_thread=False)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    # -----------------------------------------------------------------------------

    # Sets up the database, and the initial table BasicModels to record the model
    def database_setup(self):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS BasicModels ")
        self.commit()

        # Create the users table
        self.execute("""
        CREATE TABLE BasicModels(
            model_name TEXT NOT NULL,
            age INT,
            gender TEXT,
            PRIMARY KEY(model_name));
            
        CREATE TABLE ModelParameters(
            model_name TEXT NOT NULL,
            update_time TEXT,
            height REAL,
            weight REAL,
            thigh REAL,
            shank REAL,
            hip REAL,
            upper_arm REAL,
            fore_arm REAL,
            waist REAL,
            chest REAL,
            PRIMARY KEY(model_name, update_time),
            FOREIGN KEY (model_name) REFERENCES BasicModels(model_name)
        );
        )""")

        self.commit()


        # Add our admin model
        if not self.check_model_existence('admin'):
            self.add_basic_model('admin',20,'Male')

        print("\nDatabase successfullly set up.\n")


    # -----------------------------------------------------------------------------
    # Model Existence Check
    # -----------------------------------------------------------------------------
    # Return True if the model already exists, otherwise false
    def check_model_existence(self, model_name):
        sql_query = """
            SELECT 1
            FROM BasicModels
            WHERE model_name = '{model_name}'
        """
        sql_query = sql_query.format(model_name=model_name)

        if self.cur.execute(sql_query).fetchone():
            return True
        else:
            return False

    # -----------------------------------------------------------------------------
    # Human Model Basic Data Adding (model_name, age, gender)
    # -----------------------------------------------------------------------------
    # Add a model to the database table BasicModels
    def add_basic_model(self, model_name,age, gender):
        sql_cmd = """
                INSERT INTO BasicModels
                VALUES('{model_name}', '{age}', '{gender}')
            """

        sql_cmd = sql_cmd.format(model_name=model_name, age=age,gender=gender)
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    # Add a new record of a model's body measurement with timestamp
    # -----------------------------------------------------------------------------
    def add_new_body_measurement_record_with_time(self,model_name, update_time, height, weight,
                                       thigh, shank, hip, upper_arm, fore_arm, waist, chest
                                       ):
        sql_cmd = """
            INSERT INTO ModelParameters
            VALUES('{model_name}', '{update_time}','{height}','{weight}', '{thigh}',
            '{shank}','{hip}','{upper_arm}','{fore_arm}','{waist}','{chest}')
        """
        sql_cmd = sql_cmd.format(model_name=model_name,
                                 update_time=update_time,
                                 height=height,
                                 weight=weight,
                                 thigh=thigh,
                                 shank=shank,
                                 hip=hip,
                                 upper_arm=upper_arm,
                                 fore_arm=fore_arm,
                                 waist=waist,
                                 chest=chest)
        self.execute(sql_cmd)
        self.commit()
        return True


    # -----------------------------------------------------------------------------
    #
    # # Check login credentials
    # def check_credentials(self, username, password):
    #     sql_query = """
    #             SELECT 1
    #             FROM Users
    #             WHERE username = '{username}' AND password = '{password}'
    #         """
    #
    #     sql_query = sql_query.format(username=username, password=password)
    #
    #     # If our query returns
    #     if self.cur.fetchone():
    #         return True
    #     else:
    #         return False
