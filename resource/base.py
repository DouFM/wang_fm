#!/usr/bin/env python
#coding:utf8
from flask.ext.restful import reqparse
from flask.ext.restful import fields


class FileField(fields.Raw):
    def format(self, value):
        return "/api/fs/%s/" % (value._id)


class BoolField(fields.Raw):
    def format(self, value):
        return value


class LengthField(fields.Raw):
    def format(self, value):
        return len(value)


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
