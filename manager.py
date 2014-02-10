#!/usr/bin/env python
#coding:utf8
import random
import datetime
from apscheduler.scheduler import Scheduler

from flask.ext.script import Manager
from fm import app
from model.user import add_user
from spider.douban import login, update_channel_list, update_music_by_channel
from model.channel import get_channel, update_channel
from tasks.spider_task import douban_spider_task
from config import ADMIN_NAME, ADMIN_PASSWORD

manager = Manager(app)


@manager.command
def setup():
    '''setup db & update channel & get demo music'''
    print 'setuping...'
    print 'setting admin'
    try:
        assert add_user(ADMIN_NAME, ADMIN_PASSWORD, 'admin'), 'admin already exist!!!this will pass'
    except:
        pass
    print 'login douban...'
    assert login(), 'check the DOUBAN_USER_NAME, DOUBAN_USER_PASSWORD in config.py'
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
    '''update channel by uuid and num'''
    num = int(num)
    print uuid, num
    channel = get_channel(uuid=uuid)[0]
    music_list = update_music_by_channel(channel, num)
    assert len(music_list) == num
    print 'update %s %s %s for %d music' % (
        channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list), num)


@manager.command
def auto_update():
    '''update until stop manually'''
    channels = get_channel(playable=True)
    while True:
        channel = random.choice(channels)
        print datetime.datetime.now()
        print '%s\t\t%s\t\t%s' % (channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list))
        music_list = update_music_by_channel(channel, 5)
        print '%s\t\t%s\t\t%s' % (channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list))


@manager.command
def channels(uuid=None):
    '''get one/all channels in db'''
    if not uuid:
        print 'uuid\t\tname\t\tmusic_num\t\tplayable'
        for channel in get_channel():
            print '%s\t\t%s\t\t%s\t\t%s' % (
                channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list), channel.playable)
    else:
        channel = get_channel(uuid=uuid)[0]
        print 'uuid\t\tname'
        print '%s\t\t%s\t\t%s\t\t%s' % (
            channel.uuid.encode('utf8'), channel.name.encode('utf8'), len(channel.music_list), channel.playable)


@manager.command
def enable_channel(uuid):
    '''set channel playable'''
    channel = get_channel(uuid=uuid)[0]
    update_channel(channel, playable=True)


@manager.command
def disable_channel(uuid):
    '''set channel not playable'''
    channel = get_channel(uuid=uuid)[0]
    update_channel(channel, playable=False)


@manager.command
def tasks():
    '''run tasks, keep it running for spider'''
    sched = Scheduler(standalone=True)
    # http://pythonhosted.org/APScheduler/modules/scheduler.html
    sched.add_cron_job(douban_spider_task, hour=2)
    sched.start()


if __name__ == "__main__":
    manager.run()
