from pymongo import MongoClient
from ..utils import redis_client
from ..config.database import get_db
from flask import current_app as app


class UserModel:
    @staticmethod
    def find_by_id(user_id):
        db = app.db.users
        return db["user"].find_one({"_id": user_id})

    @staticmethod
    def update_wallet(user_id, new_wallet_balance):
        db = app.db.users
        #    note: try to optimize by reducing multiple db querying
        db["users"].update_one(
            {"_id": user_id}, {"$set": {"wallet": new_wallet_balance}}
        )
        return db["users"].find_one({"_id": user_id})


class ClientAppModel:
    @staticmethod
    def find_by_app_id(app_id):
        db = app.db.client
        return db["client_data"].find_one({"apps.app_id": app_id})


class ServiceChargeModel:
    @staticmethod
    def find_by_user_id(user_id):
        db = app.db.client
        return db["client_data"].find_one({"_id": user_id})


class ClientUserModel:
    @staticmethod
    def find_by_user_id(user_id):
        db = app.db.client
        return db["client_user"].find_one({"user_id": user_id})

    @staticmethod
    def update_live_image(user_id, live_image):
        db = app.db.client
        return db["client_user"].update_one(
            {"user_id": user_id}, {"$set": {"live_image": live_image}}
        )
