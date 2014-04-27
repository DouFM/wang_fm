#!/usr/bin/env python
# encoding: utf-8
import datetime
import hashlib
from storage.user import UserStorage
from model.music import get_music


def add_user(name, password, level):
    '''add new user, return user obj'''
    user = UserStorage()
    user.name = name
    user.password = _encrypt(name, password)
    assert level in ['disable', 'normal', 'admin']
    user.level = level
    user.regist_date = datetime.datetime.now()
    try:
        user.save()
    except:
        return None
    return user


def get_user(**kwargs):
    '''return user obj'''
    return UserStorage.get(**kwargs)


def get_user_status():
    '''return users status'''
    return UserStorage.status()


def update_user(user, **kwargs):
    '''update user obj by kwargs'''
    if kwargs.get('name'):
        raise AttributeError("Can't update user name")
    password = kwargs.pop('password', None)
    if password:
        kwargs['password'] = _encrypt(user.name, password)
    level = kwargs.get('level')
    if level:
        assert level in ['disable', 'normal', 'admin']
    user.update(**kwargs)


def delete_user(user):
    '''delete user obj'''
    user.delete()


def check_user_password(user, password):
    return user.password == _encrypt(user.name, password)


def check_user_enable(user):
    return not user.level == 'disable'


def add_user_history(user, op, music_key):
    new_history = user.history
    new_favor = user.favor
    new_dislike = user.dislike
    new_listened = user.listened
    new_shared = user.shared
    new_history.insert(0, [datetime.datetime.now(), op, music_key])
    if op == 'favor':
        if music_key in new_dislike:
            new_dislike.remove(music_key)
        if music_key not in new_favor:
            new_favor.insert(0, music_key)
    elif op == 'dislike':
        if music_key in new_favor:
            new_favor.remove(music_key)
        if music_key not in new_dislike:
            new_dislike.insert(0, music_key)
    elif op == 'shared':
        if music_key not in new_shared:
            new_shared.insert(0, music_key)
    elif op == 'listened':
        new_listened += 1
    else:
        assert False

    update_user(user, history=new_history, favor=new_favor,
                dislike=new_dislike, shared=new_shared, listened=new_listened)


def get_user_history(user, start, end):
    '''return as: date, op, music_key, music_title, music_cover
    '''
    historys = user.history[start: end]
    new_historys = []
    for history in historys:
        music = get_music(key=history[2])[0]
        history.append(music.title)
        history.append(music.cover)
        new_historys.append({'date': history[0],
                             'op': history[1],
                             'key': history[2],
                             'title': history[3],
                             'cover': history[4]})
    return new_historys


def get_user_favor(user, start, end):
    '''return music info
    '''
    favors = user.favor[start: end]
    new_favors = []
    for favor in favors:
        music = get_music(key=favor)[0]
        new_favors.append(music)
    return new_favors


def _encrypt(name, password):
    '''encrpy the password by name'''
    return hashlib.md5(password.encode('utf8') + name.encode('utf8')).hexdigest().upper()
