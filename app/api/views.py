from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .controllers import APIController

sandbox = Blueprint('sandbox', __name__)
live = Blueprint('live', __name__)

@sandbox.route("/", methods=["GET"])
@live.route("/", methods=["GET"])
def home():
    try:
        new_data = APIController.home
        response_message = {
            "new_data": str(new_data),
        }
        print(new_data)
        return jsonify(response_message), 200

    except Exception as e:
        error_message = {"status": "error", "message": str(e)}
    return jsonify(error_message), 500


@live.route('/get_all_api/<client_id>')
@jwt_required()
def get_all_liveapi():
    client_id = get_jwt_identity()
    return APIController.get_all_liveapi(client_id)

@sandbox.route('/get_all_api/<client_id>')
@jwt_required()
def get_all_sandboxapi():
    client_id = get_jwt_identity()
    return APIController.get_all_sandboxapi(client_id)


@sandbox.route('/create-key')
@jwt_required()
def create_sandbox_key():
    user_id = get_jwt_identity()
    return APIController.create_sandbox_key(user_id)

@sandbox.route("get-api/<api_key>")
def get_sandbox_api_logs(api_key):
    return APIController.get_sandbox_api_logs(api_key)


@sandbox.route("/delete-key", methods=["DELETE"])
@jwt_required()
def delete_sandbox_key():
    user_id = get_jwt_identity()
    api_key = request.json["api"]
    secret_key = request.json['secret']
    return APIController.delete_sandbox_key(
        user_id, api_key, secret_key)


@live.route('/create-key')
@jwt_required()
def create_live_key():
    user_id = get_jwt_identity()
    return APIController.create_live_key(user_id)

@live.route("get-api/<api_key>")
def get_live_api_logs(api_key):
    return APIController.get_live_api_logs(api_key)

@live.route("/delete-key", methods=["DELETE"])
@jwt_required()
def delete_live_key():
    user_id = get_jwt_identity()
    api_key = request.json["api"]
    secret_key = request.json['secret']
    return APIController.delete_live_key(user_id, api_key, secret_key)
