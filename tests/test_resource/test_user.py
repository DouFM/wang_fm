#!/usr/bin/env python
# encoding: utf-8
import json
from model.user import add_user, get_user, check_user_password
from model.music import add_music
from utils import BaseResourceTest


class test_user_list_resource(BaseResourceTest):
    def test_get(self):
        self.login_as_admin()   # this will add a user name admin!
        user = add_user('name1', 'pw1', 'normal')
        add_user('name2', 'pw2', 'normal')
        add_user('name3', 'pw3', 'normal')
        add_user('name4', 'pw4', 'normal')
        rv = self.app.get('/api/user/?key=' + user.key)
        # print json.loads(rv.data)
        assert len(json.loads(rv.data)) == 1
        rv = self.app.get('/api/user/')
        assert json.loads(rv.data)['count'] == 4 + 1
        rv = self.app.get('/api/user/?name=name1')
        assert len(json.loads(rv.data)) == 1
        rv = self.app.get('/api/user/?start=0&end=2')
        assert len(json.loads(rv.data)) == 2
        rv = self.app.get('/api/user/?start=0')
        assert len(json.loads(rv.data)) == 4 + 1

    def test_post(self):
        self.app.post('/api/user/',
                      data={'name': 'name1',
                            'password': 'pw1'})
        self.login_as_admin()
        rv = self.app.get('/api/user/?name=name1')
        rv = json.loads(rv.data)[0]
        #print rv
        assert rv['name'] == 'name1'
        assert rv['level'] == 'normal'

        rv = self.app.post('/api/user/',
                           data={'name': 'name1',
                                 'password': 'pw1'})
        rv = json.loads(rv.data)
        assert rv is None


class test_user_resource(BaseResourceTest):
    def test_patch(self):
        self.login_as_admin()   # this will add a user name admin!
        user = add_user('name1', 'pw1', 'normal')
        user_key = user.key
        rv = self.app.patch('/api/user/%s/' % (user_key),
                            data={'password': 'new_password',
                                  'level': 'admin'})
        rv = json.loads(rv.data)
        assert rv['level'] == 'admin'
        user = get_user(key=user_key)[0]
        assert check_user_password(user, 'new_password')

    def test_delete(self):
        self.login_as_admin()   # this will add a user name admin!
        user = add_user('name1', 'pw1', 'normal')
        user_key = user.key
        assert len(get_user(key=user_key)) == 1
        self.app.delete('/api/user/%s/' % (user_key))
        assert len(get_user(key=user_key)) == 0


class test_user_current_resource(BaseResourceTest):
    def test_get(self):
        rv = self.app.get('/api/user/current/')
        rv = json.loads(rv.data)
        assert rv is None

        add_user('name1', 'pw1', 'normal')
        rv = self.app.post('/api/user/current/',
                           data={'name': 'name1',
                                 'password': 'pw1'})
        rv = self.app.get('/api/user/current/')
        rv = json.loads(rv.data)
        assert rv['name'] == 'name1'
        assert rv['level'] == 'normal'

    def test_post(self):
        add_user('name1', 'pw1', 'normal')
        add_user('name2', 'pw2', 'disable')

        rv = self.app.post('/api/user/current/',
                           data={'name': 'name1',
                                 'password': 'pw1'})
        rv = json.loads(rv.data)
        assert rv['name'] == 'name1'
        assert rv['level'] == 'normal'

        rv = self.app.post('/api/user/current/',
                           data={'name': 'name1',
                                 'password': 'unknown'})
        rv = json.loads(rv.data)
        assert rv is None

        rv = self.app.post('/api/user/current/',
                           data={'name': 'name2',
                                 'password': 'pw2'})
        rv = json.loads(rv.data)
        assert rv is None

    def test_delete(self):
        add_user('name1', 'pw1', 'normal')
        rv = self.app.post('/api/user/current/',
                           data={'name': 'name1',
                                 'password': 'pw1'})
        rv = self.app.delete('/api/user/current/')
        rv = self.app.get('/api/user/current/')
        rv = json.loads(rv.data)
        assert rv is None


class test_user_current_history_resource(BaseResourceTest):
    def test_get(self):
        self.login_as_admin()   # this will add a user name admin!
        rv = self.app.get('/api/user/current/history/?start=0&end=10')
        rv = json.loads(rv.data)
        assert rv == []

    def test_post(self):
        self.login_as_admin()   # this will add a user name admin!
        music1 = add_music('title', 'artist', 'album', 'company',
                           '2013', '64', self.cover, self.audio, 'uuid1')
        self.cover.seek(0)
        self.audio.seek(0)
        music2 = add_music('title', 'artist', 'album', 'company',
                           '2013', '64', self.cover, self.audio, 'uuid2')
        self.app.post('/api/user/current/history/',
                      data={'op': 'favor', 'key': music1.key})
        self.app.post('/api/user/current/history/',
                      data={'op': 'dislike', 'key': music2.key})
        rv = self.app.get('/api/user/current/history/?start=0&end=10')
        rv = json.loads(rv.data)
        assert len(rv) == 2


class test_user_current_favor_resource(BaseResourceTest):
    def test_get(self):
        self.login_as_admin()   # this will add a user name admin!
        music1 = add_music('title', 'artist', 'album', 'company',
                           '2013', '64', self.cover, self.audio, 'uuid1')
        self.cover.seek(0)
        self.audio.seek(0)
        music2 = add_music('title', 'artist', 'album', 'company',
                           '2013', '64', self.cover, self.audio, 'uuid2')
        self.app.post('/api/user/current/history/',
                      data={'op': 'favor', 'key': music1.key})
        self.app.post('/api/user/current/history/',
                      data={'op': 'favor', 'key': music2.key})
        rv = self.app.get('/api/user/current/favor/?start=0&end=10')
        rv = json.loads(rv.data)
        # print rv
        assert len(rv) == 2
