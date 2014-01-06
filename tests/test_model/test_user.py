#!/usr/bin/env python
# encoding: utf-8
import mongoengine
from model.user import add_user, get_user, update_user, delete_user, _encrypt, check_user_password, add_user_history, get_user_history
from model.music import add_music
from utils import BaseTest


class test_user_model(BaseTest):
    def test_add_user(self):
        name = 'user_name'
        password = 'user_password'
        level = 'normal'
        user = add_user(name, password, level)
        try:
            add_user(name, password, level)
        except mongoengine.errors.NotUniqueError:
            pass
        assert len(get_user(key=user.key)) == 1
        user = get_user()[0]
        assert user.name == 'user_name'
        assert user.password == _encrypt('user_name', 'user_password')
        assert check_user_password(user, 'user_password')
        assert user.level == 'normal'

    def test_update_user(self):
        name = 'user_name'
        password = 'user_password'
        level = 'normal'
        add_user(name, password, level)
        user = get_user()[0]
        update_user(user, password='new_password', level='disable')
        user = get_user()[0]
        assert user.name == 'user_name'
        assert user.password == _encrypt(user.name, 'new_password')
        assert check_user_password(user, 'new_password')
        assert user.level == 'disable'
        try:
            update_user(user, name='some_name')
        except AttributeError:
            pass
        try:
            update_user(user, level='some_level')
        except AssertionError:
            pass

    def test_delete_user(self):
        name = 'user_name'
        password = 'user_password'
        level = 'normal'
        user = add_user(name, password, level)
        assert len(get_user()) == 1
        user = get_user()[0]
        delete_user(user)
        assert len(get_user()) == 0

    def test_add_user_history(self):
        user = add_user('name1', 'pw1', 'normal')
        add_user_history(user, 'favor', 'f' * 24)
        user = get_user(key=user.key)[0]
        assert len(user.history) == 1
        assert len(user.favor) == 1

        add_user_history(user, 'dislike', 'f' * 24)
        user = get_user(key=user.key)[0]
        assert len(user.history) == 2
        assert len(user.favor) == 0
        assert len(user.dislike) == 1

        add_user_history(user, 'listened', 'f' * 24)
        user = get_user(key=user.key)[0]
        assert len(user.history) == 3
        assert user.listened == 1

    def test_get_user_history(self):
        # add user
        user = add_user('name1', 'pw1', 'normal')
        # add music
        music1 = add_music('title', 'artist', 'album', 'company',
                '2013', '64', self.cover, self.audio, 'uuid1')
        self.cover.seek(0)
        self.audio.seek(0)
        music2 = add_music('title', 'artist', 'album', 'company',
                '2013', '64', self.cover, self.audio, 'uuid2')
        add_user_history(user, 'favor', music1.key)
        add_user_history(user, 'dislike', music2.key)
        assert len(get_user_history(user, 0, 10)) == 2
