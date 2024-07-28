import datetime
import uuid
from flask import current_app as app
import requests

class ClientAdminModels:

    @staticmethod
    def get_user_details(user_id):
        user_details = app.db.users.find_one({"_id": user_id})
        return user_details

    @staticmethod
    def get_client_profile(client_id):
        return app.db.client["client_app"].find_one({"_id": client_id})

    @staticmethod
    def get_client_user_data(client_id):
        return list(app.db.client["client_app"].find({"_id": client_id}))

    @staticmethod
    def get_service_charge(client_id):
        return app.db.users["service_charges"].find_one({"_id": client_id})

    @staticmethod
    def update_client_user_status(client_id, user_id, new_status, new_status_description):
        return app.db.client["client_app"].update_one({"_id": client_id, "client_users.user_id": user_id},
                            {"$set": {"client_users.$.status": new_status, "client_users.$.status_description": new_status_description}})

    @staticmethod
    def get_client_apps(client_id):
        return app.db.client["client_app"].find_one({"_id": client_id})

    # def create_app_entry(client_id, app_data):
    #     app_name = app_data.get("name").lower()
    #     app_color = app_data.get("color")
    #     app_creation_date = datetime.datetime.today().replace(microsecond=0)
    #     app_verification = app_data.get("verification", False)
    #     app_user_information = app_data.get("user_information", False)
    #     send_email_on_verification = app_data.get("on_verification", False)
    #     redirect_url = app_data.get("redirect_url")

    #     app_entry = {
    #         "app_id": uuid.uuid4().hex,
    #         "name": app_name,
    #         "color": app_color,
    #         "date_of_creation": app_creation_date,
    #         "verification": app_verification,
    #         "user_information": app_user_information,
    #         "on_verification": send_email_on_verification,
    #         "redirect_url": redirect_url
    #     }

    #     return app.db.client_app.update_one({"_id": client_id}, {"$push": {"apps": app_entry}})
    @staticmethod
    def get_app_by_id(app_id):
        return app.db.client["client_app"].find_one({"apps": {"$elemMatch": {"app_id": app_id}}}, {"_id": 0, "apps.$": 1})

    @staticmethod
    def delete_app_by_id(client_id, app_id):
        return app.db.client["client_app"].update_one({"_id": client_id}, {"$pull": {"apps": {"app_id": app_id}}})

    @staticmethod
    def log_wallet_transaction(client_id, transaction_type, amount, old_balance, new_balance, status):
        transaction = {
            "user_id": client_id,
            "transaction_type": transaction_type,
            "amount": amount,
            "old_balance": old_balance,
            "new_balance": new_balance,
            "status": status,
            "timestamp": datetime.datetime.utcnow()
        }
        app.db.wallet_transactions.insert_one(transaction)

    @staticmethod
    def get_wallet_transactions(client_id):
        return list(app.db.wallet["transactions"].find({"user_id": client_id}))

    @staticmethod
    def update_wallet_balance(client_id, new_balance):
        return app.db.users["user"].update_one({"_id": client_id}, {"$set": {"wallet": new_balance}})
