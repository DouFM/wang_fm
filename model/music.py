#!/usr/bin/env python
# encoding: utf-8
import datetime
from storage.music import MusicStorage


def add_music(title, artist, album, company, public_time,
        kbps, cover_fd, audio_fd, uuid):
    '''add new music, return music obj'''
    music = MusicStorage()
    music.title = title
    music.artist = artist
    music.album = album
    music.company = company
    music.public_time = public_time
    music.kbps = kbps
    music.cover = cover_fd
    music.audio = audio_fd
    music.upload_date = datetime.datetime.now()
    music.uuid = uuid
    # TODO
    # if on save error, cover & audio also be created in db.fs.files
    # should be fix in storage
    music.save()
    return music


def get_music(**kwargs):
    '''return music obj'''
    return MusicStorage.get(**kwargs)


def get_music_status():
    '''return music set status'''
    return MusicStorage.status()


def update_music(music, **kwargs):
    '''update music obj by kwargs'''
    music.update(**kwargs)


def delete_music(music):
    '''delete music obj'''
    music.delete()
