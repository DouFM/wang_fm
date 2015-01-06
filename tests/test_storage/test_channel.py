#!/usr/bin/env python
#coding:utf8
import datetime
from storage.channel import ChannelStorage
from utils import BaseTest


class test_channel_storage(BaseTest):
    def test_simple(self):
        assert len(ChannelStorage.get()) == 0
        channel = ChannelStorage()
        channel.name = 'demo_name'
        channel.music_list = ['1' * 24]
        now = datetime.datetime(2013, 12, 24, 10, 8, 3)
        channel.upload_date = now
        channel.uuid = 'douban-cid'
        channel.save()
        assert len(ChannelStorage.get()) == 1
        assert len(ChannelStorage.get(name='demo_name')) == 1
        assert len(ChannelStorage.get(name='unkown')) == 0
        channel = ChannelStorage.get()[0]
        assert channel.name == 'demo_name'
        assert channel.music_list == ['1' * 24]
        assert channel.upload_date == now
        channel.delete()
        assert len(ChannelStorage.get()) == 0

    def test_update(self):
        assert len(ChannelStorage.get()) == 0
        channel = ChannelStorage()
        channel.name = 'demo_name'
        channel.music_list = ['1' * 24]
        now = datetime.datetime(2013, 12, 24, 10, 8, 3)
        channel.upload_date = now
        channel.uuid = 'douban-cid'
        channel.save()
        channel.update(music_list=['2' * 24])
        channel = ChannelStorage.get()[0]
        assert channel.music_list == ['2' * 24]
