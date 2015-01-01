#!/usr/bin/env python
#coding:utf8
import mongoengine

from database.base_storage import BaseMongoStorage
from utility.utils import BaseTest


class demo_mongo_storage(BaseMongoStorage, mongoengine.Document):
    var_str = mongoengine.StringField(unique=True)
    var1 = mongoengine.IntField(default=0)
    var2 = mongoengine.IntField(default=0)


class test_demo_mongo_storage(BaseTest):
    def test_save(self):
        assert len(demo_mongo_storage.get()) == 0
        obj = demo_mongo_storage()
        obj.var_str = 'str'
        obj.var1 = 1
        obj.save()
        assert type(obj.key) == str
        assert len(demo_mongo_storage.get()) == 1
        assert obj == demo_mongo_storage.get(key=obj.key)[0]
        pass

    def test_save_unique(self):
        obj = demo_mongo_storage()
        obj.var_str = 'str'
        obj.save()
        obj = demo_mongo_storage()
        obj.var_str = 'str'
        try:
            obj.save()
        except:
            pass

    def test_get_limit(self):
        assert len(demo_mongo_storage.get()) == 0
        add_var1_list = range(10)
        for i in add_var1_list:
            obj = demo_mongo_storage()
            obj.var_str = 'str' + str(i)
            obj.var1 = i
            obj.save()
        var1_list = [each.var1 for each in demo_mongo_storage.get(start=2, end=7)]
        assert set(add_var1_list[2:7]) == set(var1_list)

    def test_update(self):
        assert len(demo_mongo_storage.get()) == 0
        obj = demo_mongo_storage()
        obj.var_str = 'str'
        obj.var1 = 0
        obj.save()
        obj.update(var1=1)
        obj = demo_mongo_storage.get()[0]
        assert obj.var1 == 1

    def test_get_multi(self):
        assert len(demo_mongo_storage.get()) == 0
        obj = demo_mongo_storage()
        obj.var_str = 'str1'
        obj.var1 = 1
        obj.var2 = 1
        obj.save()
        obj = demo_mongo_storage()
        obj.var_str = 'str2'
        obj.var1 = 1
        obj.var2 = 2
        obj.save()
        obj = demo_mongo_storage()
        obj.var_str = 'str3'
        obj.var1 = 2
        obj.var2 = 1
        obj.save()
        obj = demo_mongo_storage()
        obj.var_str = 'str4'
        obj.var1 = 2
        obj.var2 = 2
        obj.save()
        assert len(demo_mongo_storage.get(var1=1)) == 2
        assert len(demo_mongo_storage.get(var1=2)) == 2
        assert len(demo_mongo_storage.get(var1=1, var2=1)) == 1
        assert len(demo_mongo_storage.get(var1=2, var2=2)) == 1

    def test_status(self):
        assert len(demo_mongo_storage.get()) == 0
        add_var1_list = range(10)
        for i in add_var1_list:
            obj = demo_mongo_storage()
            obj.var_str = 'str' + str(i)
            obj.var1 = i
            obj.save()
        assert demo_mongo_storage.status()['count'] == 10
