#!/usr/bin/env python
# encoding: utf-8
import json

from database.channel.channel_model import add_channel, update_channel
from database.music.music_model import add_music
from utility.utils import BaseResourceTest


class test_playlist_list_resource(BaseResourceTest):
    def test_get(self):
        channel = add_channel('name1', 'uuid1')
        update_channel(channel, playable=True)
        channel = add_channel('name2', 'uuid2')
        update_channel(channel, playable=True)
        channel = add_channel('name3', 'uuid3')
        channel = add_channel('name4', 'uuid4')
        rv = self.app.get('/api/playlist/')
        assert len(json.loads(rv.data)) == 2


class test_playlist_resource(BaseResourceTest):
    def test_get(self):
        self.login_as_admin()
        channel = add_channel('name1', 'uuid1')
        update_channel(channel, playable=True)

        title = 'music_title'
        artist = 'music_artist'
        album = 'music_album'
        company = 'music_company'
        public_time = '2013'
        kbps = '64'
        uuid = 'douban-uuid'
        new_music_list = []
        for i in range(20):
            self.cover.seek(0)
            self.audio.seek(0)
            music = add_music(title, artist, album, company, public_time,
                              kbps, self.cover, self.audio, uuid + str(i))
            new_music_list.append(music.key)
        update_channel(channel, music_list=new_music_list)
        rv = self.app.get('/api/playlist/%s/?num=10' % (channel.key))
        rv = json.loads(rv.data)
        assert len(rv) == 10

        rv = self.app.get('/api/playlist/%s/?num=50' % (channel.key))
        rv = json.loads(rv.data)
        assert len(rv) == 20
