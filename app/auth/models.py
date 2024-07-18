import uuid
from passlib.hash import pbkdf2_sha256
from flask import current_app as app


class User:
    def __init__(self, _id, first_name, last_name, email, password, wallet=0):
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.wallet = wallet
        print(self.password, "....................$$$$$$$$$$$$$$$$$$")

    @staticmethod
    def find_by_email(email):
        db = app.db.users
        return db["user"].find_one({"email": email})

    def save_to_db(self):
        db = app.db.users
        return db["user"].insert_one(self.to_dict())

    def to_dict(self):
        return {
            "_id": self._id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "wallet": self.wallet,
        }


class ClientApp:
    def __init__(self, user_id):
        self._id = user_id
        self.apps = []

    def save_to_db(self):
        db = app.db.client
        return db["client_data"].insert_one(self.to_dict())

    def to_dict(self):
        return {"_id": self._id, "apps": self.apps}


class ServiceCharge:
    def __init__(self, user_id, email):
        self._id = user_id
        self.email = email
        self.service = {}
        self.charges = 0

    def save_to_db(self):
        db = app.db.users
        return db["service_charges"].insert_one(self.to_dict())

    def to_dict(self):
        return {"_id": self._id, "email": self.email, "charges": self.charges}
