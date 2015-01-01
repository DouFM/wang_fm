#!/usr/bin/env python
# encoding: utf-8
import mongoengine
import mongoengine.errors

from database.music.music_model import add_music, get_music, update_music, delete_music, get_music_status
from utility.utils import BaseTest


class test_music_model(BaseTest):
    def test_add_music(self):
        title = 'music_title'
        artist = 'music_artist'
        album = 'music_album'
        company = 'music_company'
        public_time = '2013'
        kbps = '64'
        uuid = 'douban-uuid'
        music = add_music(title, artist, album, company,
                          public_time, kbps, self.cover, self.audio, uuid)
        try:
            add_music(title, artist, album, company,
                      public_time, kbps, self.cover, self.audio, uuid)
        except mongoengine.errors.NotUniqueError:
            pass
        assert len(get_music(key=music.key)) == 1
        music = get_music()[0]
        assert music.title == 'music_title'
        assert music.artist == 'music_artist'
        assert music.album == 'music_album'
        assert music.company == 'music_company'
        assert music.public_time == '2013'
        assert music.kbps == '64'
        self.cover.seek(0)
        self.audio.seek(0)
        assert music.cover.read() == self.cover.read()
        assert music.audio.read() == self.audio.read()
        assert music.uuid == 'douban-uuid'

    def test_update_music(self):
        title = 'music_title'
        artist = 'music_artist'
        album = 'music_album'
        company = 'music_company'
        public_time = '2013'
        kbps = '64'
        uuid = 'douban-uuid'
        music = add_music(title, artist, album, company,
                          public_time, kbps, self.cover, self.audio, uuid)
        self.cover.seek(0)
        self.audio.seek(0)
        music = get_music()[0]
        # exchange cover & audio
        update_music(music, title='new_title', artist='new_artist',
                     album='new_album', company='new_company', public_time='2014',
                     kbps='128', cover=self.audio, audio=self.cover, uuid='new_douban-uuid')
        music = get_music()[0]
        assert music.title == 'new_title'
        assert music.artist == 'new_artist'
        assert music.album == 'new_album'
        assert music.company == 'new_company'
        assert music.public_time == '2014'
        assert music.kbps == '128'
        self.cover.seek(0)
        self.audio.seek(0)
        assert music.cover.read() == self.audio.read()
        assert music.audio.read() == self.cover.read()
        assert music.uuid == 'new_douban-uuid'

    def test_delete_music(self):
        title = 'music_title'
        artist = 'music_artist'
        album = 'music_album'
        company = 'music_company'
        public_time = '2013'
        kbps = '64'
        uuid = 'douban-uuid'
        music = add_music(title, artist, album, company,
                          public_time, kbps, self.cover, self.audio, uuid)
        assert len(get_music()) == 1
        music = get_music()[0]
        delete_music(music)
        assert len(get_music()) == 0

    def test_get_music(self):
        title = 'music_title'
        artist = 'music_artist'
        album = 'music_album'
        company = 'music_company'
        public_time = '2013'
        kbps = '64'
        uuid = 'douban-uuid'
        for i in range(10):
            add_music(title, artist, album, company, public_time,
                      kbps, self.cover, self.audio, uuid + str(i))
        assert len(get_music(start=0, end=5)) == 5

    def test_get_status(self):
        title = 'music_title'
        artist = 'music_artist'
        album = 'music_album'
        company = 'music_company'
        public_time = '2013'
        kbps = '64'
        uuid = 'douban-uuid'
        for i in range(10):
            add_music(title, artist, album, company, public_time,
                      kbps, self.cover, self.audio, uuid + str(i))
        assert get_music_status()['count'] == 10
