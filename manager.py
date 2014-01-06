#!/usr/bin/env python
#coding:utf8
from flask.ext.script import Manager
from apscheduler.scheduler import Scheduler
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
def tasks():
    '''run tasks, keep it running for spider'''
    sched = Scheduler(standalone=True)
    # http://pythonhosted.org/APScheduler/modules/scheduler.html
    sched.add_cron_job(douban_spider_task, hour=2)
    sched.start()


if __name__ == "__main__":
    manager.run()
