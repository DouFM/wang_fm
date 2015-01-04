#!/usr/bin/env python
# encoding: utf-8
import datetime

from database.user.user_storage import UserStorage
from database.music.music_model import get_music


##################login###################
def add_user(user_id):
    user = UserStorage()
    user.user_id = user_id
    try:
        user.save()
    except:
        return None
    return user


################get_operation###########################
def get_user(**kwargs):
    return UserStorage.get(**kwargs)


def get_user_status():
    return UserStorage.status()



def check_operation_exist(user, op, key):
    for history in user.history:
        if history[1] == op and history[2] == key:
            return True
    return False


def get_user_history(user, start, end):
    """
        return user operation history
        return as: date, op, music_key, music_title, music_cover
    """
    if start < 0 or start > end:
        start = 0
        end = -1

    history_list = user.history[start:end]
    new_history_list = list()
    for history in history_list:
        music = get_music(key=history[2])[0]
        new_history_list.append({'date': history[0],
                             'op': history[1],
                             'key': history[2],
                             'title': music.title,
                             'audio': music.audio,
                             'cover': music.cover})
    return new_history_list


def get_user_music_list(user, kind, start, end):
    if start < 0 or start > end:
        start = 0
        end = -1
    if kind == 'listened':
        music_key_list = user.listened[start:end]
    elif kind == 'dislike':
        music_key_list = user.dislike[start:end]
    elif kind == 'favor':
        music_key_list = user.favor[start:end]
    elif kind == 'share':
        music_key_list = user.share[start:end]
    else:
        return []

    music_list = []
    #at here we just return music object
    for key in music_key_list:
        music = get_music(key=key)[0]
        music_list.append(music)
    return music_list


##################edit operation#############################
def update_user(user, **kwargs):
    kwargs.pop('user_id', None)
    user.update(**kwargs)


def delete_user(user):
    user.delete()


def add_user_history(user, op, music_key):
    new_history = user.history
    new_favor = user.favor
    new_dislike = user.dislike
    new_listened = user.listened
    new_share = user.share
    new_history.insert(0, [datetime.datetime.now(), op, music_key])
    if op == 'favor':
        if music_key in new_dislike:
            new_dislike.remove(music_key)
        if music_key not in new_favor:
            new_favor.insert(0, music_key)
        else:
            new_favor.remove(music_key)
    elif op == 'dislike':
        if music_key in new_favor:
            new_favor.remove(music_key)
        if music_key not in new_dislike:
            new_dislike.insert(0, music_key)
        else:
            new_dislike.remove(music_key)
    elif op == 'share':
        if music_key not in new_share:
            new_share.insert(0, music_key)
    elif op == 'listened':
        #we should order listened music by data
        if music_key in new_listened:
            new_listened.remove(music_key)
        new_listened.insert(0, music_key)
    else:
        assert False

    update_user(user, history=new_history, favor=new_favor,
                dislike=new_dislike, share=new_share, listened=new_listened)
