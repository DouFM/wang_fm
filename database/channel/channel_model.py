#!/usr/bin/env python
# encoding: utf-8
import datetime

from database.channel.channel_storage import ChannelStorage


def add_channel(name, uuid):
    channel = ChannelStorage()
    channel.name = name
    channel.uuid = uuid
    channel.upload_date = datetime.datetime.now()
    channel.save()
    return channel


def get_channel(**kwargs):
    channels = ChannelStorage.get(**kwargs)
    return channels


def get_channel_status():
    return ChannelStorage.status()


def update_channel(channel, **kwargs):
    channel.update(**kwargs)


def delete_channel(channel):
    channel.delete()
