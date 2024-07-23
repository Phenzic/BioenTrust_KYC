
import uuid
from .models import AppModel
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..utils.token_handler import is_access_token_revoked


class AppController:

    @staticmethod
    def home():
        return "Welcome to BioEntrust Auth server"

    @staticmethod
    @jwt_required()
    @is_access_token_revoked
    def create_app():

        user_id = get_jwt_identity()
        app_data = {
            "app_id": uuid.uuid4().hex,
            "name": request.json["name"],
            "color": request.json["color"],
            "date_of_creation": request.json["date_of_creation"],
            "verification": request.json["verification"],
            "user_information": request.json["user_information"],
            "on_verification": request.json["on_verification"],
            "redirect_url": request.json["redirect_url"]
        }

        user = AppModel.find_by_user_id(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        result = AppModel.create_app(app_data, user_id)

        if result.modified_count == 0:
            return jsonify({"error": "Failed to add app to user"}), 500

        return jsonify({"status": "App added successfully",
                       "app_id": app_data["app_id"]}), 201
