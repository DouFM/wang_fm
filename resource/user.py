#!/usr/bin/env python
# encoding: utf-8
from flask import session
from flask.ext.restful import fields, marshal, Resource

from base import BaseArgs, LengthField, MusicKey
from base import login_check, update_login_user_table
from database.user.login_user_model import delete_login_user, get_login_user
from music import music_fields
from database.user.user_model import *
from log.login import login_log


class UserMusicQueryArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('type', type=str, choices=('favor', 'dislike', 'shared', 'listened'))
        self.parser.add_argument('start', type=int)
        self.parser.add_argument('end', type=int)


class UserHistoryGetArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('start', type=int)
        self.parser.add_argument('end', type=int)


class UserHistoryPostArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('op', type=str, choices=('favor', 'dislike', 'shared', 'listened'))
        self.parser.add_argument('key', type=MusicKey)


user_status_fields = {
    'count': fields.Integer
}

status_fields = {
    'status': fields.String
}

user_fields = {
    'favor': LengthField,
    'share': LengthField,
    'dislike': LengthField,
    'listened': LengthField
}

history_fields = {
    'date': fields.DateTime,
    'op': fields.String,
    'key': fields.String,
    'title': fields.String,
    'audio': fields.String,
    'cover': fields.String,
}


class UserLogoutResource(Resource):

    def get(self):
        ret = {}
        if not login_check(session):
            ret['status'] = 'have not login'
        else:
            info = 'user %s logout', session['login_user']
            login_log.log_info(info)
            user = get_login_user(user_id=session['login_user'])[0]
            delete_login_user(user)
            session.pop('login_user', None)
            ret['status'] = 'success'
        return marshal(ret, status_fields)


class UserProfileResource(Resource):
    def get(self):
        if not login_check(session):
            return None
        user = get_user(user_id=session['login_user'])[0]
        return marshal(user, user_fields)


class UserHistoryResource(Resource):

    def get(self):
        args = UserHistoryGetArgs().args
        if not login_check(session):
            return None
        user = get_user(user_id=session['login_user'])[0]
        history = get_user_history(user, args['start'], args['end'])
        return marshal(history, history_fields)

    def post(self):
        args = UserHistoryPostArgs().args
        if not login_check(session):
            return None
        user = get_user(user_id=session['login_user'])[0]
        add_user_history(user, args['op'], args['key'])
        update_login_user_table(session['login_user'])
        return marshal({'status':args['op'] + '_success'}, status_fields)


class UserMusicResource(Resource):

    def get(self):
        args = UserMusicQueryArgs().args
        if not login_check(session):
            return None
        user = get_user(user_id=session['login_user'])[0]
        music_list = get_user_music_list(user, args['type'], args['start'], args['end'])
        update_login_user_table(session['login_user'])
        return marshal(music_list, music_fields)
