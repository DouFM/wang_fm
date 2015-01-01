#!/usr/bin/env python
# encoding: utf-8
import mongoengine

from database.base_storage import BaseMongoStorage
from config.config import DB_HOST, DB_PORT, DB_NAME


mongoengine.connect(DB_NAME, host=DB_HOST, port=DB_PORT)


class MusicStorage(BaseMongoStorage, mongoengine.Document):
    """store music info
    key             str
    title           str
    artist          str
    album           str
    company         str
    public_time     str
    kbps            str
    cover           file
    audio           file
    upload_date     datetime
    uuid            str
    """
    title = mongoengine.StringField(max_length=256, default='')
    artist = mongoengine.StringField(max_length=256, default='')
    album = mongoengine.StringField(max_length=256, default='')
    company = mongoengine.StringField(max_length=256, default='')
    public_time = mongoengine.StringField(max_length=10, default='')
    kbps = mongoengine.StringField(max_length=5, default='')
    cover = mongoengine.FileField()
    audio = mongoengine.FileField()
    upload_date = mongoengine.DateTimeField()

    uuid = mongoengine.StringField(unique=True)

    meta = {
        'ordering': ['-upload_date']
    }


    def delete(self):
        self.cover.delete()
        self.audio.delete()
        super(MusicStorage, self).delete()

    def update(self, **kwargs):
        cover = kwargs.pop('cover', None)
        audio = kwargs.pop('audio', None)
        if cover:
            self.cover.replace(cover)
        if audio:
            self.audio.replace(audio)
        self.save()
        super(MusicStorage, self).update(**kwargs)
