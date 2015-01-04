#!/usr/bin/env python
# encoding: utf-8
from flask import Flask
from flask import request
from flask import session
from flask import make_response
import datetime
from resource import base
from flask.ext.restful import Api
from flask import render_template
from config import url_map
from config.config import SECRET_KEY
from config.config import PERMANENT_SESSION_LIFETIME
from config.config import SESSION_REFRESH_EACH_REQUEST
from database.user import login_user_model

app = Flask(__name__)
api = Api(app)

app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
#app.secret_key = SECRET_KEY
app.config.update(
    SECRET_KEY=SECRET_KEY,
    ERMANENT_SESSION_LIFETIME = PERMANENT_SESSION_LIFETIME,
    SESSION_REFRESH_EACH_REQUEST = SESSION_REFRESH_EACH_REQUEST,

)
url_map.set_url_map(api)

app.debug = True

@app.route('/')
def index():
    if base.login_check(session):
        user_id = session['login_user']
        login_user = login_user_model.get_login_user(user_id=user_id)[0]
        resp = make_response(render_template('index.html', login_flag=True, user_name=login_user.user_name))
        expire_time = datetime.datetime.now() + datetime.timedelta(seconds=60*60*24)
        resp.set_cookie('user_name', login_user.user_name, max_age=60*60*24, expires=expire_time)
        resp.set_cookie('user_id', login_user.user_id, max_age=60*60*24, expires=expire_time)
        resp.set_cookie('user_recognition', login_user.cookie_key, max_age=60*60*24, expires=expire_time)
        return resp
    else:
        login_flag = False
        user_recognition = request.cookies.get('user_recognition', None)
        user_id = request.cookies.get('user_id', None)
        user_name = request.cookies.get('user_name', None)
        if user_recognition and user_id and login_user_model.auto_login_by_cookie(user_id=user_id, cookie_key=user_recognition):
            session['login_user'] = user_id
            login_flag = True
        return render_template("index.html", login_flag=login_flag, user_name=user_name)
