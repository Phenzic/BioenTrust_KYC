import uuid
from passlib.hash import pbkdf2_sha256
from flask import current_app as app
from ..config.database import get_db


class User:
    def __init__(self, first_name, last_name, email, password, wallet=0):
        self._id = uuid.uuid4().hex
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = pbkdf2_sha256.hash(password)
        self.wallet = wallet

    @staticmethod
    def find_by_email(email):
        return get_db.users.find_one({"email": email})

    def save_to_db(self):
        get_db.users.insert_one(self.to_dict())

    def to_dict(self):
        return {
            "_id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "wallet": self.wallet
        }

class ClientApp:
    def __init__(self, user_id):
        self._id = user_id
        self.apps = []

    def save_to_db(self):
        get_db.client_app.insert_one(self.to_dict())

    def to_dict(self):
        return {
            "_id": self._id,
            "apps": self.apps
        }

class ServiceCharge:
    def __init__(self, user_id, email):
        self._id = user_id
        self.email = email
        self.service = {}

    def save_to_db(self):
        get_db.service_charge.insert_one(self.to_dict())

    def to_dict(self):
        return {
            "_id": self._id,
            "email": self.apps
        }
