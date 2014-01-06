#!/usr/bin/env python
# encoding: utf-8
from flask import Response
from flask.ext.restful import Resource
import mongoengine.fields
from bson.objectid import ObjectId


class FileResource(Resource):
    def get(self, key):
        # TODO
        # maybe fs should be global
        fs = mongoengine.fields.GridFSProxy()
        file = fs.get(ObjectId(key)).read()
        return Response(file, mimetype='application/octet-stream')
