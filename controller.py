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

                # Store the user details for us to use throughout
                # global human_model_details
                # human_model_details['model_name'] = model_name

                resp = make_response(redirect(url_for('complete_step3')))
                resp.set_cookie('model_name', model_name)
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
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('index'))


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
        model.add_a_basic_human_model(model_name, age, gender)
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
            basic_model = model.define_basic_model(age, gender)
            # # insert data to database
            # model.add_a_basic_human_model(model_name, age, gender)
            # basic_model = model.define_basic_model(int(age), gender)

            hair_color = request.form.get('hair_colour')  # 头发颜色
            skin_color = request.form.get('skin_colour')  # 皮肤颜色
            top_dress = request.form.get('top')  # 上衣
            bottom_dress = request.form.get('bot')  # 下装

            # hair_color = model.split_mesh_name(hair_color)
            # skin_color = model.split_mesh_name(skin_color)
            # top_dress = model.split_mesh_name(top_dress)
            # bottom_dress = model.split_mesh_name(bottom_dress)

            model.add_model_appearance(model_name, hair_color, skin_color, top_dress, bottom_dress, basic_model)

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
    # print("~"*20+session['logged_in']+"~"*20)
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    # flash("welcome " + human_model_details['model_name'], 'success')
    if request.method == 'GET':
        # print("~"*45)
        model_name = request.cookies.get('model_name')
        # print(model_name)
        model_texture = model.search_model_texture_file_path(model_name)
        return render_template('step3.html', model_texture=model_texture)
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
        upper_arm = request.form.get('upper_arm')  # 胳膊
        waist = request.form.get('waist')
        chest = request.form.get('chest')

        # print("{},{},{}".format(model_name,update_time,height))
        model.add_new_body_measurment_record(model_name, height, weight,
                                             thigh, shank, hip, upper_arm, waist, chest)
        # return render_template('step4.html')
        return redirect(url_for('complete_step4'))


@app.route('/step4', methods=['GET','POST'])
def complete_step4():
    """ Generate a health report """
    # 如果未登录
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    if request.method == 'GET':
        model_name = request.cookies.get('model_name')
        last_two_records = model.search_last_two_body_measurement_records(model_name)
        return render_template('step4.html')
