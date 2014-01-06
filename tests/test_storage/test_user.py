#!/usr/bin/env python
#coding:utf8
import datetime
from storage.user import UserStorage
from utils import BaseTest


class test_user_storage(BaseTest):
    def test_simple(self):
        assert len(UserStorage.get()) == 0
        user = UserStorage()
        user.name = 'demo_name'
        user.password = 'demo_password'
        user.level = 'demo_level'
        now = datetime.datetime(2013, 12, 24, 10, 8, 3)
        user.regist_date = now
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.now()
        user.history = [[d1, 'favor', 'h' * 24], [d2, 'dislike', 'd' * 24]]
        user.favor = ['f' * 24]
        user.dislike = ['d' * 24]
        user.listened = 10
        user.save()
        assert type(user.key) == str
        assert len(UserStorage.get()) == 1
        assert len(UserStorage.get(name='demo_name')) == 1
        assert len(UserStorage.get(name='demo_name', level='demo_level')) == 1
        assert len(UserStorage.get(name='unkown')) == 0
        user = UserStorage.get()[0]
        assert user.name == 'demo_name'
        assert user.password == 'demo_password'
        assert user.level == 'demo_level'
        assert len(user.history) == 2
        assert user.favor == ['f' * 24]
        assert user.dislike == ['d' * 24]
        assert user.listened == 10
        assert user.regist_date == now
        user.delete()
        assert len(UserStorage.get()) == 0
