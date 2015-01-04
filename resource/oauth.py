#!/usr/bin/env python
# encoding: utf-8
import requests
import json
import hashlib
from flask import session
from flask import redirect
from flask.ext.restful import Resource, fields, marshal
from config.config import APP_ID
from config.config import APP_SECRET
from config.config import GET_REQUEST_URL
from config.config import GET_ACCESS_URL
from config.config import AUTHORIZE_URL
from config.config import REDIRECT_URL
from config.config import GET_LOGIN_USER_ID_URL
from database.oauth import oauth_model
from database.user import user_model
from database.user import login_user_model
from base import login_check

oauth_request_fields = {
    'status': fields.String,
    'authorize_url': fields.String,
}

oauth_access_fields = {
    'status': fields.String,
    'user_recognition': fields.String,
    'user_id': fields.String,
    'user_name': fields.String,
}


class OAuthRequest(Resource):
    @staticmethod
    def get_request():
        request_url = GET_REQUEST_URL % (APP_ID, APP_SECRET)
        r = requests.get(request_url)
        if r.status_code != requests.codes.ok:
            return None
        result = json.loads(r.text)
        if result['status'] != 'success' or result['app_id'] != APP_ID:
            return None
        return result['request_token'].encode('utf-8')

    @staticmethod
    def generate_user_recognition(request_token):
        return hashlib.md5(request_token).hexdigest().upper()

    def get(self):
        if login_check(session):
            return marshal({'status': 'user already login', 'authorize_url': None}, oauth_request_fields)
        request_token = OAuthRequest.get_request()
        if not request_token:
            return marshal({'status': 'can not get request_token', 'authorize_url': None}, oauth_request_fields)
        user_recognition = OAuthRequest.generate_user_recognition(request_token)

        if not oauth_model.add_oauth(request_token=request_token, user_recognition=user_recognition):
            return marshal({'status': 'store request token fail', 'authorize_url': None}, oauth_request_fields)

        session['user_recognition'] = user_recognition
        authorize_url = AUTHORIZE_URL % (request_token, REDIRECT_URL)
        return marshal({'status': 'success', 'authorize_url': authorize_url}, oauth_request_fields)


class OAuthAccess(Resource):
    def get(self, request_token):
        oauth_info = oauth_model.get_oauth(request_token=request_token)[0]
        #get access token
        access_url = GET_ACCESS_URL % (request_token, APP_ID, APP_SECRET)
        r = requests.get(access_url)
        if r.status_code != requests.codes.ok:
            return marshal({'status': 'can not get access token'}, oauth_access_fields)
        result = json.loads(r.text)
        if result['status'] != 'success' or result['app_id'] != APP_ID:
            return marshal({'status': 'can not get access token'}, oauth_access_fields)
        access_token = result['access_token']

        #get login user id
        login_user_id_url = GET_LOGIN_USER_ID_URL % (access_token, APP_ID, APP_SECRET)
        r = requests.get(login_user_id_url)
        if r.status_code != requests.codes.ok:
            return marshal({'status': 'can not get login user id'}, oauth_access_fields)
        result = json.loads(r.text)
        if result['status'] != 'success':
            return marshal({'status': 'can not get login user id'}, oauth_access_fields)

        #update session
        session['login_user'] = result['user_id']
        #self.set_cookie('remember_login_user', oauth_info.user_recognition)

        #update user table
        if not user_model.get_user(user_id=result['user_id']):
            user_model.add_user(result['user_id'])

        #update login_user table
        login_user = login_user_model.get_login_user(user_id=result['user_id'])
        if login_user:
            login_user_model.delete_login_user(login_user[0])

        cookie_key=oauth_info.user_recognition
        login_user_model.add_login_user(user_id=result['user_id'], user_name=result['user_name'], cookie_key=cookie_key)

        #check oauth table to delete useless information
        oauth_model.delete_oauth(oauth_info)
        oauth_model.delete_expire_oauth()

        return redirect('/')
