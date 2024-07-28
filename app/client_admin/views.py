from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .controllers import ClientAdminController

client_admin = Blueprint('client_admin', __name__)

@client_admin.route('/<endpoint>')
@jwt_required()
def admin_websocket(endpoint):
    return ClientAdminController.admin_websocket(endpoint)



@client_admin.route('/get-user-details', methods=['POST'])
@jwt_required()
def get_user_details():
    return ClientAdminController.get_user_details(request)



@client_admin.route('/dashboard/all-data', methods=['GET'])
@jwt_required()
def dashboard():
    return ClientAdminController.dashboard()

@client_admin.route('/dashboard/all-data-with-date', methods=['GET'])
@jwt_required()
def dashboard_date():
    return ClientAdminController.dashboard_date()


@client_admin.route("/get-app", methods=["POST"])
def get_app():
    return ClientAdminController.get_app(request)

@client_admin.route("delete-app", methods=["DELETE"])
@jwt_required()
def delete_app():
    return ClientAdminController.delete_app(request)

@client_admin.route('/update-app', methods=['PUT'])
@jwt_required()
def update_user_details():
    return ClientAdminController.update_app(request)

@client_admin.route("/fund", methods=["POST"])
@jwt_required()
def fund_wallet():
    return ClientAdminController.fund_wallet(request)

@client_admin.route("/get-wallet-transactions", methods=["GET"])
@jwt_required()
def get_wallet_transactions():
    user_id = get_jwt_identity()
    return ClientAdminController.get_wallet_transactions(user_id)


@client_admin.route("/get-client-profile", methods=["GET"])
@jwt_required()
def get_client_profile():
    client_id = get_jwt_identity()
    return ClientAdminController.get_client_profile(client_id)

