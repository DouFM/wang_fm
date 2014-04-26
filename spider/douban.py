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
from model.channel import get_channel, add_channel, update_channel
from model.music import get_music, add_music
from config import DOUBAN_USER_NAME, DOUBAN_USER_PASSWORD

DOUBAN_SPIDER_NAME = 'radio_desktop_win'
DOUBAN_SPIDER_VERSION = '100'
DOUBAN_CHANNEL_UUID_FORMAT = 'douban-%d'    # % (channel_id)
DOUBAN_MUSIC_UUID_FORMAT = 'douban-%d-%d'   # % (aid, sid)

_user_id = None
_token = None
_expire = None


def login():
    payload = {'app_name': DOUBAN_SPIDER_NAME,
               'version': DOUBAN_SPIDER_VERSION,
               'email': DOUBAN_USER_NAME,
               'password': DOUBAN_USER_PASSWORD}
    try:
        r = requests.post("http://www.douban.com/j/app/login", data=payload)
    except requests.exceptions.ConnectionError, requests.exceptions.Timeout:
        return False
    r = json.loads(r.text)
    if r['r'] != 0:
        print 'spider.douban.login: failed. r=', r
        return False
    global _user_id, _token, _expire
    _user_id = r['user_id']
    _token = r['token']
    _expire = r['expire']
    return True


def update_channel_list():
    r = requests.get("http://www.douban.com/j/app/radio/channels")
    r = json.loads(r.text)
    channel_list = []
    assert 'channels' in r
    for channel in r['channels']:
        cid = int(channel['channel_id'])
        uuid = DOUBAN_CHANNEL_UUID_FORMAT % (cid)
        if cid != 0 and len(get_channel(uuid=uuid)) == 0:
            # not private list and not in db
            new_channel = add_channel(channel['name'], uuid)
            channel_list.append(new_channel)
    return channel_list


def _update_channel_once(channel, max_num=10):
    '''update music in channel. max is the max number it will update
    return updated music
    please login before this function'''
    global _user_id, _token, _expire
    # TODO
    # maybe need a better method to assert and get cid
    assert channel.uuid.startswith(DOUBAN_CHANNEL_UUID_FORMAT.split('-')[0])
    cid = int(channel.uuid.split('-')[1])
    if channel.music_list == []:
        payload = {'app_name': DOUBAN_SPIDER_NAME,
                   'version': DOUBAN_SPIDER_VERSION,
                   'user_id': _user_id,
                   'expire': _expire,
                   'token': _token,
                   'channel': cid,
                   'type': 'n'}
    else:
        uuid = get_music(key=random.choice(channel.music_list))[0].uuid
        sid = uuid.split('-')[2]
        payload = {'app_name': DOUBAN_SPIDER_NAME,
                   'version': DOUBAN_SPIDER_VERSION,
                   'user_id': _user_id,
                   'expire': _expire,
                   'token': _token,
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
        print 'getting list'
        r = requests.get("http://www.douban.com/j/app/radio/people", params=payload, timeout=5)
    except requests.exceptions.ConnectionError, requests.exceptions.Timeout:
        traceback.print_exc()
        return []
    r = json.loads(r.text)
    assert r['r'] == 0
    update_music = []
    #channel_music_list = channel.music_list
    for song in r['song']:
        try:
            uuid = DOUBAN_MUSIC_UUID_FORMAT % (int(song['aid']), int(song['sid']))
        except:
            # ads
            continue
        print uuid
        music = None
        if len(get_music(uuid=uuid)) == 0:
            try:
                print 'getting song'
                cover_fd = requests.get(song['picture'], stream=True, timeout=5).raw
                audio_fd = requests.get(song['url'], stream=True, timeout=5).raw
            except requests.exceptions.ConnectionError, requests.exceptions.Timeout:
                traceback.print_exc()
                continue
            music = add_music(song['title'], song['artist'], song['albumtitle'],
                              song['company'], song['public_time'], song['kbps'],
                              cover_fd, audio_fd, uuid)
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
    '''update the music in channel, music count is num'''
    updated_music = []
    retry = 0
    while num > 0:
        music_list = _update_channel_once(channel, num)
        updated_music.extend(music_list)
        num -= len(music_list)
        if music_list == []:
            retry += 1
            if retry > 5:
                break
    return updated_music
