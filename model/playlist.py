#!/usr/bin/env python
# encoding: utf-8
import random
from model.music import get_music


def get_music_by_channel(channel, num):
    num = min(len(channel.music_list), num)
    music_list = random.sample(channel.music_list, num)
    return [get_music(key=each)[0] for each in music_list]
