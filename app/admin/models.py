from flask import current_app as app


class AdminModel:

    @staticmethod
    def find_by_email(email):
        return app.db.admin["admin_data"].find_one({"email": email})

    @staticmethod
    def add_new_admin(new_admin):
        return app.db.admin["admin_data"].insert(new_admin)

    @staticmethod
    def get_all_client_users():
        return app.db.client["client_user"].find()

    @staticmethod
    def aggregator(pipeline):
        return app.db.client["client_user"].aggregate(pipeline)

    @staticmethod
    def find_user():
        return app.db.users["user"].find()

    @staticmethod
    def get_charges_by_id(client_id):
        db = app.db.users
        return db["service_charges"].find_one({"_id": client_id})

    @staticmethod
    def update_carges(client_id, new_user_service_charge):
        db = app.db.users
        return db["service_charges"].update_one(
            {"_id": client_id}, new_user_service_charge
        )

    @staticmethod
    def find_transaction_by_id(client_id):
        db = app.db.wallet
        return db["transactions"].find_one({"user_id": client_id})

    @staticmethod
    def find_distinct():
        return app.db.client["client_user"].find().distinct("user_id")

    @staticmethod
    def find_admin():
        return app.db.admin["admin_data"].find()
