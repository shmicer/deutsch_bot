import pandas as pd
from envparse import Env
from pymongo import MongoClient

env = Env()


class MongoDBClient:
    def __init__(self, url):
        self.url = url
        self.client = None

    def __enter__(self):
        self.client = MongoClient(self.url)
        return self.client

    def __exit__(self, exc_type, exc_value, traceback):
        if self.client:
            self.client.close()


try:
    MONGODB_URL = env.str('MONGODB_URL', default='mongodb://localhost:27017/')

    client = MongoClient(MONGODB_URL)
    db = client.user_database
    data_collection = db['deutsch']


    csv_file_path = 'words.csv'
    data = pd.read_csv(csv_file_path, header=None)
    data.columns = ['word', 'translate']

    with MongoDBClient(MONGODB_URL) as client:
        data_dict = data.to_dict(orient='records')
        data_collection.insert_many(data_dict)

except Exception as e:
    print(f"Произошла ошибка: {e}")