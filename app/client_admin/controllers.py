from flask import Blueprint, jsonify, request, after_this_request
from flask import current_app as app
from flask_jwt_extended import get_jwt_identity

from ..utils.wallet_handler import Wallet
from .models import ClientAdminModels


class ClientAdminController:

    @staticmethod
    def admin_websocket(endpoint):
        client_id = get_jwt_identity()
        try:
            data = {}
            client_profile = ClientAdminModels.get_client_profile(client_id)
            client_data = app.db.client_user.find_one({"user_id": client_id})
            client_user_data = ClientAdminModels.get_client_user_data(
                client_id)
            charges_data = ClientAdminModels.get_service_charge(client_id)

            if endpoint == "verifications":
                data = client_user_data
            elif endpoint == "get_all_apps":
                data = client_data["apps"]
            elif endpoint == "profile":
                data = client_profile
            elif endpoint == "charges":
                data = charges_data
            else:
                return jsonify({"error": "Endpoint does not exist"}), 404

            return jsonify(data), 200

        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def get_user_details(request):
        client_user_id = request.json['user_id']
        client_user = app.db.vaults["vault"].find_one(
            {"user_id": client_user_id})
        return jsonify(
            {"user_data": ClientAdminModels.get_user_details(client_user_id)})

    @staticmethod
    def update_app():
        client_id = get_jwt_identity()
        user_id = request.json['user_id']
        new_status = request.json['status']
        new_status_description = request.json['status_description']
        ClientAdminModels.update_client_user_status(
            client_id, user_id, new_status, new_status_description)
        client_profile = ClientAdminModels.get_client_profile(client_id)
        return jsonify(client_profile)

    @staticmethod
    def dashboard():
        client_id = get_jwt_identity()
        pipeline = [
            {"$match": {"_id": client_id}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        result = list(app.db.client["client_user"].aggregate(pipeline))
        result = {i["_id"]: i["count"] for i in result}
        result = {"Total": 0, "Success": 0, "Failed": 0, **result}
        result["Total"] = sum(result.values())
        return jsonify(result)

    @staticmethod
    def get_wallet_transactions(user_id):
        return ClientAdminModels.get_wallet_transactions(user_id)

    @staticmethod
    def fund_wallet(request):
        client_id = get_jwt_identity()
        user = app.db.users["user"].find_one({"_id": client_id})
        transaction_amount = request.json["amount"]
        old_wallet_balance = {"wallet": user["wallet"]}
        new_wallet_balance = int(
            old_wallet_balance["wallet"]) + int(transaction_amount)

        new_wallet_balance = {"$set": {"wallet": new_wallet_balance}}

        try:
            Wallet.transaction_log(
                client_id,
                "fund",
                transaction_amount,
                old_wallet_balance["wallet"],
                new_wallet_balance["$set"]["wallet"],
                "Success")
        except BaseException:
            Wallet.transaction_log(
                client_id,
                "fund",
                transaction_amount,
                old_wallet_balance,
                new_wallet_balance,
                "Failed")

        app.db.users["user"].update_one({"_id": client_id}, new_wallet_balance)
        # Wallet["user"].update_one({"_id": client_id}, new_wallet_balance)
        user = app.db.users["user"].find_one({"_id": client_id})

        return user

    @staticmethod
    def dashboard_date():
        client_id = get_jwt_identity()
        pipeline = [
            {
                "$match": {
                    "_id": client_id}}, {
                "$project": {
                    "date": {
                        "$dateToString": {
                            "format": "%Y-%m-%d", "date": "$requestTime"}}, "status": "$status"}}, {
                                "$group": {
                                    "_id": {
                                        "date": "$date", "status": "$status"}, "count": {
                                            "$sum": 1}}}, {
                                                "$group": {
                                                    "_id": "$_id.date", "status_counts": {
                                                        "$push": {
                                                            "status": "$_id.status", "count": "$count"}}}}]
        result = list(app.db.client["client_user"].aggregate(pipeline))
        result = {i["_id"]: {"Success": 0, "Failed": 0, **{j["status"]
            : j["count"] for j in i["status_counts"]}} for i in result}
        return jsonify(result)

    @staticmethod
    def delete_app(request):
        client_id = get_jwt_identity()
        desired_app_id = request.json["app_id"]

        # Update operation using $pull
        update_query = {"$pull": {"apps": {"app_id": desired_app_id}}}

        app.db.client["client_app"].update_one(
            {"_id": client_id}, update_query)

        client_apps_details = app.db.client["client_app"].find_one(
            {"_id": client_id})

        return jsonify(client_apps_details)

    @staticmethod
    def get_app(requests):
        app_id = requests.json["app_id"]
        return ClientAdminModels.get_app_by_id(app_id)

    @staticmethod
    def get_client_profile(client_id):
        # app_id = request.json["app_id"]
        return ClientAdminModels.get_client_profile(client_id)
