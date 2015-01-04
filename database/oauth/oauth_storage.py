#!/usr/bin/env python
#coding:utf8
import mongoengine
from database.base_storage import BaseMongoStorage
from config.config import DB_HOST, DB_PORT, DB_NAME


mongoengine.connect(DB_NAME, host=DB_HOST, port=DB_PORT)


class OAuthStorage(BaseMongoStorage, mongoengine.Document):
    """store user info
    access_token      str
    user_recognition  str
    date date
    """
    request_token = mongoengine.StringField(max_length=256, unique=True)
    user_recognition = mongoengine.StringField(max_length=256, unique=True)
    date = mongoengine.DateTimeField()

    def __str__(self):
        return u'user_recognition:%s' % self.user_recognition