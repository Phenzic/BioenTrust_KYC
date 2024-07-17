from . import Config

from pymongo import MongoClient

def get_db():
    client = MongoClient(Config.MONGO_URI)
    db = client
    return db
