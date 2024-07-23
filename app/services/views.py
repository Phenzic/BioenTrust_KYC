
from flask import Blueprint, request
from .controllers import ServiceController

api = Blueprint('api', __name__)


@api.route('/get_user_details', methods=['POST'])
def get_user_details():
    client_user_id = request.json["client_user_id"]
    return ServiceController.get_user_details(client_user_id)


@api.route('/bvn_verification', methods=['POST'])
def bvn_verification():
    return ServiceController.bvn_verification()


@api.route('/vnin_verification', methods=['POST'])
def vnin_verification():
    return ServiceController.vnin_verification()


@api.route('/nin_verification', methods=['POST'])
def nin_verification():
    return ServiceController.nin_verification()


@api.route('/ip_verification', methods=['POST'])
def ip_verification():
    return ServiceController.ip_verification()


@api.route('/ad_phone_verification', methods=['POST'])
def ad_phone_verification():
    return ServiceController.ad_phone_verification()


@api.route('/facial_comparison', methods=['POST'])
def facial_comparison():
    return ServiceController.facial_comparison()


@api.route('/cac', methods=['POST'])
def cac():
    return ServiceController.cac()
