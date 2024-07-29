from flask import jsonify
from ..auth.models import ClientApp
from .models import APIModel
from ..utils.api_handler import HMACHelper
from ..config import Config


class APIController:

    @staticmethod
    def home():
        return "Welcome to BioEntrust Auth server"

    @staticmethod
    def get_all_liveapi(client_id):
        document = APIModel.find_api_vault_by_id(client_id)
        if not document:
            return jsonify({"message": "User has no generated API key"}), 400
        return jsonify(document)

    @staticmethod
    def get_all_sandboxapi(client_id):
        document = APIModel.find_api_vault_by_id(client_id)
        if not document:
            return jsonify({"message": "User has no generated API key"}), 400
        return jsonify(document)

    @staticmethod
    def get_sandbox_api_logs(api_key):
        key = Config.SANDBOX_KEY
        helper = HMACHelper(key)
        logs = APIModel.find_api_logs_by_id(api_key)
        if logs:
            secret_key = logs["api_data"][0]["secret_key"]
            if helper.verify_key(api_key, secret_key):
                return jsonify(logs), 200
            return jsonify({"message": "Invalid API key, Use a Sandbox API key"}), 403
        return jsonify({"message": "No logs found for this API key"}), 404

    @staticmethod
    def get_live_api_logs(api_key):
        key = Config.LIVE_KEY
        helper = HMACHelper(key)
        logs = APIModel.find_api_logs_by_id(api_key)
        if logs:
            secret_key = logs["api_data"][0]["secret_key"]
            if helper.verify_key(api_key, secret_key):
                return jsonify(logs), 200
            return jsonify({"message": "Invalid API key, Use a Live API key"}), 403
        return jsonify({"message": "No logs found for this API key"}), 404

    @staticmethod
    def create_sandbox_key(user_id):
        key = Config.SANDBOX_KEY
        hmac_helper = HMACHelper(key)
        api_key, api_signature = hmac_helper.generate_key()
        secret_key = api_signature

        user = ClientApp.find_by_user_id(user_id)

        if not user:
            return jsonify({"status": "User not found"}), 404

        if "sandbox_keys" in user:
            APIModel.update_sandbox_keys(user_id, api_key, secret_key)
        else:
            APIModel.insert_sandbox_keys(user_id, api_key, secret_key)

        return (
            jsonify(
                {
                    "status": "Sandbox API key and secret key created and stored successfully",
                    "api_key": api_key,
                    "secret_key": secret_key,
                }
            ),
            201,
        )

    @staticmethod
    def create_live_key(user_id):
        key = Config.LIVE_KEY
        hmac_helper = HMACHelper(key)
        api_key, api_signature = hmac_helper.generate_key()
        secret_key = api_signature

        user = ClientApp.find_by_user_id(user_id)
        if not user:
            return jsonify({"status": "User not found"}), 404

        if "live_keys" in user:
            APIModel.update_live_keys(user_id, api_key, secret_key)
        else:
            APIModel.insert_live_keys(user_id, api_key, secret_key)

        return (
            jsonify(
                {
                    "status": "Live API key and secret key created and stored successfully",
                    "api_key": api_key,
                    "secret_key": secret_key,
                }
            ),
            201,
        )

    @staticmethod
    def delete_sandbox_key(user_id, api_key, secret_key):
        return APIController._delete_key(user_id, api_key, secret_key, "sandbox_keys")

    @staticmethod
    def delete_live_key(user_id, api_key, secret_key):
        return APIController._delete_key(user_id, api_key, secret_key, "live_keys")

    @staticmethod
    def _delete_key(user_id, api_key, secret_key, key_type):

        user = APIModel.find_by_user_id(user_id)
        response = {}

        if user:
            key_found = False
            for key_pair in user.get(key_type, []):
                if key_pair["key"] == api_key and key_pair["secret"] == secret_key:
                    key_found = True
                    break
            if key_found:
                result = (
                    APIModel.delete_sandbox_key(user_id, api_key, secret_key)
                    if key_type == "sandbox_keys"
                    else APIModel.delete_live_key(user_id, api_key, secret_key)
                )

                response["message"] = (
                    "API key and secret key deleted successfully"
                    if result.modified_count > 0
                    else "No keys were deleted"
                )
                response["status"] = 200 if result.modified_count > 0 else 500
            else:
                response["message"] = "Key pair not found"
                response["status"] = 400
        else:
            response["message"] = "User not found"
            response["status"] = 400

        return jsonify(response)
