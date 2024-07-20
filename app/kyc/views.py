# views.py
from flask import Blueprint, request, jsonify
from controllers import KYCController

kyc_bp = Blueprint("kyc", __name__)


@kyc_bp.route("/api/<endpoint>", methods=["POST"])
def kyc_microservice(endpoint):
    data = request.get_json()
    if endpoint == "facial_comparison":
        return KYCController.process_facial_comparison(data)
    return KYCController.process_request(endpoint, data)
