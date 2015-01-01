#!/usr/bin/env python
#coding:utf8
import time
import random
import datetime

from apscheduler.scheduler import Scheduler
from flask.ext.script import Manager
from fm import app
from crawler.spider import login, update_channel_list, update_music_by_channel
from database.channel.channel_model import get_channel, update_channel
from database.music.music_model import get_music
from crawler.spider_task import douban_spider_task
from log.spider import spider_task_log

manager = Manager(app)


@manager.command
def setup():
    """setup db & update channel & get demo music"""
    print 'setuping...'
    print 'login douban...'
    assert login(), 'check network or the DOUBAN_USER_NAME, DOUBAN_USER_PASSWORD in config.py'
    print 'update channel list'
    update_channel_list()
    print 'update demo music'
    channel = get_channel()[0]
    music_list = update_music_by_channel(channel, 1)
    assert len(music_list) == 1
    print 'add demo channel to playlist'
    update_channel(channel, playable=True)


@manager.command
def update_channel_num(uuid, num):
    """update channel by uuid and num"""
    num = int(num)
    print uuid, num
    channel = get_channel(uuid=uuid)[0]
    assert login(), 'check network or the DOUBAN_USER_NAME, DOUBAN_USER_PASSWORD in config.py'
    music_list = update_music_by_channel(channel, num)
    assert len(music_list) == num
    print 'update %s %s %s for %d music' % (
        channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list), num)


@manager.command
def auto_update():
    """update until stop manually"""
    assert login(), 'check network or the DOUBAN_USER_NAME, DOUBAN_USER_PASSWORD in config.py'
    channels = get_channel(playable=True)
    while True:
        channel = random.choice(channels)
        print datetime.datetime.now()
        print '%s\t\t%s\t\t%s' % (channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list))
        music_list = update_music_by_channel(channel, 5)
        print '%s\t\t%s\t\t%s' % (channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list))


@manager.command
def channels(uuid=None):
    """get one/all channels in db"""
    if not uuid:
        channel_list = get_channel()
    else:
        channel_list = get_channel(uuid=uuid)

    print 'key\t\t\t\tuuid\t\t\t\tname\t\t\t\tmusic_num\t\t\t\tplayable'
    for channel in channel_list:
        print '%s\t\t%s\t\t%s\t\t%s\t\t%s' % (
           channel.key.encode('utf-8'), channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list), channel.playable)


@manager.command
def enable_channel(uuid):
    """set channel playable"""
    channel = get_channel(uuid=uuid)[0]
    update_channel(channel, playable=True)


@manager.command
def disable_channel(uuid):
    """set channel not playable"""
    channel = get_channel(uuid=uuid)[0]
    update_channel(channel, playable=False)



@manager.command
def music(uuid=None):
    if not uuid:
        music_list = get_music()
    else:
        music_list = get_music(uuid=uuid)

    print 'key\t\t\t\t\t\tuuid\t\t\t\t\t\ttitle\t\t\t\t\t\tartist'
    for music in music_list:
        print '%s\t\t%s\t\t%s\t\t\t\t%s' % (
            music.key.encode('utf-8'), music.uuid.encode('utf8'), music.title.encode('utf8'), music.artist.encode('utf-8'))

@manager.command
def tasks(hour):
    """run tasks, keep it running for crawler"""
    sched = Scheduler(standalone=True)
    # http://pythonhosted.org/APScheduler/modules/scheduler.html
    sched.add_cron_job(douban_spider_task, hour=int(hour))
    sched.start()
    info = 'start tasks at' + datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    spider_task_log.log_info(info)


if __name__ == "__main__":
    manager.run()
