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
        self.execute("DROP TABLE IF EXISTS Models ")
        self.commit()
        self.execute("DROP TABLE IF EXISTS ModelParameters ")
        self.commit()
        self.execute("DROP TABLE IF EXISTS Textures ")
        self.commit()
        self.execute("DROP TABLE IF EXISTS BasicModels ")
        self.commit()
        self.execute("DROP TABLE IF EXISTS ModelAppearance ")
        self.commit()

        # Create the users table
        self.execute("""
        CREATE TABLE Models(
            model_name TEXT NOT NULL,
            age INT,
            gender TEXT,
            PRIMARY KEY(model_name));
            
        CREATE TABLE ModelParameters(
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
        
        CREATE TABLE Textures(
            feature TEXT PRIMARY KEY NOT NULL,
            file_path TEXT NOT NULL
        );
        
        CREATE TABLE BasicModels(
            basic_model_name TEXT PRIMARY KEY NOT NULL,
            file_path TEXT NOT NULL  
        );
        
        CREATE TABLE ModelAppearance(
            model_name TEXT PRIMARY KEY NOT NULL REFERENCES Models(model_name),
            hair_color TEXT NOT NULL REFERENCES Textures(feature),
            skin_color TEXT NOT NULL REFERENCES Textures(feature),
            top_dress TEXT NOT NULL REFERENCES Textures(feature),
            bottom_dress TEXT NOT NULL REFERENCES Textures(feature),
            basic_model_name TEXT NOT NULL REFERENCES BasicModels(basic_model_name)
            
        );
        """)

        self.commit()

        # Add our admin model
        if not self.check_model_existence('admin'):
            self.add_model('admin', 20, 'Female')
        self.add_model_textures('black', '/black_hair')
        self.add_model_textures('yellow', '/yellow_skin')
        self.add_model_textures('T_shirt', '/T_shirt')
        self.add_model_textures('dress', '/dress')
        self.add_basic_model('adult_female', os.path.abspath('..') + '/adult_female')
        self.add_model_appearance('admin', 'black', 'yellow', 'T_shirt', 'dress', 'adult_female')
        self.add_new_body_measurement_record_with_time('admin', "2021-09-09 00:05:09", 1, 1, 1, 1, 1, 1, 1, 1,1)
        self.add_new_body_measurement_record_with_time('admin', "2020-09-09 00:05:09", 1, 1, 1, 1, 1, 1, 1, 1,1)
        self.add_new_body_measurement_record_with_time('admin', "2022-09-09 00:05:09", 1, 1, 1, 1, 1, 1, 1, 1,1)

        print("\nDatabase successfullly set up.\n")

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
                            SELECT update_time,height,weight,weight,shank,hip,arm_girth,arm_pan,waist,chest
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
                            SELECT update_time,height,weight,weight,shank,hip,arm_girth,arm_pan,waist,chest
                            FROM  ModelParameters  
                            WHERE model_name = '{model_name}'
                            ORDER BY update_time DESC LIMIT 1
                        """
        sql_query = sql_query.format(model_name=model_name)
        self.execute(sql_query)
        return self.cur.fetchall()
