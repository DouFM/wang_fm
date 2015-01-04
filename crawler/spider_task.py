#!/usr/bin/env python
# encoding: utf-8
import datetime
from log.spider import spider_task_log
from database.channel.channel_model import get_channel
from crawler.spider import login, update_channel_list, update_music_by_channel


def douban_spider_task():
    info = u'tasks.spider_task.douban_spider_task: start %s' % (datetime.datetime.now())
    spider_task_log.log_info(info)

    login()
    info = u'tasks.spider_task.douban_spider_task: login success %s' % (datetime.datetime.now())
    spider_task_log.log_info(info)

    channel_list = update_channel_list()
    for channel_name in channel_list:
        info = u'tasks.spider_task.douban_spider_task: updated_channel %s' % channel_name
        spider_task_log.log_info(info)

    channel_list = get_channel()
    for channel in channel_list:
        music_list = update_music_by_channel(channel, channel.update_num)
        info = u'tasks.spider_task.douban_spider_task: channel %s, updated_num %d' % (channel, len(music_list))
        print info
        spider_task_log.log_info(info)

    info = u'tasks.spider_task.douban_spider_task: end %s' % (datetime.datetime.now())
    spider_task_log.log_info(info)


if __name__ == "__main__":
    douban_spider_task()
