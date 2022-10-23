"""
Route management.

This provides all the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML static
to be displayed.

"""

import flask
from flask import *
from flask import g
from model import *
from contextlib import contextmanager
import os

"may be useful when the name of 'static' and 'templates' files change"
# app = flask.Flask(__name__, template_folder='templates', static_folder='static')

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SERVER_NAME'] = "127.0.0.1:5000"

# @app.before_first_request_funcs
# def before_request():
#     print("currently connect to real db")
model = Model()
model.create_database()

error_message = "No Special Characters Allowed ; # & ' < > -  , not empty input allowed and limit 50 characters!"


#####################################################
#   INDEX
#####################################################
@app.route('/')
def index():
    """
    If already login, go to step3
    Otherwise prompt login
     """
    # If the user has not logged in
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    # If the user has logged in, directly go to step3
    return redirect(url_for('complete_step3'))


#####################################################
#   REGISTER
#####################################################
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """
    Handle the register page
    Provides /register
    - [GET] viewing the register page
    - [POST] if submitting register detail - model name, check register
    """
    if 'logged_in' in session:
        return redirect(url_for('complete_step3'))

    if request.method == 'GET':
        return render_template('index.html')
    else:
        # get model name
        model_name = request.form.get('modelname')

        if model.check_user_input(model_name):
            # check the Special Characters
            if model.check_model_already_exists(model_name):
                # if the model name exists, recommend user to login or register another
                flash("The model name already exists, please login or register other names ", 'info')
                return redirect(url_for('register_page'))
            else:
                # move on step1
                resp = make_response(redirect(url_for('complete_step1')))
                resp.set_cookie('model_name', model_name)
                return resp

                # return redirect(url_for('complete_step1'))
        else:
            # special character input detect
            flash(error_message, 'warning')
            return redirect(url_for('register_page'))


#####################################################
#   LOGIN
#####################################################
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """ Here handles the login page
    Provides /login
        - [GET] If they are just viewing the page then render login page.
        - [POST] If submitting login details, check login.

    """
    # If the user has already logged in, directly go to step3 page
    if 'logged_in' in session:
        return redirect(url_for('complete_step3'))

    if request.method == 'GET':
        return render_template('index.html')

    else:
        model_name = request.form.get('modelname')
        print(model_name)

        if model.check_user_input(model_name):

            if model.check_model_already_exists(model_name):
                # No credential check, log user in
                session['logged_in'] = True
                age_and_gender = model.search_model_age_and_gender(model_name)
                age = age_and_gender[0][0]
                gender = age_and_gender[0][1]

                resp = make_response(redirect(url_for('complete_step3')))
                resp.set_cookie('model_name', model_name)
                resp.set_cookie('age', str(age))
                resp.set_cookie('gender', gender)
                return resp

            else:
                flash("Incorrect model name input, please try again or register", 'warning')
                return redirect(url_for('login_page'))
        else:
            # special character input detect
            flash(error_message, 'warning')
            return redirect(url_for('login_page'))




#####################################################
#   LOGOUT
#####################################################
@app.route('/logout')
def logout():
    """
    Logs out of the current session
        - Removes any stored human model data.
    """
    resp = make_response(redirect(url_for('index')))
    if 'logged_in' in session:
        session.pop('logged_in')
        resp.delete_cookie('model_name')
        resp.delete_cookie('age')
        resp.delete_cookie('gender')

    return resp


@app.route('/step1', methods=['GET', 'POST'])
def complete_step1():
    """ Handle the 1st step of the body visualizer """

    # If currently the user has logged in, directly go to step3 page
    if 'logged_in' in session:
        return redirect(url_for('complete_step3'))

    if request.method == 'GET':
        return render_template('step1.html')

    elif request.method == 'POST':
        # get the Age and Gender
        age = request.form.get('age')
        gender = request.form.get('gender')

        resp = make_response(redirect(url_for('complete_step2')))
        resp.set_cookie('age', age)
        resp.set_cookie('gender', gender)
        return resp


@app.route('/step2', methods=['GET', 'POST'])
def complete_step2():
    """ Handle the 3rd step of the body visualizer """
    if 'logged_in' in session:
        return redirect(url_for('complete_step3'))

    if request.method == 'GET':
        # load model name
        model_name = request.cookies.get('model_name')
        # define basic model
        age = request.cookies.get('age')
        gender = request.cookies.get('gender')

        # insert data to database
        basic_model = model.define_basic_model(age, gender)
        return render_template('step2.html', basic_model=basic_model)
    elif request.method == 'POST':
        if 'logged_in' not in session or not session['logged_in']:
            session['logged_in'] = True
            # # load model name
            model_name = request.cookies.get('model_name')
            # # define basic model
            age = request.cookies.get('age')
            gender = request.cookies.get('gender')
            # # insert data to database
            model.add_a_basic_human_model(model_name, age, gender)
            # basic_model = model.define_basic_model(int(age), gender)

            hair_color = request.form.get('hair_colour')
            skin_color = request.form.get('skin_colour')
            top_dress = request.form.get('top')
            bottom_dress = request.form.get('bot')
            basic_model_path = request.form.get("clothing_style")

            model.add_model_appearance(model_name, hair_color, skin_color, top_dress, bottom_dress, basic_model_path)

            latest_records = model.get_at_most_two_newest_body_measurement_record(model_name)
            if latest_records is None or len(latest_records) == 0:
                is_new_account = True
            else:
                is_new_account = False
            return redirect(url_for('complete_step3'))
        else:
            return redirect(url_for('complete_step3'))


@app.route('/step3', methods=['GET', 'POST'])
def complete_step3():
    """ Handle the 3rd step of the body visualizer """
    # If the user has not logged in
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    if request.method == 'GET':
        model_name = request.cookies.get('model_name')
        model_texture = model.search_model_texture_file_path(model_name)
        model_parameters = model.search_last_one_body_measurement_records(model_name)
        body_parameters_range = model.search_body_parameters_range(model_name)
        return render_template('step3.html',
                               model_texture=model_texture,
                               model_parameters=model_parameters,
                               body_parameters_range=body_parameters_range
                               )

    elif request.method == 'POST':

        # submit the body measurements to the database
        model_name = request.cookies.get('model_name')
        height = request.form.get('height')
        if height is None:
            height = 0
        weight = request.form.get('weight')
        thigh = request.form.get('thigh')
        shank = request.form.get('shank')
        hip = request.form.get('hip')
        arm_girth = request.form.get('Arm girth')
        arm_pan = request.form.get("Arms pan")
        waist = request.form.get('waist')
        chest = request.form.get('chest')

        # store the new body measurement into the database
        model.add_new_body_measurment_record(model_name, height, weight,
                                             thigh, shank, hip, arm_girth, arm_pan, waist, chest)

        return redirect(url_for('complete_step4'))


@app.route('/step4', methods=['GET', 'POST'])
def complete_step4():
    """ Generate a health report """
    # If the user has not logged in
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))
    if request.method == 'GET':
        model_name = request.cookies.get('model_name')

        # model texture path including: hair_color,skin_color,top_dress,bottom_dress,basic_model_path
        model_texture = model.search_model_texture_file_path(model_name)


        # basic model body parameters_range
        body_parameters_range = model.search_body_parameters_range(model_name)

        # if len(latest_records) = 2 , the 1st element is the second newest, the 2nd element is the newest
        latest_records = model.get_at_most_two_newest_body_measurement_record(model_name)

        # historic_records: a list of records,length <= 10
        historic_records = model.get_historic_body_measurement_records_to_be_displayed(model_name)

        # get latest 10 records
        weight_records = model.fetch_specified_body_measurement("weight", historic_records)
        # get latest 10 bmi
        bmi_records = model.calculate_bmi(historic_records)
        # get latest 10 bmr
        bmr_records = model.calculate_bmr(historic_records, request.cookies.get('gender'), request.cookies.get('age'))

        # get latest 10 bfr
        body_fat_rate_records = model.calculate_body_fat_rate(historic_records, bmi_records, request.cookies.get('gender'),request.cookies.get('age'))

        last_twenty_historic_records = model.get_last_twenty_body_measurement_records_to_be_displayed(model_name)
        # get latest 20 times
        last_twenty_update_time = model.fetch_specified_body_measurement("update_time", last_twenty_historic_records)
        # get latest 20 weights
        last_twenty_weight_records = model.fetch_specified_body_measurement("weight", last_twenty_historic_records)
        # get latest 20 bmr
        last_twenty_bmr_records = model.calculate_bmr(last_twenty_historic_records, request.cookies.get('gender'),
                                                      request.cookies.get('age'))
        # get latest 20 bmi
        last_twenty_bmi_records = model.calculate_bmi(last_twenty_historic_records)
        # get latest 20 bfr
        last_twenty_body_fate_rate_records = model.calculate_body_fat_rate(last_twenty_historic_records,last_twenty_bmi_records,
                                                                           request.cookies.get('gender'),request.cookies.get('age'))

        # get latest 20（update_time, weight, bmi, bmr, body_fat_rate）records
        last_twenty_combined_records = model.zip_combined_records(last_twenty_update_time, last_twenty_weight_records,
                                                                  last_twenty_bmi_records, last_twenty_bmr_records,
                                                                  last_twenty_body_fate_rate_records)

        is_male = request.cookies.get('gender') == "male"

        # check whether this is a new user
        if latest_records is None or len(latest_records) == 0:
            is_new_account = True
        else:
            is_new_account = False

        if latest_records is not None and len(latest_records) == 1:
            has_only_one_record = 1
        else:
            has_only_one_record = 0

        changed_parameters = []
        unchanged_parameters = []
        parameter_change_report = []
        times = []

        if not is_new_account and not has_only_one_record:
            old_time = latest_records[0]["update_time"]
            new_time = latest_records[1]["update_time"]
            times.append(old_time)
            times.append(new_time)
            changed_parameters, unchanged_parameters = model.generate_parameter_change_report(model_name,latest_records)

            parameter_change_report = changed_parameters+unchanged_parameters

        else:
            parameter_change_report = ["Thanks for taking a go at our Health Report page! We now have one of your " \
                                      "body measurement record in our database, well done! Please keep on using our website for your " \
                                      "body shape tracking! With one more record stored, we are able to offer you a brief and straightforward " \
                                      "summary to indicate how your body measurements have changed! Keep going! :)".format(model_name)]

        if not is_new_account:
            # bmi_report is a list of length 2, with first element the Evaluation，the second element the Information
            current_bmi = bmi_records[len(bmi_records)-1]
            bmi_report_list= model.generate_bmi_report(current_bmi)
        else:
            bmi_report_list = []

        if not is_new_account:
            # bmr_report is a list of length 2, with first element the Evaluation，the second element the Information
            current_bmr = bmr_records[len(bmr_records)-1]
            bmr_report_list = model.generate_bmr_report(current_bmr)
        else:
            bmr_report_list = []

        if not is_new_account:
            # bfr_report is a list of length 2, with first element the Evaluation，the second element the Information
            current_body_fat_rate = body_fat_rate_records[len(body_fat_rate_records)-1]
            bfr_report_list = model.generate_bfr_report(current_body_fat_rate,request.cookies.get("gender"))
            # print(bfr_report_list)
        else:
            bfr_report_list = []

        if not is_new_account:
            weight_report = model.generate_weight_report(latest_records,weight_records)
        else:
            weight_report =[]

        if historic_records is not None and len(historic_records) < 5:
            less_than_5_records = True
        else:
            less_than_5_records = False

        return render_template('step4.html',
                               model_texture=model_texture,
                               model_name = model_name,
                               body_parameters_range=body_parameters_range,
                               latest_records_original=latest_records,
                               latest_records =json.dumps(latest_records),
                               is_male=json.dumps(is_male),
                               historic_records=historic_records,
                               weight_records=weight_records,
                               bmi_records=bmi_records,
                               bmr_records=bmr_records,
                               body_fat_rate_records=body_fat_rate_records,
                               last_twenty_historic_records = last_twenty_historic_records,
                               last_twenty_weight_records = last_twenty_weight_records,
                               last_twenty_bmi_records = last_twenty_bmi_records,
                               last_twenty_bmr_records = last_twenty_bmr_records,
                               last_twenty_body_fate_rate_records = last_twenty_body_fate_rate_records,
                               last_twenty_combined_records = last_twenty_combined_records,
                               has_only_one_record = has_only_one_record,
                               parameter_change_report = json.dumps(parameter_change_report),
                               times = json.dumps(times),
                               bmi_report_list=bmi_report_list,
                               bmr_report_list=bmr_report_list,
                               bfr_report_list=bfr_report_list,
                               weight_report=weight_report,
                               less_than_5_records=less_than_5_records)


