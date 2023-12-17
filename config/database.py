from envparse import Env
from pymongo import MongoClient
import pandas as pd

env = Env()

client = MongoClient('mongodb://mongo_db:27017/')
db = client.user_database
data_collection = db['deutsch']
users = db['users']


def search_or_save_user(user_id, username, datetime):
    user_filter = {
        'user_id': user_id
    }
    user = users.find_one(user_filter)
    if not user:
        user = {
            'user_id': user_id,
            'username': username,
            'datetime': datetime,
            'status': 'active'
        }
        users.insert_one(user)
    return user

