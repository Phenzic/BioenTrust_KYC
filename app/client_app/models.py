from flask import current_app as app

class AppModel:

    @staticmethod
    def find_by_user_id(user_id):
        return app.db.client["client_app"].find_one({"_id": user_id})
    
    @staticmethod
    def create_app(app_data, user_id):
        result = app.db.client["client_app"].update_one(
            {"_id": user_id},
            {"$push": {"apps": app_data}}
        )
        return result
