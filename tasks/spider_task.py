#!/usr/bin/env python
# encoding: utf-8
import datetime
from model.channel import get_channel
from spider.douban import login, update_channel_list, update_music_by_channel


def douban_spider_task():
    print 'tasks.spider_task.douban_spider_task: start %s' % (datetime.datetime.now())
    login()
    print 'tasks.spider_task.douban_spider_task: login success %s' % (datetime.datetime.now())
    channels = update_channel_list()
    print 'tasks.spider_task.douban_spider_task: updated_channel %s' % (channels)
    for channel in get_channel():
        music_list = update_music_by_channel(channel, channel.update_num)
        print u'tasks.spider_task.douban_spider_task: channel %s, updated_num %d' % (channel, len(music_list))
    print 'tasks.spider_task.douban_spider_task: end %s' % (datetime.datetime.now())
