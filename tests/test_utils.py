#!/usr/bin/env python
#coding:utf8
import json

from flask.ext.restful import Api, Resource

from utility.utils import BaseTest, BaseResourceTest, authenticated
from database.user.user_model import add_user


class test_base_test(BaseTest):
    def test_demo(self):
        pass


class test_base_resource_test(BaseResourceTest):
    def test_demo(self):
        pass


class AuthResource(Resource):
    @authenticated('normal', 'admin')
    def get(self):
        return True

    @authenticated('admin')
    def post(self):
        return True

    def delete(self):
        return True


class test_auth(BaseResourceTest):
    def setup(self):
        super(test_auth, self).setup()
        import fm

        fm.app.config['TESTING'] = False

    def test_authenticated(self):
        add_user('name1', 'pw1', 'normal')
        add_user('name2', 'pw2', 'disable')
        import fm

        self.api = Api(fm.app)
        self.api.add_resource(AuthResource, '/test/api/auth/')

        rv = self.app.get('/test/api/auth/')
        rv = json.loads(rv.data)
        assert rv['status'] == 403
        rv = self.app.post('/api/user/current/',
                           data={'name': 'name1',
                                 'password': 'pw1'})
        rv = self.app.get('/test/api/auth/')
        rv = json.loads(rv.data)
        assert rv is True
        rv = self.app.post('/test/api/auth/')
        rv = json.loads(rv.data)
        assert rv['status'] == 403

        rv = self.app.delete('/api/user/current/')
        rv = self.app.post('/api/user/current/',
                           data={'name': 'name2',
                                 'password': 'pw2'})
        rv = self.app.get('/test/api/auth/')
        rv = json.loads(rv.data)
        assert rv['status'] == 403
