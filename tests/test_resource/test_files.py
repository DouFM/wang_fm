#!/usr/bin/env python
# encoding: utf-8
import mongoengine.fields
from utils import BaseResourceTest


class test_file_resource(BaseResourceTest):
    def test_get(self):
        fs = mongoengine.fields.GridFSProxy()
        fs.put(self.cover)
        key = fs._id
        rv = self.app.get('/api/fs/%s/' % key)
        self.cover.seek(0)
        # rv_cover = rv.data
        # self_cover = self.cover.read()
        # print type(rv_cover), rv_cover
        # print type(self_cover), self_cover
        assert rv.data == self.cover.read()

        # try again
        rv = self.app.get('/api/fs/%s/' % key)
        self.cover.seek(0)
        assert rv.data == self.cover.read()
        fs.delete()
