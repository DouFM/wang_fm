#!/usr/bin/env python
# encoding: utf-8
from flask.ext.restful import Resource, fields, marshal
from .base import BaseArgs, LengthField, FileField
from model.playlist import get_music_by_channel
from model.channel import get_channel


class PlaylistQueryArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('num', type=int)


playlist_fields = {
    'key': fields.String,
    'name': fields.String,
    'music_list': LengthField,
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


class PlaylistListResource(Resource):
    def get(self):
        ret_channels = get_channel(playable=True)
        return marshal(ret_channels, playlist_fields)


class PlaylistResource(Resource):
    def get(self, key):
        args = PlaylistQueryArgs().args
        num = args['num']
        channel = get_channel(key=key)[0]
        return marshal(get_music_by_channel(channel, num), music_fields)
