#!/usr/bin/env python
# encoding: utf-8
from flask import session
from flask.ext.restful import Resource, fields, marshal_with, marshal
from .base import BaseArgs, LengthField, FileField
from model.user import get_user_status, get_user, add_user, update_user, delete_user, check_user_password, check_user_enable, get_user_history, add_user_history, get_user_favor
from utils import authenticated


class UserQueryArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('start', type=int)
        self.parser.add_argument('end', type=int)
        self.parser.add_argument('key', type=str)
        self.parser.add_argument('name', type=unicode)
        self.parser.add_argument('level', type=str, choices=('disable', 'nromal', 'admin'))


class UserRegArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('name', type=unicode)
        self.parser.add_argument('password', type=str)


class UserPatchArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('password', type=str)
        self.parser.add_argument('level', type=str, choices=('disable', 'nromal', 'admin'))


class UserLoginArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('name', type=unicode)
        self.parser.add_argument('password', type=str)


class UserHistoryQueryArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('start', type=int)
        self.parser.add_argument('end', type=int)


class UserHistoryPostArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('op', type=str, choices=('favor', 'dislike', 'shared', 'listened'))
        self.parser.add_argument('key', type=str)


user_status_fields = {
    'count': fields.Integer
}

user_fields = {
    'key': fields.String,
    'name': fields.String,
    'level': fields.String,
    'regist_date': fields.DateTime,
    'favor': LengthField,
    'dislike': LengthField,
    'listened': fields.Integer,
}

music_fields = {
    'key': fields.String,
    'title': fields.String,
    'artist': fields.String,
    'album': fields.String,
    'company': fields.String,
    'public_time': fields.String,
    'kbps': fields.String,
    'cover': FileField,
    'audio': FileField,
}

history_fields = {
    'date': fields.DateTime,
    'op': fields.String,
    'key': fields.String,
    'title': fields.String,
    'cover': FileField,
}


class UserListResource(Resource):
    @authenticated('admin')
    def get(self):
        args = UserQueryArgs().args
        if args == {}:
            return marshal(get_user_status(), user_status_fields)
        users = get_user(**args)
        return marshal(users, user_fields)

    def post(self):
        args = UserRegArgs().args
        user = add_user(args['name'], args['password'], 'normal')
        if user:
            return marshal(user, user_fields)
        return None


class UserResource(Resource):
    @authenticated('admin')
    @marshal_with(user_fields)
    def patch(self, key):
        args = UserPatchArgs().args
        user = get_user(key=key)[0]
        update_user(user, **args)
        user = get_user(key=key)[0]
        return user

    @authenticated('admin')
    def delete(self, key):
        user = get_user(key=key)[0]
        delete_user(user)


class UserCurrentResource(Resource):
    def get(self):
        try:
            user = get_user(key=session['user'])[0]
            return marshal(user, user_fields)
        except:
            return None

    def post(self):
        args = UserLoginArgs().args
        user = get_user(name=args['name'])[0]
        if check_user_password(user, args['password']) and check_user_enable(user):
            session['user'] = user.key
            return marshal(user, user_fields)
        return None

    def delete(self):
        session.pop('user', None)


class UserCurrentHistoryResource(Resource):
    @authenticated('normal', 'admin')
    def get(self):
        user = get_user(key=session['user'])[0]
        args = UserHistoryQueryArgs().args
        if 'start' not in args:
            args['start'] = None
        if 'end' not in args:
            args['end'] = None
        return marshal(get_user_history(user, args['start'], args['end']), history_fields)

    @authenticated('normal', 'admin')
    def post(self):
        user = get_user(key=session['user'])[0]
        args = UserHistoryPostArgs().args
        add_user_history(user, args['op'], args['key'])


class UserCurrentFavorResource(Resource):
    @authenticated('normal', 'admin')
    def get(self):
        user = get_user(key=session['user'])[0]
        args = UserHistoryQueryArgs().args  # use history query args
        if 'start' not in args:
            args['start'] = None
        if 'end' not in args:
            args['end'] = None
        return marshal(get_user_favor(user, args['start'], args['end']), music_fields)
