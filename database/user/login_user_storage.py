# coding:utf-8
import mongoengine
from database.base_storage import BaseMongoStorage
from config.config import DB_HOST, DB_PORT, DB_NAME

mongoengine.connect(DB_NAME, host=DB_HOST, port=DB_PORT)


class LoginUserStorage(BaseMongoStorage, mongoengine.Document):
    """
    user_id str
    update_date date
    cookie_key str
    cur_status str
    user_name str
    """
    user_id = mongoengine.StringField(max_length=256, unique=True, required=True)
    update_date = mongoengine.DateTimeField()
    cookie_key = mongoengine.StringField(max_length=256, unique=True)
    cur_status = mongoengine.StringField(max_length=10, required=True)
    user_name = mongoengine.StringField(max_length=256, required=True)
