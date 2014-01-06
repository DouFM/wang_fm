#!/usr/bin/env python
#coding:utf8
import mongoengine
from .base import BaseMongoStorage
from config import DB_HOST, DB_PORT, DB_NAME


mongoengine.connect(DB_NAME, host=DB_HOST, port=DB_PORT)


class UserStorage(BaseMongoStorage, mongoengine.Document):
    """store music info
    key             str
    name            str
    password        str
    level           str in ('disable', 'normal', 'admin')
    regist_date     datetime

    history         list : [[date, op, key], [date, op, key], ...]
    favor           list : [key, key, ...]
    dislike         list : [key, key, ...]
    listened        int
    """
    name = mongoengine.StringField(max_length=256, unique=True, required=True)
    password = mongoengine.StringField(max_length=40, required=True)
    level = mongoengine.StringField(max_length=20, default='normal')
    regist_date = mongoengine.DateTimeField()

    history = mongoengine.ListField()
    favor = mongoengine.ListField(mongoengine.StringField(max_length=24))
    dislike = mongoengine.ListField(mongoengine.StringField(max_length=24))
    listened = mongoengine.IntField(default=0)

    meta = {
        'ordering': ['-regist_date']
    }

    def __str__(self):
        return 'name=%s, level=%s' % (self.name, self.level)
