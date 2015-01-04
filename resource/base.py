#!/usr/bin/env python
#coding:utf8
from flask.ext.restful import reqparse
from flask.ext.restful import fields

from database.music.music_model import get_music
from database.user.user_model import get_user
from database.channel.channel_model import get_channel
from database.user.login_user_model import check_login_user, update_login_user_date
from config.config import ADMIN_PASSWORD


class FileField(fields.Raw):
    def format(self, value):
        return "/api/fs/%s/" % (value._id)


class LengthField(fields.Raw):
    def format(self, value):
        return len(value)


def MusicKey(key):
    try:
        assert get_music(key=key)[0]
    except:
        raise ValueError("Invalid Music Key")
    return key


def UserKey(key):
    try:
        assert get_user(key=key)[0]
    except:
        raise ValueError("Invalid User Key")
    return key


def ChannelKey(key):
    try:
        assert get_channel(key=key)[0]
    except:
        raise ValueError("Invalid Channel Key")
    return key


def PlaylistKey(key):
    try:
        assert get_channel(key=key)[0]
    except:
        raise ValueError("Invalid Playlist Key")
    return key


class RequestParser(reqparse.RequestParser):
    def parse_args(self, req=None):
        """clean the argv without value"""
        ret = super(RequestParser, self).parse_args(req)
        new_ret = {key: val for key, val in ret.iteritems() if val is not None}
        return new_ret


class BaseArgs(object):
    """base args class, subclass should implete rules.
    use self.args to get args in request"""

    def __init__(self):
        self.parser = RequestParser()
        self.rules()
        self.args = self.parser.parse_args()

    def rules(self):
        """use add_argument to add rule here"""
        raise NotImplementedError


def login_check(session):
    if 'login_user' in session and check_login_user(user_id=session['login_user']):
        return True
    return False


def update_login_user_table(user_id):
    update_login_user_date(user_id=user_id)


"""
def administrator_check(session):
    if 'administrator' in session and session['administrator'] == ADMIN_NAME:
        return True
    return False
    """