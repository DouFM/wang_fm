#!/usr/bin/env python
#coding:utf8
from model.music import get_music
from model.channel import get_channel
from spider.douban import login, update_channel_list, update_music_by_channel
from utils import BaseTest


class test_douban(BaseTest):
    def test_update_music_by_channel(self):
        assert login(), 'check the DOUBAN_USER_NAME, DOUBAN_USER_PASSWORD in config.py'
        assert len(update_channel_list()) > 0
        assert len(get_music()) == 0
        channel = get_channel()[0]
        music_list = update_music_by_channel(channel, 1)
        assert len(music_list) == 1
        assert len(get_music()) == 1
        channel = get_channel()[0]
        assert len(channel.music_list) == 1
