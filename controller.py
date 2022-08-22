"""
Route management.

This provides all of the websites routes and handles what happens each
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

session = {}                        # Session information (logged in state)
human_model_details = {}            # Human model details kept for us, 比如model的name

app.config['SECRET_KEY'] = os.urandom(24)
model = Model()

@app.route('/')
def index():
    """
    If already login( 即之前已输入过model name ), go to step3
    Otherwise prompt login
     """

    # 如果未登录
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login_page'))

    # 如果已经登陆过，直接跳转至step3.html开始调身体参数捏人
    return render_template('step3.html',
                           session = session,
                           human_model_details = human_model_details)


#####################################################
#   LOGIN
#####################################################
@app.route('/login', methods=['GET','POST'])
def login_page():
    """ Here handles the login page
    Provides /login
        - [GET] If they are just viewing the page then render login page.
        - [POST] If submitting login details, check login.

    """

    if request.method == 'GET':
        return render_template('index.html')

    else:
        model_name = request.form.get('modelname') # 前端请用'modelname'

        # No credential check, log user in
        session['logged_in'] = True

        # Store the user details for us to use throughout
        global human_model_details
        human_model_details['model_name'] = model_name

        if model.check_model_already_exists(model_name):
            # 如果该模型已存在,跳转到step3.html
            return redirect(url_for('complete_step3'))

        else:
            # 如果该模型还未创建完成（name, age, gender都有），那么跳转到step1.html
            return redirect(url_for('complete_step1'))

#####################################################
#   LOGOUT
#####################################################
@app.route('/logout')
def logout():
    """
    Logs out of the current session
        - Removes any stored human model data.
    """
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/step1',methods=['GET','POST'])
def complete_step1():
    """ Handle the 1st step of the body visualizer """

    if request.method == 'GET':
        return render_template('step1.html')

    elif request.method == 'POST':
        # 获取性别年龄，入库
        age = request.form.get('age')
        gender = request.form.get('gender')
        model_name = human_model_details['model_name']
        model.add_a_basic_human_model(model_name,age,gender)
        return redirect(url_for('complete_step2'))

@app.route('/step2', methods=['GET','POST'])
def complete_step2():
    """ Handle the 3rd step of the body visualizer """

    if request.method == 'GET':
        return render_template('step2.html')

@app.route('/step3', methods=['GET','POST'])
def complete_step3():
    """ Handle the 3rd step of the body visualizer """

    if request.method == 'GET':
        return render_template('step3.html')
