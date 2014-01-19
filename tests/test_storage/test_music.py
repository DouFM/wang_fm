#!/usr/bin/env python
# encoding: utf-8
import datetime
from storage.music import MusicStorage
from utils import BaseTest


class test_music_storage(BaseTest):
    def test_simple(self):
        assert len(MusicStorage.get()) == 0
        music = MusicStorage()
        music.title = 'demo_title'
        music.artist = 'demo_artist'
        music.album = 'demo_album'
        music.company = 'demo_company'
        music.public_time = '2013'
        music.kbps = '64'
        music.cover = self.cover.read()
        music.audio = self.audio.read()
        now = datetime.datetime(2013, 12, 24, 10, 8, 0)
        music.upload_date = now
        music.uuid = 'douban-sid-aid'
        music.save()
        assert type(music.key) == str
        key = music.key
        assert len(MusicStorage.get()) == 1
        assert len(MusicStorage.get(title='demo_title')) == 1
        assert len(MusicStorage.get(title='demo_title', album='demo_album')) == 1
        assert len(MusicStorage.get(title='unkown')) == 0
        music = MusicStorage.get()[0]
        assert music.key == key
        assert music.title == 'demo_title'
        assert music.artist == 'demo_artist'
        assert music.album == 'demo_album'
        assert music.company == 'demo_company'
        assert music.public_time == '2013'
        assert music.kbps == '64'
        self.cover.seek(0)
        self.audio.seek(0)
        assert music.cover.read() == self.cover.read()
        assert music.audio.read() == self.audio.read()
        assert music.upload_date == now
        assert music.uuid == 'douban-sid-aid'
        music.delete()
        assert len(MusicStorage.get()) == 0

    def test_update(self):
        assert len(MusicStorage.get()) == 0
        music = MusicStorage()
        music.title = 'demo_title'
        music.artist = 'demo_artist'
        music.album = 'demo_album'
        music.company = 'demo_company'
        music.public_time = '2013'
        music.kbps = '64'
        # exchange cover & audio
        music.cover = self.cover.read()
        music.audio = self.audio.read()
        now = datetime.datetime(2013, 12, 24, 10, 8, 0)
        music.upload_date = now
        music.uuid = 'douban-sid-aid'
        music.save()
        self.cover.seek(0)
        self.audio.seek(0)
        music.update(title='new_title', artist='new_artist', album='new_album',
                     company='new_company', public_time='2014', kbps='128',
                     cover=self.audio, audio=self.cover, uuid='new_douban-uuid')
        music = MusicStorage.get()[0]
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
