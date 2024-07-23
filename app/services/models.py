from pymongo import MongoClient
from flask import current_app as app


class ServiceModel:

    @staticmethod
    def insert_one(data):
        return app.db.user_vault["vault"].insert_one(data)
    
    @staticmethod
    def find_user_by_id(user_id):
        return app.db.users.find_one({"id": user_id}, {"_id": 0})
    @staticmethod
    def find_data_by_bvn(bvn):
        return app.db.user_vault["vault"].find_one({"idNumber": bvn})
    @staticmethod
    def find_data_by_id(id_number):
        return app.db.user_vault["vault"].find_one({"idNumber": id_number})
    
    @staticmethod
    def find_data_by_reg_num(cac):
        return app.db.user_vault["vault"].find_one({"registrationNumber": cac})    

    @staticmethod
    def insert_data(data):
        app.db.user_vault["vault"].insert_one(data)
