from pymongo import MongoClient
from os import environ
from dotenv import load_dotenv


load_dotenv()

class MongoConnection:
    _client = None
    @classmethod
    def get_connection(cls):
        if cls._client is None:
            cls._client = MongoClient(environ.get('MONGO_URL'))
        return cls._client