#!/usr/bin/env python
# encoding: utf-8
'''
Ref:
https://github.com/zonyitoo/doubanfm-qt/wiki/%E8%B1%86%E7%93%A3FM-API
'''
import json
import random
import traceback

import requests
import requests.exceptions

from database.channel.channel_model import get_channel, add_channel, update_channel
from database.music.music_model import get_music, add_music
from config.config import DOUBAN_USER_NAME, DOUBAN_USER_PASSWORD
from log.spider import spider_log

DOUBAN_SPIDER_NAME = 'radio_desktop_win'
DOUBAN_SPIDER_VERSION = '100'
DOUBAN_CHANNEL_UUID_FORMAT = 'douban-%d'    # % (channel_id)
DOUBAN_MUSIC_UUID_FORMAT = 'douban-%d-%d'   # % (aid, sid)

g_user_id = None
g_token = None
g_expire = None


def login():
    payload = {'app_name': DOUBAN_SPIDER_NAME,
               'version': DOUBAN_SPIDER_VERSION,
               'email': DOUBAN_USER_NAME,
               'password': DOUBAN_USER_PASSWORD}
    try:
        r = requests.post("http://www.douban.com/j/app/login", data=payload)
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.Timeout:
        return False
    r = json.loads(r.text)
    if r['r'] != 0:
        info = 'crawler.douban.login: failed. r=%s', r
        spider_log.log_info(info)
        return False
    global g_user_id, g_token, g_expire
    g_user_id = r['user_id']
    g_token = r['token']
    g_expire = r['expire']
    spider_log.log_info('crawler.douban.login: success')
    return True


def update_channel_list():
    r = requests.get("http://www.douban.com/j/app/radio/channels")
    r = json.loads(r.text)
    channel_list = []
    assert 'channels' in r
    for channel in r['channels']:
        cid = int(channel['channel_id'])
        uuid = DOUBAN_CHANNEL_UUID_FORMAT % cid
        if cid != 0 and not get_channel(uuid=uuid):
            # not private list and not in db
            new_channel = add_channel(channel['name'], uuid)
            channel_list.append(new_channel.name)
    return channel_list


def _update_channel_once(channel, max_num=20):
    """"update music in channel. max is the max number it will update
    return updated music
    please login before this function"""
    global g_user_id, g_token, g_expire
    # TODO
    # maybe need a better method to assert and get cid
    assert channel.uuid.startswith(DOUBAN_CHANNEL_UUID_FORMAT.split('-')[0])
    cid = int(channel.uuid.split('-')[1])
    if not channel.music_list:
        payload = {'app_name': DOUBAN_SPIDER_NAME,
                   'version': DOUBAN_SPIDER_VERSION,
                   'user_id': g_user_id,
                   'expire': g_expire,
                   'token': g_token,
                   'channel': cid,
                   'type': 'n'}
    else:
        uuid = get_music(key=random.choice(channel.music_list))[0].uuid
        sid = uuid.split('-')[2]
        payload = {'app_name': DOUBAN_SPIDER_NAME,
                   'version': DOUBAN_SPIDER_VERSION,
                   'user_id': g_user_id,
                   'expire': g_expire,
                   'token': g_token,
                   'channel': cid,
                   'type': 'p',
                   'sid': sid}

        # # mark as listened
        # mark_payload = {'app_name': DOUBAN_SPIDER_NAME,
        #                 'version': DOUBAN_SPIDER_VERSION,
        #                 'user_id': _user_id,
        #                 'expire': _expire,
        #                 'token': _token,
        #                 'channel': cid,
        #                 'type': 'e',
        #                 'sid': sid}
        # try:
        #     requests.get("http://www.douban.com/j/app/radio/people", params=mark_payload, timeout=5)
        # except:
        #     pass

        # # don't play again
        # mark_payload = {'app_name': DOUBAN_SPIDER_NAME,
        #                 'version': DOUBAN_SPIDER_VERSION,
        #                 'user_id': _user_id,
        #                 'expire': _expire,
        #                 'token': _token,
        #                 'channel': cid,
        #                 'type': 'b',
        #                 'sid': sid}
        # try:
        #     requests.get("http://www.douban.com/j/app/radio/people", params=mark_payload, timeout=5)
        # except:
        #     pass
    try:
        r = requests.get("http://www.douban.com/j/app/radio/people", params=payload, timeout=5)
    except requests.exceptions.ConnectionError:
        traceback.print_exc()
        return []
    except requests.exceptions.Timeout:
        traceback.print_exc()
        return []
    r = json.loads(r.text)
    assert r['r'] == 0
    update_music = []
    for song in r['song']:
        try:
            uuid = DOUBAN_MUSIC_UUID_FORMAT % (int(song['aid']), int(song['sid']))
        except Exception:
            # ads
            continue
        if not get_music(uuid=uuid):
            try:
                import pdb; pdb.set_trace()
                cover_fd = requests.get(song['picture'], stream=True, timeout=5).raw
                audio_fd = requests.get(song['url'], stream=True, timeout=5).raw
            except requests.exceptions.ConnectionError:
                traceback.print_exc()
                continue
            except requests.exceptions.Timeout:
                traceback.print_exc()
                continue
            try:
                print song['rating_avg']
                music = add_music(song['title'], song['artist'], song['albumtitle'],
                                  song['company'], song['public_time'], song['kbps'],
                                  cover_fd, audio_fd, uuid)
            except Exception:
                traceback.print_exc()
                continue

            spider_log.log_info("add music:"+uuid)
        else:
            music = get_music(uuid=uuid)[0]

        if music and music.key not in channel.music_list:
            channel_music_list = channel.music_list
            channel_music_list.append(music.key)
            update_channel(channel, music_list=channel_music_list)
            update_music.append(music)
            if len(update_music) >= max_num:
                break
    return update_music


def update_music_by_channel(channel, num):
    """update the music in channel, music count is num"""
    updated_music = []
    retry = 0
    while num > 0:
        music_list = _update_channel_once(channel, num)
        updated_music.extend(music_list)
        num -= len(music_list)
        if not music_list:
            retry += 1
            if retry > 5:
                break
    return updated_music
