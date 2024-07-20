from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import APIController

sandbox = Blueprint('sandbox_api', __name__)
live = Blueprint('live_api', __name__)


@sandbox.route('/get_all_api')
@jwt_required()
def get_all_liveapi():
    client_id = get_jwt_identity()
    return APIController.get_all_liveapi(client_id)


@live.route("get_api/<api_key>")
def get_live_api_logs(api_key):
    return APIController.get_api_logs(api_key, "API_LIVE_KEY")


@sandbox.route("get_api/<api_key>")
def get_sandbox_api_logs(api_key):
    return APIController.get_api_logs(api_key, "API_SANDBOX_KEY")


@sandbox.route('/create_sandbox_key')
@jwt_required()
def create_sandbox_key():
    user_id = get_jwt_identity()
    return APIController.create_key(user_id, "API_SANDBOX_KEY", "sandbox_keys")


@live.route('/create_live_key')
@jwt_required()
def create_live_key():
    user_id = get_jwt_identity()
    return APIController.create_key(user_id, "API_LIVE_KEY", "live_keys")


@sandbox.route("/delete_sandbox_api", methods=["DELETE"])
@jwt_required()
def delete_sandbox_key():
    user_id = get_jwt_identity()
    api_key = request.json["api"]
    secret_key = request.json['secret']
    return APIController.delete_key(
        user_id, api_key, secret_key, "sandbox_keys")


@live.route("/delete_live_api", methods=["DELETE"])
@jwt_required()
def delete_live_key():
    user_id = get_jwt_identity()
    api_key = request.json["api"]
    secret_key = request.json['secret']
    return APIController.delete_key(user_id, api_key, secret_key, "live_keys")
