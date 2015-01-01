#!/usr/bin/env python
# encoding: utf-8
from flask.ext.restful import Resource, fields, marshal_with, marshal

from .base import BaseArgs, LengthField, ChannelKey
from database.channel.channel_model import get_channel_status, get_channel, update_channel, delete_channel


class ChannelQueryArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('start', type=int)
        self.parser.add_argument('end', type=int)
        self.parser.add_argument('key', type=ChannelKey)
        self.parser.add_argument('name', type=unicode)
        self.parser.add_argument('playable', type=bool)


"""
class ChannelPatchArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('name', type=unicode)
        self.parser.add_argument('update_num', type=int)
        self.parser.add_argument('playable', type=bool)
"""

channel_status_fields = {
    'count': fields.Integer
}

channel_fields = {
    'key': fields.String,
    'name': fields.String,
    'music_list': LengthField,
    'upload_date': fields.DateTime,
    'update_num': fields.Integer,
    'playable': fields.Raw,
}


class ChannelQueryResource(Resource):
    def get(self):
        args = ChannelQueryArgs().args
        if not args:
            return marshal(get_channel_status(), channel_status_fields)
        ret_channels = get_channel(**args)
        return marshal(ret_channels, channel_fields)


"""
class ChannelResource(Resource):
    @authenticated('admin')
    @marshal_with(channel_fields)
    def patch(self, key):
        args = ChannelPatchArgs().args
        channel = get_channel(key=key)[0]
        update_channel(channel, **args)
        channel = get_channel(key=key)[0]
        return channel

    @authenticated('admin')
    def delete(self, key):
        channel = get_channel(key=key)[0]
        delete_channel(channel)
"""
