#!/usr/bin/env python
# encoding: utf-8
from model.channel import add_channel, get_channel, update_channel, delete_channel
from utils import BaseTest


class test_channel_model(BaseTest):
    def test_add_channel(self):
        name = 'channel_name'
        uuid = 'douban-cid'
        add_channel(name, uuid)
        assert len(get_channel()) == 1
        channel = get_channel()[0]
        assert channel.name == 'channel_name'
        assert channel.uuid == 'douban-cid'

    def test_update_channel(self):
        name = 'channel_name'
        uuid = 'douban-cid'
        channel = add_channel(name, uuid)
        assert len(get_channel()) == 1
        update_channel(channel, music_list=['1' * 24, '2' * 24])
        assert len(get_channel()) == 1
        channel = get_channel()[0]
        assert channel.music_list == ['1' * 24, '2' * 24]

    def test_delete_channel(self):
        name = 'channel_name'
        uuid = 'douban-cid'
        add_channel(name, uuid)
        assert len(get_channel()) == 1
        channel = get_channel()[0]
        delete_channel(channel)
        assert len(get_channel()) == 0
