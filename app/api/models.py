# models.py
from pymongo import MongoClient
import os

client = MongoClient('mongodb://localhost:27017/')
db = client.your_database_name

class APIModel:
    @staticmethod
    def find_api_vault_by_id(client_id):
        return db.api_vault.find_one({'id': client_id})

    @staticmethod
    def find_api_logs_by_id(api_key):
        return db.api_logs.find_one({"_id": api_key})

    @staticmethod
    def update_sandbox_keys(user_id, api_key, secret_key):
        db.client_app.update_one({'_id': user_id}, {'$push': {'sandbox_keys': {'key': api_key, 'secret': secret_key}}})

    @staticmethod
    def insert_sandbox_keys(user_id, api_key, secret_key):
        db.client_app.update_one({'_id': user_id}, {'$set': {'sandbox_keys': [{'key': api_key, 'secret': secret_key}]}})

    @staticmethod
    def update_live_keys(user_id, api_key, secret_key):
        db.client_app.update_one({'_id': user_id}, {'$push': {'live_keys': {'key': api_key, 'secret': secret_key}}})

    @staticmethod
    def insert_live_keys(user_id, api_key, secret_key):
        db.client_app.update_one({'_id': user_id}, {'$set': {'live_keys': [{'key': api_key, 'secret': secret_key}]}})

    @staticmethod
    def delete_sandbox_key(user_id, api_key, secret_key):
        return db.client_app.update_one({'_id': user_id}, {'$pull': {'sandbox_keys': {'key': api_key, 'secret': secret_key}}})

    @staticmethod
    def delete_live_key(user_id, api_key, secret_key):
        return db.client_app.update_one({'_id': user_id}, {'$pull': {'live_keys': {'key': api_key, 'secret': secret_key}}})
