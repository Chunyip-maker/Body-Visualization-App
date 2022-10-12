"""
Route management.

This provides all the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML static
to be displayed.

"""

import flask
from flask import *
from model import *
from contextlib import contextmanager
import os

"may be useful when the name of 'static' and 'templates' files change"
# app = flask.Flask(__name__, template_folder='templates', static_folder='static')

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SERVER_NAME'] = "127.0.0.1:5000"
model = Model()
response = Response()

error_message = "No Special Characters Allowed ; # & ' < > -  , not empty input allowed and limit 50 characters!"


#####################################################
#   INDEX
#####################################################
@app.route('/')
def index():
    """
    If already login( 即之前已输入过model name ), go to step3
    Otherwise prompt login
     """
    # 如果未登录
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    # 如果已经登陆过，直接跳转至step3.html开始调身体参数捏人
    return redirect(url_for('complete_step3'))


#####################################################
#   REGISTER
#####################################################
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """
    Here handles the register page
    Provides /register
    - [GET] viewing the register page
    - [POST] if submitting register detail - model name, check register
    """
    # 如果已经登陆过，直接跳转至step3.html开始调身体参数捏人
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

                # global human_model_details
                # human_model_details['model_name'] = model_name
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
    # 如果已经登陆过，直接跳转至step3.html开始调身体参数捏人
    if 'logged_in' in session:
        return redirect(url_for('complete_step3'))

    if request.method == 'GET':
        return render_template('index.html')

    else:
        model_name = request.form.get('modelname')  # 前端请用'modelname'
        print(model_name)

        if model.check_user_input(model_name):

            if model.check_model_already_exists(model_name):
                # No credential check, log user in
                session['logged_in'] = True
                age_and_gender = model.search_model_age_and_gender(model_name)
                age = age_and_gender[0][0]
                gender = age_and_gender[0][1]
                # print(age_and_gender[0][0])

                # Store the user details for us to use throughout
                # global human_model_details
                # human_model_details['model_name'] = model_name

                resp = make_response(redirect(url_for('complete_step3')))
                resp.set_cookie('model_name', model_name)
                resp.set_cookie('age', str(age))
                resp.set_cookie('gender', gender)
                return resp

                # 如果该模型已存在,跳转到step3.html
                # return redirect(url_for('complete_step3'))
            else:
                flash("Incorrect model name input, please try again or register", 'warning')
                return redirect(url_for('login_page'))
        else:
            # special character input detect
            flash(error_message, 'warning')
            return redirect(url_for('login_page'))

        # else:
        #     # 如果该模型还未创建完成（name, age, gender都有），那么跳转到step1.html
        #     return redirect(url_for('complete_step1'))


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
    # return redirect(url_for('index'))


@app.route('/step1', methods=['GET', 'POST'])
def complete_step1():
    """ Handle the 1st step of the body visualizer """

    # 如果已经登陆过，直接跳转至step3.html开始调身体参数捏人
    if 'logged_in' in session:
        return redirect(url_for('complete_step3'))

    if request.method == 'GET':
        return render_template('step1.html')

    elif request.method == 'POST':
        # 获取性别年龄，
        age = request.form.get('age')
        gender = request.form.get('gender')

        # model_name = human_model_details['model_name']
        # print("{},{},{}".format(model_name,age,gender))
        # model.add_a_basic_human_model(model_name, age, gender)
        resp = make_response(redirect(url_for('complete_step2')))
        resp.set_cookie('age', age)
        resp.set_cookie('gender', gender)
        return resp

        # return redirect(url_for('complete_step2'))


@app.route('/step2', methods=['GET', 'POST'])
def complete_step2():
    """ Handle the 3rd step of the body visualizer """
    # 如果已经登陆过，直接跳转至step3.html开始调身体参数捏人
    if 'logged_in' in session:
        return redirect(url_for('complete_step3'))

    if request.method == 'GET':
        # load model name
        model_name = request.cookies.get('model_name')

        # define basic model
        age = request.cookies.get('age')
        gender = request.cookies.get('gender')
        # basic_model = model.define_basic_model(int(age), gender)

        # insert data to database
        basic_model = model.define_basic_model(age, gender)
        return render_template('step2.html', basic_model=basic_model)
    elif request.method == 'POST':
        # 如果未登录 -- 未完成注册系统都不识别为登录成功
        if 'logged_in' not in session or not session['logged_in']:
            session['logged_in'] = True
            # # load model name
            model_name = request.cookies.get('model_name')
            #
            # # define basic model
            age = request.cookies.get('age')
            gender = request.cookies.get('gender')
            # basic_model = model.define_basic_model(age, gender)
            # # insert data to database
            model.add_a_basic_human_model(model_name, age, gender)
            # basic_model = model.define_basic_model(int(age), gender)

            hair_color = request.form.get('hair_colour')  # 头发颜色
            skin_color = request.form.get('skin_colour')  # 皮肤颜色
            top_dress = request.form.get('top')  # 上衣
            bottom_dress = request.form.get('bot')  # 下装
            basic_model_path = request.form.get("clothing_style")  # 基础模型的路径

            # hair_color = model.split_mesh_name(hair_color)
            # skin_color = model.split_mesh_name(skin_color)
            # top_dress = model.split_mesh_name(top_dress)
            # bottom_dress = model.split_mesh_name(bottom_dress)

            model.add_model_appearance(model_name, hair_color, skin_color, top_dress, bottom_dress, basic_model_path)

            # 暂时没用
            # textures_file_path = model.search_model_texture_file_path(model_name)
            # basic_model_file_path = model.search_basic_model_file_path(model_name)
            return redirect(url_for('complete_step3'))
        else:
            return redirect(url_for('complete_step3'))


@app.route('/step3', methods=['GET', 'POST'])
def complete_step3():
    """ Handle the 3rd step of the body visualizer """
    # 如果未登录
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    # flash("welcome " + human_model_details['model_name'], 'success')
    if request.method == 'GET':
        # print("~"*45)
        model_name = request.cookies.get('model_name')
        model_texture = model.search_model_texture_file_path(model_name)
        # print(model_texture)
        model_parameters = model.search_last_one_body_measurement_records(model_name)
        body_parameters_range = model.search_body_parameters_range(model_name)
        is_new_model= len(model.get_historic_body_measurement_records_to_be_displayed(model_name)) == 0
        print("NewModel: "+str(is_new_model))
        # print(model_parameters)
        return render_template('step3.html',
                               is_new_model=is_new_model,
                               model_texture=model_texture,
                               model_parameters=model_parameters,
                               body_parameters_range=body_parameters_range)

    elif request.method == 'POST':
        # 提交7项参数入库
        # model_name = human_model_details['model_name']
        model_name = request.cookies.get('model_name')
        height = request.form.get('height')
        if height is None:  # 成年人不能改变身高，默认值为0
            height = 0
        weight = request.form.get('weight')
        thigh = request.form.get('thigh')  # 大腿
        shank = request.form.get('shank')  # 小腿
        hip = request.form.get('hip')  # 臀围
        arm_girth = request.form.get('Arm girth')  # 胳膊
        arm_pan = request.form.get("Arms pan")
        waist = request.form.get('waist')
        chest = request.form.get('chest')

        # store the new body measurement into the database
        model.add_new_body_measurment_record(model_name, height, weight,
                                             thigh, shank, hip, arm_girth, arm_pan, waist, chest)

        # return render_template('step4.html')
        return redirect(url_for('complete_step4'))


@app.route('/step4', methods=['GET', 'POST'])
def complete_step4():
    """ Generate a health report """
    # 如果未登录
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))



    if request.method == 'GET':
        model_name = request.cookies.get('model_name')

        # model texture path including: hair_color,skin_color,top_dress,bottom_dress,basic_model_path
        model_texture = model.search_model_texture_file_path(model_name)


        # basic model body parameters_range
        body_parameters_range = model.search_body_parameters_range(model_name)

        # latest_records: a list of records，record可能仅一个（因为是新用户），也可能为两个，每个record以字典形式保存body measurement
        # 如果len(latest_records) = 2 ，第一个是次新的，第二个是最新的
        latest_records = model.get_at_most_two_newest_body_measurement_record(model_name)

        # historic_records: a list of records，record最多有十个，按时间均匀分布，包含最新数据和最老数据，每个record以字典形式保存body measurement
        historic_records = model.get_historic_body_measurement_records_to_be_displayed(model_name)

        # 抽取最近十次的体重
        weight_records = model.fetch_specified_body_measurement("weight", historic_records)
        # 计算出最近十次的bmi
        bmi_records = model.calculate_bmi(historic_records)
        # 计算出最近十次的基础代谢率bmr
        bmr_records = model.calculate_bmr(historic_records, request.cookies.get('gender'), request.cookies.get('age'))

        # 计算出最近十次的体脂率
        body_fat_rate_records = model.calculate_body_fat_rate(historic_records, bmi_records, request.cookies.get('gender'),request.cookies.get('age'))

        last_twenty_historic_records = model.get_last_twenty_body_measurement_records_to_be_displayed(model_name)
        # 抽取最近20次的时间
        last_twenty_update_time = model.fetch_specified_body_measurement("update_time", last_twenty_historic_records)
        # 抽取最近20次体重
        last_twenty_weight_records = model.fetch_specified_body_measurement("weight", last_twenty_historic_records)
        # 计算出最近20次基础代谢率
        last_twenty_bmr_records = model.calculate_bmr(last_twenty_historic_records, request.cookies.get('gender'),
                                                      request.cookies.get('age'))
        # 计算出最近20次bmi
        last_twenty_bmi_records = model.calculate_bmi(last_twenty_historic_records)
        # 计算出最近20次体脂率
        last_twenty_body_fate_rate_records = model.calculate_body_fat_rate(last_twenty_historic_records,last_twenty_bmi_records,
                                                                           request.cookies.get('gender'),request.cookies.get('age'))

        # 获得最近二十次的（update_time, weight, bmi, bmr, body_fat_rate）记录
        last_twenty_combined_records = model.zip_combined_records(last_twenty_update_time, last_twenty_weight_records,
                                                                  last_twenty_bmi_records, last_twenty_bmr_records,
                                                                  last_twenty_body_fate_rate_records)

        is_male = request.cookies.get('gender') == "male"

        # 判断是否为新用户，即无历史记录
        if len(latest_records) == 0:
            is_new_account = True
        else:
            is_new_account = False

        if len(latest_records) == 1:
            has_only_one_record = True
        else:
            has_only_one_record = False

        if not is_new_account and not has_only_one_record:
            parameter_change_report = model.generate_parameter_change_report(model_name,latest_records)
            print(parameter_change_report)
        else:
            parameter_change_report = "As you are currently a new model, there is currently no historic data for your body parameter comparison :(\n"
            print(parameter_change_report)

        if not is_new_account:
            # bmi_report是一个长度为2的list，第一个element是评价，第二个是科普信息
            current_bmi = bmi_records[len(bmi_records)-1]
            bmi_report_list= model.generate_bmi_report(current_bmi)
            print(bmi_report_list)
        else:
            bmi_report_list = []

        if not is_new_account:
            # bmr_report是一个长度为2的list，第一个element是评价，第二个是科普信息
            current_bmr = bmr_records[len(bmr_records)-1]
            bmr_report_list = model.generate_bmr_report(current_bmr)
            print(bmr_report_list)
        else:
            bmr_report_list = []

        if not is_new_account:
            # bfr_report是一个长度为2的list，第一个element是评价，第二个是科普信息
            current_body_fat_rate = body_fat_rate_records[len(body_fat_rate_records)-1]
            bfr_report_list = model.generate_bfr_report(current_body_fat_rate,request.cookies.get("gender"))
            print(bfr_report_list)
        else:
            bfr_report_list = []

        if len(historic_records) < 5:
            less_than_5_records = True
        else:
            less_than_5_records = False

        print("Less than 5 records: "+str(less_than_5_records))

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
                               parameter_change_report=parameter_change_report,
                               bmi_report_list=bmi_report_list,
                               bmr_report_list=bmr_report_list,
                               bfr_report_list=bfr_report_list,
                               less_than_5_records=less_than_5_records)


# # for test only
# @app.route('/test', methods=['GET', 'POST'])
# def complete_test():
#     """ Handle the 3rd step of the body visualizer """
#     # 如果已经登陆过，直接跳转至step3.html开始调身体参数捏人
#     if 'logged_in' in session:
#         return redirect(url_for('complete_step3'))
#
#     if request.method == 'GET':
#         # load model name
#         model_name = request.cookies.get('model_name')
#
#         # define basic model
#         age = request.cookies.get('age')
#         gender = request.cookies.get('gender')
#         # basic_model = model.define_basic_model(int(age), gender)
#
#         # insert data to database
#         basic_model = model.define_basic_model(age, gender)
#         return render_template('test.html', basic_model=basic_model)
#     elif request.method == 'POST':
#         # 如果未登录 -- 未完成注册系统都不识别为登录成功
#         if 'logged_in' not in session or not session['logged_in']:
#             session['logged_in'] = True
#             # # load model name
#             model_name = request.cookies.get('model_name')
#
#             #
#             # # define basic model
#             age = request.cookies.get('age')
#             gender = request.cookies.get('gender')
#             basic_model = model.define_basic_model(age, gender)
#             # # insert data to database
#             model.add_a_basic_human_model(model_name, age, gender)
#             # basic_model = model.define_basic_model(int(age), gender)
#
#             hair_color = request.form.get('hair_colour')  # 头发颜色
#             skin_color = request.form.get('skin_colour')  # 皮肤颜色
#             top_dress = request.form.get('top')  # 上衣
#             bottom_dress = request.form.get('bot')  # 下装
#
#             # hair_color = model.split_mesh_name(hair_color)
#             # skin_color = model.split_mesh_name(skin_color)
#             # top_dress = model.split_mesh_name(top_dress)
#             # bottom_dress = model.split_mesh_name(bottom_dress)
#
#             model.add_model_appearance(model_name, hair_color, skin_color, top_dress, bottom_dress, basic_model)
#
#             # 暂时没用
#             # textures_file_path = model.search_model_texture_file_path(model_name)
#             # basic_model_file_path = model.search_basic_model_file_path(model_name)
#             return redirect(url_for('complete_test'))
#         else:
#             return redirect(url_for('complete_test'))

