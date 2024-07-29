from flask import current_app as app


class APIModel:
    @staticmethod
    def find_api_vault_by_id(app_id):
        return app.db.api["api_logs"].find_one({"id": app_id})

    @staticmethod
    def find_api_logs_by_id(api_key):
        return app.db.api["api_logs"].find_one({"_id": api_key})

    @staticmethod
    def find_by_user_id(user_id):
        return app.db.client["client_app"].find_one({"_id": user_id})

    @staticmethod
    def update_sandbox_keys(user_id, api_key, secret_key):
        app.db.client["client_app"].update_one(
            {"_id": user_id},
            {"$push": {"sandbox_keys": {"key": api_key, "secret": secret_key}}},
        )

    @staticmethod
    def insert_sandbox_keys(user_id, api_key, secret_key):
        app.db.client["client_app"].update_one(
            {"_id": user_id},
            {"$set": {"sandbox_keys": [{"key": api_key, "secret": secret_key}]}},
        )

    @staticmethod
    def update_live_keys(user_id, api_key, secret_key):
        app.db.client["client_app"].update_one(
            {"_id": user_id},
            {"$push": {"live_keys": {"key": api_key, "secret": secret_key}}},
        )

    @staticmethod
    def insert_live_keys(user_id, api_key, secret_key):
        app.db.client["client_app"].update_one(
            {"_id": user_id},
            {"$set": {"live_keys": [{"key": api_key, "secret": secret_key}]}},
        )

    @staticmethod
    def delete_sandbox_key(user_id, api_key, secret_key):
        return app.db.client["client_app"].update_one(
            {"_id": user_id},
            {"$pull": {"sandbox_keys": {"key": api_key, "secret": secret_key}}},
        )

    @staticmethod
    def delete_live_key(user_id, api_key, secret_key):
        return app.db.client["client_app"].update_one(
            {"_id": user_id},
            {"$pull": {"live_keys": {"key": api_key, "secret": secret_key}}},
        )
