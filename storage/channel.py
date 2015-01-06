#!/usr/bin/env python
# encoding: utf-8
import mongoengine
from .base import BaseMongoStorage
from config import DB_HOST, DB_PORT, DB_NAME


mongoengine.connect(DB_NAME, host=DB_HOST, port=DB_PORT)


class ChannelStorage(BaseMongoStorage, mongoengine.Document):
    """store music info
    key             str
    name            str
    music_list      list(key)
    upload_date     datetime
    uuid            str
    update_num      int
    playable        bool
    """
    name = mongoengine.StringField(max_length=256)
    music_list = mongoengine.ListField(mongoengine.StringField(max_length=24), default=[])
    upload_date = mongoengine.DateTimeField()

    uuid = mongoengine.StringField(unique=True)

    # the music num this channel will update pre day.
    update_num = mongoengine.IntField(default=0)
    playable = mongoengine.BooleanField(default=False)

    meta = {
        'ordering': ['upload_date']
    }

    def __str__(self):
        return 'name=%s, len(music_list)=%s' % (self.name, len(self.music_list))
