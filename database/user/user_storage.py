#!/usr/bin/env python
#coding:utf8
import mongoengine
from database.base_storage import BaseMongoStorage
from config.config import DB_HOST, DB_PORT, DB_NAME


mongoengine.connect(DB_NAME, host=DB_HOST, port=DB_PORT)


class UserStorage(BaseMongoStorage, mongoengine.Document):
    """store user info
    key             str
    user_id            str
    history         list : [[date, op, key], [date, op, key], ...]
    favor           list : [key, key, ...]
    dislike         list : [key, key, ...]
    share           list : [key, key, ...]
    """
    user_id = mongoengine.StringField(max_length=256, unique=True, required=True)
    history = mongoengine.ListField()
    favor = mongoengine.ListField(mongoengine.StringField(max_length=24))
    dislike = mongoengine.ListField(mongoengine.StringField(max_length=24))
    share = mongoengine.ListField(mongoengine.StringField(max_length=24))
    listened = mongoengine.ListField(mongoengine.StringField(max_length=24))
