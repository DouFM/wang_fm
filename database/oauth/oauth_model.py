#!/usr/bin/env python
# encoding: utf-8
import datetime
from database.oauth.oauth_storage import OAuthStorage


def add_oauth(**kwargs):
    oauth = OAuthStorage()
    oauth.request_token = kwargs['request_token']
    oauth.user_recognition = kwargs['user_recognition']
    oauth.date = datetime.datetime.now()
    try:
        oauth.save()
    except Exception:
        return None
    return oauth


def get_oauth(**kwargs):
    return OAuthStorage.get(**kwargs)


def update_oauth(oauth, **kwargs):
    oauth.update(**kwargs)


def delete_oauth(oauth):
    oauth.delete()


def delete_expire_oauth():
    exceed_date = datetime.datetime.now() + datetime.timedelta(seconds=10*60)
    expire_oauth_list = OAuthStorage.get(date__lte=exceed_date)
    for oauth in expire_oauth_list:
        delete_oauth(oauth)