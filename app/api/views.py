from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .controllers import APIController

sandbox = Blueprint('sandbox', __name__)
live = Blueprint('live', __name__)


@sandbox.route('/get_all_api')
@jwt_required()
def get_all_liveapi():
    client_id = get_jwt_identity()
    return APIController.get_all_liveapi(client_id)


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
    return APIController.delete_key(
        user_id, api_key, secret_key, "sandbox_keys")


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
    return APIController.delete_key(user_id, api_key, secret_key, "live_keys")
