import os
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
        # self.execute("DROP TABLE IF EXISTS Models ")
        # self.commit()
        # self.execute("DROP TABLE IF EXISTS ModelParameters ")
        # self.commit()
        # self.execute("DROP TABLE IF EXISTS Textures ")
        # self.commit()
        # self.execute("DROP TABLE IF EXISTS BasicModels ")
        # self.commit()
        # self.execute("DROP TABLE IF EXISTS ModelAppearance ")
        # self.commit()
        # self.execute("DROP TABLE IF EXISTS AgeGroupParametersRange ")
        # self.commit()

        # Create the users table
        self.execute("""
        CREATE TABLE IF NOT EXISTS Models(
            model_name TEXT NOT NULL,
            age INT,
            gender TEXT,
            PRIMARY KEY(model_name));
            
        CREATE TABLE IF NOT EXISTS  ModelParameters(
            model_name TEXT NOT NULL,
            update_time DATETIME,
            height REAL,
            weight REAL,
            thigh REAL,
            shank REAL,
            hip REAL,
            arm_girth REAL,
            arm_pan REAL,
            waist REAL,
            chest REAL,
            PRIMARY KEY(model_name, update_time),
            FOREIGN KEY (model_name) REFERENCES Models(model_name)
        );
        
        CREATE TABLE IF NOT EXISTS Textures(
            feature TEXT PRIMARY KEY NOT NULL,
            file_path TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS BasicModels(
            basic_model_name TEXT PRIMARY KEY NOT NULL,
            file_path TEXT NOT NULL  
        );
        
        CREATE TABLE IF NOT EXISTS ModelAppearance(
            model_name TEXT PRIMARY KEY NOT NULL REFERENCES Models(model_name),
            hair_color TEXT NOT NULL REFERENCES Textures(feature),
            skin_color TEXT NOT NULL REFERENCES Textures(feature),
            top_dress TEXT NOT NULL REFERENCES Textures(feature),
            bottom_dress TEXT NOT NULL REFERENCES Textures(feature),
            basic_model_name TEXT NOT NULL REFERENCES BasicModels(basic_model_name)
            
        );
        
        CREATE TABLE IF NOT EXISTS AgeGroupParametersRange(
            age_group TEXT PRIMARY KEY NOT NULL,
            height_max REAL,
            height_min REAL,
            weight_max REAL,
            weight_min REAL,
            chest_max REAL,
            chest_min REAL,
            waist_max REAL,
            waist_min REAL,
            hip_max REAL,
            hip_min REAL,
            arm_girth_max REAL,
            arm_girth_min REAL,
            arm_pan_max REAL,
            arm_pan_min REAL,
            thigh_max REAL,
            thigh_min REAL,
            shank_max REAL,
            shank_min REAL
        );
        """)

        self.commit()

        # Add our admin model
        if self.check_table_is_empty("Models") and not self.check_model_existence('admin'):
            self.add_model('admin', 20, 'male')

        # Only add data when the tables are empty
        if self.check_table_is_empty("Textures"):
            self.add_model_textures('black', '/black_hair')
            self.add_model_textures('yellow', '/yellow_skin')
            self.add_model_textures('T_shirt', '/T_shirt')
            self.add_model_textures('dress', '/dress')

        if self.check_table_is_empty("BasicModels"):
            self.add_basic_model('adult_female', os.path.abspath('..') + '/adult_female')

        if self.check_table_is_empty("ModelAppearance"):
            self.add_model_appearance('admin', 'black', 'yellow', 'T_shirt', 'dress', 'adult_female')

        if self.check_table_is_empty("ModelParameters"):
            self.add_new_body_measurement_record_with_time('admin', "2021-09-09 00:05:09", 1, 1, 1, 1, 1, 1, 1, 1,1)
            self.add_new_body_measurement_record_with_time('admin', "2020-09-09 00:05:09", 1, 1, 1, 1, 1, 1, 1, 1,1)
            self.add_new_body_measurement_record_with_time('admin', "2022-09-09 00:05:09", 1, 1, 1, 1, 1, 1, 1, 1,1)

        if self.check_table_is_empty("AgeGroupParametersRange"):
            self.add_age_group_parameters_range()

        # print("\nDatabase successfullly set up.\n")

    # -----------------------------------------------------------------------------
    # Check if a table is empty or not
    # -----------------------------------------------------------------------------
    # Return True if the table is empty, otherwise false
    def check_table_is_empty(self, table_name):
        sql_query="""
            SELECT COUNT(*) 
            FROM (
                select 0 
                from '{table_name}'
                limit 1);
        """
        sql_query = sql_query.format(table_name=table_name)
        result = self.cur.execute(sql_query).fetchone()
        if result[0] == 0:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------
    # Model Existence Check
    # -----------------------------------------------------------------------------
    # Return True if the model already exists, otherwise false
    def check_model_existence(self, model_name):
        sql_query = """
            SELECT 1
            FROM Models
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
    # Add a model to the database table Models
    def add_model(self, model_name, age, gender):
        sql_cmd = """
                INSERT INTO Models
                VALUES('{model_name}', '{age}', '{gender}')
            """

        sql_cmd = sql_cmd.format(model_name=model_name, age=age, gender=gender)
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    # Add a new record of a model's body measurement with timestamp
    # -----------------------------------------------------------------------------
    def add_new_body_measurement_record_with_time(self, model_name, update_time, height, weight,
                                                  thigh, shank, hip, arm_girth, arm_pan, waist, chest
                                                  ):
        sql_cmd = """
            INSERT INTO ModelParameters
            VALUES('{model_name}', '{update_time}','{height}','{weight}', '{thigh}',
            '{shank}','{hip}','{arm_girth}','{arm_pan}','{waist}','{chest}')
        """
        sql_cmd = sql_cmd.format(model_name=model_name,
                                 update_time=update_time,
                                 height=height,
                                 weight=weight,
                                 thigh=thigh,
                                 shank=shank,
                                 hip=hip,
                                 arm_girth=arm_girth,
                                 arm_pan=arm_pan,
                                 waist=waist,
                                 chest=chest)
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    #  Model Appearance Data Adding
    # -----------------------------------------------------------------------------
    def add_model_appearance(self, model_name, hair_color, skin_color, top_dress, bottom_dress, basic_model_name):
        sql_cmd = """
                    INSERT INTO ModelAppearance
                    VALUES('{model_name}', '{hair_color}','{skin_color}','{top_dress}', '{bottom_dress}',
                    '{basic_model_name}')
                """
        sql_cmd = sql_cmd.format(model_name=model_name,
                                 hair_color=hair_color,
                                 skin_color=skin_color,
                                 top_dress=top_dress,
                                 bottom_dress=bottom_dress,
                                 basic_model_name=basic_model_name
                                 )
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    #  Model Texture Data Adding (feature, file_path)
    # -----------------------------------------------------------------------------
    def add_model_textures(self, feature, file_path):
        sql_cmd = """
                    INSERT INTO Textures
                    VALUES('{feature}', '{file_path}')
                """
        sql_cmd = sql_cmd.format(feature=feature,
                                 file_path=file_path)
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    #  Basic Model  Data Adding (basic_model_name, file_path)
    # -----------------------------------------------------------------------------
    def add_basic_model(self, basic_model_name, file_path):
        sql_cmd = """
                    INSERT INTO BasicModels
                    VALUES('{basic_model_name}', '{file_path}')
                """
        sql_cmd = sql_cmd.format(basic_model_name=basic_model_name,
                                 file_path=file_path)
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    #  Add basic model parameters range (Max and Min value)
    # -----------------------------------------------------------------------------
    def add_age_group_parameters_range(self):
        sql_cmd = """
                       INSERT INTO AgeGroupParametersRange
                       VALUES
                       ('teenager_male',130, 180, 30, 90, 75, 95, 60, 80, 75, 95, 20, 35, 35, 50, 40, 58, 22, 40),
                       ('teenager_female',130, 180, 30, 90, 70, 90, 45, 65, 70, 90, 15, 30, 30, 40, 37, 45, 20, 38),
                       ('adult_male',160, 210, 40, 100, 85, 105, 70, 90, 85, 105, 25, 40, 40, 55, 48, 66, 30, 48),
                       ('adult_female',150, 200, 30, 90, 80, 100, 55, 75, 80, 100, 15, 30, 34, 44, 45, 63, 28, 46),
                       ('middle_male',160, 210, 40, 100, 90, 110, 75, 95, 85, 105, 25, 40, 40, 55, 48, 66, 30, 48),
                       ('middle_female',150, 200, 30, 90, 85, 105, 65, 85, 80, 100, 15, 30, 34, 44, 45, 63, 28, 46),
                       ('old_male',155, 205, 40, 100, 90, 110, 75, 95, 85, 105, 25, 40, 40, 55, 48, 66, 30, 48 ),
                       ('old_female',145, 195, 30, 90, 85, 105, 65, 85, 80, 100, 15, 30, 34, 44, 45, 63, 28, 46);
                       
                   """
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    #  Search  Model age and gender by model name
    # -----------------------------------------------------------------------------
    def search_model_age_and_gender(self, model_name):
        sql_query = """
                    SELECT age,gender
                    FROM Models
                    WHERE model_name = '{model_name}'
                """
        sql_query = sql_query.format(model_name=model_name)

        self.execute(sql_query)
        return self.cur.fetchall()

    # -----------------------------------------------------------------------------
    #  Search Basic Model file path
    # -----------------------------------------------------------------------------
    def search_basic_model_file_path(self, model_name):
        sql_query = """
                    SELECT file_path
                    FROM BasicModels JOIN ModelAppearance USING (basic_model_name)
                    WHERE model_name = '{model_name}'
                """
        sql_query = sql_query.format(model_name=model_name)

        self.execute(sql_query)
        return self.cur.fetchall()

    # -----------------------------------------------------------------------------
    #  Search Model Texture file path
    # -----------------------------------------------------------------------------
    def search_model_texture_file_path(self, model_name):

        # sql_query = """
        #                     SELECT file_path
        #                     FROM  Textures  JOIN ModelAppearance
        #                     WHERE model_name = '{model_name}'
        #                 """
        sql_query = """
                                    SELECT hair_color,skin_color,top_dress,bottom_dress
                                    FROM  ModelAppearance 
                                    WHERE model_name = '{model_name}'
                                """
        sql_query = sql_query.format(model_name=model_name)
        self.execute(sql_query)
        return self.cur.fetchall()[0]

    # -----------------------------------------------------------------------------
    # Last two body measurement records
    # -----------------------------------------------------------------------------
    def search_last_two_body_measurement_records(self, model_name):
        sql_query = """
                            SELECT update_time,height,weight,chest,waist,hip,arm_girth,arm_pan,thigh,shank
                            FROM  ModelParameters  
                            WHERE model_name = '{model_name}'
                            ORDER BY update_time DESC LIMIT 2
                        """
        sql_query = sql_query.format(model_name=model_name)
        self.execute(sql_query)
        return self.cur.fetchall()

    # -----------------------------------------------------------------------------
    # the Last one body measurement record
    # -----------------------------------------------------------------------------
    def search_last_one_body_measurement_record(self, model_name):
        sql_query = """
                            SELECT update_time,height,weight,chest,waist,hip,arm_girth,arm_pan,thigh,shank
                            FROM  ModelParameters  
                            WHERE model_name = '{model_name}'
                            ORDER BY update_time DESC LIMIT 1
                        """
        sql_query = sql_query.format(model_name=model_name)
        self.execute(sql_query)
        return self.cur.fetchall()

    # -----------------------------------------------------------------------------
    # Search model parameters range by age group
    # -----------------------------------------------------------------------------
    def search_body_parameters_range(self, age_group):
        sql_query = """
                            SELECT *
                            FROM  AgeGroupParametersRange  
                            WHERE age_group = '{age_group}'
                        """
        sql_query = sql_query.format(age_group=age_group)
        self.execute(sql_query)
        return self.cur.fetchall()

    # -----------------------------------------------------------------------------
    # Search the newest 2 body measurement records for a model
    # -----------------------------------------------------------------------------
    def get_two_newest_body_measurement(self, model_name):
        sql_query = """
                    SELECT *
                    FROM ModelParameters
                    WHERE model_name = '{model_name}'
                    ORDER BY update_time DESC
                    LIMIT 2
        """
        sql_query = sql_query.format(model_name=model_name)
        self.execute(sql_query)
        return self.cur.fetchall()

if __name__=="__main__":
    database = SQLDatabase()
    database.database_setup()


