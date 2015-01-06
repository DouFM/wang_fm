#!/usr/bin/env python
# encoding: utf-8
import datetime
from storage.channel import ChannelStorage


def add_channel(name, uuid):
    '''add new channel, return channel obj'''
    channel = ChannelStorage()
    channel.name = name
    channel.uuid = uuid
    channel.upload_date = datetime.datetime.now()
    channel.save()
    return channel


def get_channel(**kwargs):
    '''return channel obj'''
    channels = ChannelStorage.get(**kwargs)
    return channels


def get_channel_status():
    '''return channel status'''
    return ChannelStorage.status()


def update_channel(channel, **kwargs):
    '''update channel obj by kwargs'''
    channel.update(**kwargs)


def delete_channel(channel):
    '''delete channel obj'''
    channel.delete()
