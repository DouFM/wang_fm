#!/usr/bin/env python
# encoding: utf-8
import requests
import json
import hashlib
from flask import session
from flask.ext.restful import Resource, fields, marshal
from database.user import user_model
from database.user import login_user_model
from base import BaseArgs
from base import login_check
from config.config import APP_AUTH_URL

class AppAuthArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('user_name', type=unicode)
        self.parser.add_argument('password', type=unicode)


app_auth_fields = {
    'status': fields.String,
    'user_id': fields.String,
    'user_name': fields.String,
}


class AppAuthRequest(Resource):
    def post(self):
        #import pdb; pdb.set_trace()
        if login_check(session):
            return marshal({'status':'already login', 'user_id':None}, app_auth_fields)

        args = AppAuthArgs().args
        args['user_name'] = args['user_name'].encode('utf-8')
        args['password'] = args['password'].encode('utf-8')
        request_url = APP_AUTH_URL % (args['user_name'], args['password'])
        r = requests.get(request_url)
        if r.status_code != requests.codes.ok:
            return marshal({'status':'can not get rs response', 'user_id':None, 'user_name':None}, app_auth_fields)
        result = json.loads(r.text)
        if result['status'] != 'ok':
            return marshal({'status':result['status'], 'user_id':None, 'user_name':None}, app_auth_fields)

        session['login_user'] = result['user_id']
        #update user table
        if not user_model.get_user(user_id=result['user_id']):
            user_model.add_user(result['user_id'])

        #update login_user table
        login_user = login_user_model.get_login_user(user_id=result['user_id'])
        if login_user:
            login_user_model.delete_login_user(login_user[0])
        cookie_key = hashlib.md5(result['user_id']).hexdigest().lower()
        login_user_model.add_login_user(user_id=result['user_id'], cookie_key=cookie_key, user_name=result['user_name'])

        return marshal({'status':'success', 'user_id':result['user_id'], 'user_name': result['user_name']}, app_auth_fields)
