#!/usr/bin/env python
# encoding: utf-8
import json

from database.music.music_model import add_music, get_music
from utility.utils import BaseResourceTest


class test_music_list_resource(BaseResourceTest):
    def test_get(self):
        music1 = add_music('title1', 'artist1', 'album1', 'company1',
                           '2001', '64', self.cover, self.audio, 'uuid1')
        self.cover.seek(0)
        self.audio.seek(0)
        add_music('title2', 'artist2', 'album2', 'company2',
                  '2001', '128', self.cover, self.audio, 'uuid2')
        self.cover.seek(0)
        self.audio.seek(0)
        add_music('title3', 'artist3', 'album3', 'company3',
                  '2004', '64', self.cover, self.audio, 'uuid3')
        self.cover.seek(0)
        self.audio.seek(0)
        add_music('title4', 'artist4', 'album4', 'company4',
                  '2004', '128', self.cover, self.audio, 'uuid4')
        rv = self.app.get('/api/music/?key=' + music1.key)
        # print json.loads(rv.data)
        assert len(json.loads(rv.data)) == 1
        rv = self.app.get('/api/music/')
        assert json.loads(rv.data)['count'] == 4
        rv = self.app.get('/api/music/?title=title1')
        assert len(json.loads(rv.data)) == 1
        rv = self.app.get('/api/music/?kbps=64')
        assert len(json.loads(rv.data)) == 2
        rv = self.app.get('/api/music/?title=title1&kbps=64')
        assert len(json.loads(rv.data)) == 1
        rv = self.app.get('/api/music/?start=0&end=2')
        assert len(json.loads(rv.data)) == 2
        rv = self.app.get('/api/music/?start=0')
        assert len(json.loads(rv.data)) == 4

        # get cover and audio
        rv = self.app.get('/api/music/?start=0&end=1')
        music = json.loads(rv.data)[0]
        rv_cover = self.app.get(music['cover'])
        rv_audio = self.app.get(music['audio'])
        self.cover.seek(0)
        self.audio.seek(0)
        assert rv_cover.data == self.cover.read()
        assert rv_audio.data == self.audio.read()


class test_music_resource(BaseResourceTest):
    def test_patch(self):
        self.login_as_admin()
        music = add_music('title', 'artist', 'album', 'company',
                          '2001', '64', self.cover, self.audio, 'uuid')
        music_key = music.key
        rv = self.app.patch('/api/music/%s/' % (music_key),
                            data={'title': 'only_title'})
        rv_music = json.loads(rv.data)
        assert rv_music['title'] == 'only_title'

        rv = self.app.patch('/api/music/%s/' % (music_key),
                            data={'title': 'new_title', 'artist': 'new_artist',
                                  'album': 'new_album', 'company': 'new_company',
                                  'public_time': '2014', })
        rv_music = json.loads(rv.data)
        assert rv_music['title'] == 'new_title'
        assert rv_music['artist'] == 'new_artist'
        assert rv_music['album'] == 'new_album'
        assert rv_music['company'] == 'new_company'
        assert rv_music['public_time'] == '2014'

    def test_delete(self):
        self.login_as_admin()
        music = add_music('title', 'artist', 'album', 'company',
                          '2001', '64', self.cover, self.audio, 'uuid')
        music_key = music.key
        assert len(get_music(key=music_key)) == 1
        self.app.delete('/api/music/%s/' % (music_key))
        assert len(get_music(key=music_key)) == 0
