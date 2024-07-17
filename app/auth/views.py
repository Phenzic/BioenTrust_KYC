from flask import Blueprint, request, jsonify
from .controllers import AuthController 
from . import auth

@auth.route("/", methods=["GET"])
def home():
    try:
        new_data = AuthController.home()
        response_message = {
            "status": "Running Successfully...",
            "message": "https://docs.bioentrust.com",
            "new_data": str(new_data),
        }
        print(new_data)
        return jsonify(response_message), 200

    except Exception as e:
        error_message = {"status": "error", "message": str(e)}
        return jsonify(error_message), 500


@auth.route("/signup", methods=["POST"])
def signup():
    return AuthController.signup(request)

@auth.route("/verify-email", methods=["POST"])
def verify_email():
    return AuthController.verify_email(request)


@auth.route("/signin", methods=["POST"])
def signin():
    return AuthController.signin(request)

