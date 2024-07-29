
from passlib.hash import pbkdf2_sha256
from flask import current_app as app
from ..utils.otp_handler import otp_handler
from ..utils import redis_client


class User:
    def __init__(self, _id, first_name, last_name, email, password, wallet=0):
        self._id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.wallet = wallet

    @staticmethod
    def find_by_id(user_id):
        db = app.db.users
        return db["user"].find_one({"_id": user_id})

    @staticmethod
    def update_password(user_id, new_password):
        db = app.db.users
        db["user"].update_one(
            {"_id": user_id}, {"$set": {"password": pbkdf2_sha256.hash(new_password)}}
        )

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


class TokenBlocklist:
    @staticmethod
    def add_to_blocklist(jti, expires):
        redis_client.set(jti, "", ex=expires)

    @staticmethod
    def is_token_revoked(jti):
        return redis_client.get(jti) is not None


class EmailService:
    @staticmethod
    def send_password_reset(
            email,
            subject,
            sender,
            recipients,
            text_body,
            html_body):
        otp_handler.send_email(
            subject=subject,
            sender=sender,
            recipients=recipients,
            text_body=text_body,
            html_body=html_body,
        )


class ClientApp:
    def __init__(self, user_id):
        self._id = user_id
        self.apps = []

    @staticmethod
    def find_by_app_id(app_id):
        return app.db.client["client_app"].find_one({"apps.app_id": app_id})

    @staticmethod
    def find_by_user_id(user_id):
        return app.db.client["client_app"].find_one({"_id": user_id})

    def save_to_db(self):
        db = app.db.client
        return db["client_app"].insert_one(self.to_dict())

    def to_dict(self):
        return {"_id": self._id, "apps": self.apps}


class ServiceCharge:
    def __init__(self, user_id, email):
        self._id = user_id
        self.email = email
        self.service = {
            "e-affidavit": 0,
            "e-attendance": 0,
            "e-census": 0,
            "kyc": 0,
        }
        # self.charges = 0

    def save_to_db(self):
        db = app.db.users
        return db["service_charges"].insert_one(self.to_dict())

    def to_dict(self):
        return {"_id": self._id, "email": self.email, "services": self.service}


class ClientUser:
    @staticmethod
    def insert_new_request(new_request):
        app.db.client["client_user"].insert_one(new_request)

    @staticmethod
    def get_user_details(user_id):
        user_details = app.db.users.find_one({"_id": user_id})
        return user_details
