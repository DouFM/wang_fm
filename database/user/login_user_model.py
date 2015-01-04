# coding:utf-8
import datetime
from login_user_storage import LoginUserStorage


def add_login_user(**kwargs):
    login_user = LoginUserStorage()
    login_user.user_id = kwargs['user_id']
    login_user.cur_status = 'login'
    login_user.cookie_key = kwargs['cookie_key']
    login_user.user_name = kwargs['user_name']
    login_user.update_date = datetime.datetime.now()
    try:
        login_user.save()
    except Exception:
        return None
    return login_user


def get_login_user(**kwargs):
    return LoginUserStorage.get(**kwargs)


def get_all_login_user():
    return LoginUserStorage.get(cur_status='login')


def check_login_user(**kwargs):
    if LoginUserStorage.get(**kwargs):
        return True
    return False


def delete_login_user(login_user):
    """
    if user deliberate logout, we should delete login user
    """
    login_user.delete()


def update_login_user_date(**kwargs):
    """
    every user operation will update login user table, and delete the expire user
    """
    login_user = LoginUserStorage.get(**kwargs)
    if not login_user:
        return
    login_user[0].update(update_date=datetime.datetime.now())
    exceed_date = datetime.datetime.now() - datetime.timedelta(seconds=24*60)
    expire_login_user_list = LoginUserStorage.get(update_date__lte=exceed_date)
    for user in expire_login_user_list:
        user.update(cur_status='logout', update_date=datetime.datetime.now())


def auto_login_by_cookie(**kwargs):
    user = LoginUserStorage.get(**kwargs)
    if not user:
        return False
    user[0].update(cur_status='login', update_date=datetime.datetime.now())
    return True
