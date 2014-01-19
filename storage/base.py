#!/usr/bin/env python
#coding:utf8
import mongoengine


class BaseMongoStorage(object):
    '''adapter for MongoDB'''
    def save(self):
        '''save obj to db'''
        mongoengine.Document.save(self)

    def update(self, **kwargs):
        '''update obj by kwargs

        update(var1=1)
        update(var1=1, var2=2)'''
        new_kwargs = {}
        for key in kwargs:
            new_kwargs['set__' + key] = kwargs[key]
        mongoengine.Document.update(self, **new_kwargs)

    def delete(self):
        '''delete obj from db'''
        mongoengine.Document.delete(self)

    @classmethod
    def get(cls, **kwargs):
        '''get obj list from db'''
        start = kwargs.pop('start', None)
        end = kwargs.pop('end', None)
        key = kwargs.pop('key', None)
        if key:
            kwargs['pk'] = key
        return [obj for obj in cls.objects(**kwargs)[start:end]]

    @classmethod
    def status(cls):
        '''get status of this storage'''
        return {'count': cls.objects.count()}

    @property
    def key(self):
        return str(self.pk)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)
