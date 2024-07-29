from flask import jsonify, request
from flask_jwt_extended import (
    get_jwt,
    create_access_token,
    create_refresh_token,
)
from passlib.hash import pbkdf2_sha256
import uuid
import datetime
from .models import AdminModel


class AdminController:

    @staticmethod
    def admin_refresh_access():
        jwt = get_jwt()
        if "sub" not in jwt:
            return jsonify({"msg": "Invalid token"}), 401

        identity = jwt["sub"]
        role = jwt["role"]
        new_access_token = create_access_token(
            identity=identity, additional_claims={"role": role}
        )

        return jsonify({"access": new_access_token})

    @staticmethod
    def admin_register():
        try:
            name = request.json["name"]
            email = request.json["email"]
            password = request.json["password"]
            admin = AdminModel.find_by_email(email)

            if admin:
                return jsonify({"error": "User already exists"}), 400

            hashed_password = pbkdf2_sha256.hash(password)
            new_admin = {
                "_id": str(uuid.uuid4()),
                "name": name,
                "email": email,
                "password": hashed_password,
                "created_at": datetime.datetime.now(),
            }
            AdminModel.add_new_admin(new_admin)
            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def admin_login():
        try:
            email = request.json["email"]
            password = request.json["password"]
            admin = AdminModel.find_by_email(email)

            if not admin:
                return jsonify({"error": "User not found"}), 401

            if admin and pbkdf2_sha256.verify(password, admin["password"]):
                access_token = create_access_token(
                    identity=admin["_id"], additional_claims={"role": "admin"}
                )
                refresh_token = create_refresh_token(
                    identity=admin["_id"], additional_claims={"role": "admin"}
                )
                return (
                    jsonify(
                        {
                            "message": "Logged In",
                            "token": {"access": access_token, "refresh": refresh_token},
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Invalid email or password"}), 401
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def admin_dashboard():
        verifications = AdminModel.get_all_client_users
        verifications = list(verifications)

        failed_verifications = [x for x in verifications if x["status"] == "Failed"]
        successful_verifications = [
            x for x in verifications if x["status"] == "Success"
        ]

        results = {
            "Total": len(list(verifications)),
            "Failed": len(failed_verifications),
            "Success": len(successful_verifications),
        }

        return jsonify(results)

    @staticmethod
    def admin_dashboard_date():
        pipeline = [
            {
                "$project": {
                    "date": {
                        "$dateToString": {"format": "%Y-%m-%d", "date": "$requestTime"}
                    },
                    "status": "$status",
                }
            },
            {
                "$group": {
                    "_id": {"date": "$date", "status": "$status"},
                    "count": {"$sum": 1},
                }
            },
            {
                "$group": {
                    "_id": "$_id.date",
                    "status_counts": {
                        "$push": {"status": "$_id.status", "count": "$count"}
                    },
                }
            },
            {"$sort": {"_id": 1}},
        ]

        results = AdminModel.aggregator(pipeline)
        results = list(results)

        results = {
            i["_id"]: {
                "Success": 0,
                "Failed": 0,
                **{j["status"]: j["count"] for j in i["status_counts"]},
            }
            for i in results
        }

        return jsonify(results)

    @staticmethod
    def get_client_details():
        try:
            client_profiles = AdminModel.find_user()
            data = list(client_profiles) if client_profiles else []
            return jsonify(data)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def get_service_price():
        client_id = request.json["client_id"]
        try:
            service_charge = AdminModel.get_charges_by_id(client_id)
            if service_charge:
                return jsonify(service_charge)
            else:
                return jsonify({"error": "Client not found"}), 404
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def set_service_price():
        client_id = request.json["client_id"]
        services = request.json["services"]
        try:
            new_user_service_charge = {
                "$set": {"service." + k: v for k, v in services.items()}
            }

            AdminModel.update_carges(client_id, new_user_service_charge)
            service_charge = AdminModel.get_charges_by_id(client_id)
            return jsonify(service_charge)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def wallet_logs():
        client_id = request.json["client_id"]
        try:
            wallet_logs = AdminModel.find_transaction_by_id(client_id)
            data = list(wallet_logs)[::-1] if wallet_logs else []
            return jsonify(data)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @staticmethod
    def user_role_distribution():
        try:
            clients = AdminModel.find_user()
            unique_verifications = AdminModel.find_distinct()
            admin = AdminModel.find_admin()

            results = {
                "clients": len(list(clients)),
                "end_users": len(unique_verifications),
                "admin": len(list(admin)),
            }
            return jsonify(results)
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
