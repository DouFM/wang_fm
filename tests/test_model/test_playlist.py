#!/usr/bin/env python
# encoding: utf-8
from database.playlist.playlist import get_music_by_channel
from database.channel.channel_model import add_channel, update_channel, get_channel
from database.music.music_model import add_music
from utility.utils import BaseTest


class test_playlist_model(BaseTest):
    def test_get_music_by_channel(self):
        name = 'channel_name'
        uuid = 'douban-cid'
        channel = add_channel(name, uuid)
        assert len(get_music_by_channel(channel, 20)) == 0

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
        channel = get_channel(key=channel.key)[0]
        assert len(get_music_by_channel(channel, 30)) == 20
        assert len(get_music_by_channel(channel, 20)) == 20
        assert len(get_music_by_channel(channel, 10)) == 10
