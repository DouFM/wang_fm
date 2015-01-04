#!/usr/bin/env python
# encoding: utf-8
from flask.ext.restful import Resource, fields, marshal

from .base import BaseArgs, LengthField, FileField
from resource.music import music_fields
from database.playlist.playlist import get_music_by_channel
from database.channel.channel_model import get_channel


class PlaylistQueryArgs(BaseArgs):
    def rules(self):
        self.parser.add_argument('num', type=int)


playlist_fields = {
    'key': fields.String,
    'name': fields.String,
    'music_list': LengthField,
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

