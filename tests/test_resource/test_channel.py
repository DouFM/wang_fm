#!/usr/bin/env python
# encoding: utf-8
import json
from model.channel import add_channel, get_channel
from utils import BaseResourceTest


class test_channel_list_resource(BaseResourceTest):
    def test_get(self):
        channel1 = add_channel('name1', 'uuid1')
        add_channel('name2', 'uuid2')
        add_channel('name3', 'uuid3')
        add_channel('name4', 'uuid4')
        rv = self.app.get('/api/channel/?key=' + channel1.key)
        # print json.loads(rv.data)
        assert len(json.loads(rv.data)) == 1
        rv = self.app.get('/api/channel/')
        assert json.loads(rv.data)['count'] == 4
        rv = self.app.get('/api/channel/?name=name1')
        assert len(json.loads(rv.data)) == 1
        rv = self.app.get('/api/channel/?start=0&end=2')
        assert len(json.loads(rv.data)) == 2
        rv = self.app.get('/api/channel/?start=0')
        assert len(json.loads(rv.data)) == 4


class test_channel_resource(BaseResourceTest):
    def test_patch(self):
        self.login_as_admin()
        channel = add_channel('name1', 'uuid1')
        channel_key = channel.key
        rv = self.app.patch('/api/channel/%s/' % (channel_key),
                data={'name': 'new_name',
                    'update_num': 10,
                    'playable': True})
        rv = json.loads(rv.data)
        assert rv['name'] == 'new_name'
        assert rv['update_num'] == 10
        assert rv['playable'] is True

    def test_delete(self):
        self.login_as_admin()
        channel = add_channel('name1', 'uuid1')
        channel_key = channel.key
        assert len(get_channel(key=channel_key)) == 1
        self.app.delete('/api/channel/%s/' % (channel_key))
        assert len(get_channel(key=channel_key)) == 0
