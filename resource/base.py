#!/usr/bin/env python
#coding:utf8
from flask.ext.restful import reqparse
from flask.ext.restful import fields
from model.music import get_music
from model.user import get_user
from model.channel import get_channel


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
        '''clean the argv without value'''
        ret = super(RequestParser, self).parse_args(req)
        new_ret = {key: val for key, val in ret.iteritems() if val is not None}
        return new_ret


class BaseArgs(object):
    '''base args class, subclass should implete rules.
    use self.args to get args in request'''

    def __init__(self):
        self.parser = RequestParser()
        self.rules()
        self.args = self.parser.parse_args()

    def rules(self):
        '''use add_argument to add rule here'''
        raise NotImplementedError
