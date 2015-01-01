#!/usr/bin/env python
#coding:utf8
import tempfile
import functools

import mongoengine
from mongoengine.connection import _get_db
from flask import session, abort

from database.user.user_model import get_user
from config.config import DB_HOST, DB_PORT, TEST_DB_NAME
from database.user.user_model import add_user


def get_current_user():
    try:
        return get_user(key=session['login_user'])[0]
    except:
        return None


def authenticated(*req):
    def actualDecorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = get_current_user()
            if not user:
                abort(403)
            user_level = user.level
            # print user,user_level,req
            if user_level not in req:
                abort(403)
            return method(self, *args, **kwargs)

        return wrapper

    return actualDecorator


class BaseTest(object):
    '''the base test class
    change default db to TEST_DB_NAME.
    clean db before test'''

    def setup(self):
        mongoengine.register_connection(mongoengine.DEFAULT_CONNECTION_NAME, TEST_DB_NAME, DB_HOST, DB_PORT)
        # TODO
        # this code is using pymongo
        # maybe mongoengine have the same code
        db = _get_db()
        for name in db.collection_names(False):
            db[name].remove()
        self.cover = tempfile.TemporaryFile()
        self.cover.write('cover')
        self.cover.seek(0)
        self.audio = tempfile.TemporaryFile()
        self.audio.write('audio')
        self.audio.seek(0)

    def teardown(self):
        self.cover.close()
        self.audio.close()


class BaseResourceTest(BaseTest):
    '''the base resource test
    handle app config'''

    def setup(self):
        super(BaseResourceTest, self).setup()
        import fm

        fm.app.config['TESTING'] = True
        self.app = fm.app.test_client()

    def login_as_admin(self):
        add_user('admin', 'admin', 'admin')
        self.app.post('/api/user/current/',
                      data={'name': 'admin',
                            'password': 'admin'})

    def logout(self):
        self.app.delete('/api/user/current/')

    def teardown(self):
        self.logout()
        super(BaseResourceTest, self).teardown()
