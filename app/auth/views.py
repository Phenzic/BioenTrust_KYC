from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager
from .controllers import AuthController

jwt = JWTManager()

auth = Blueprint("user", __name__)


@auth.route("/home", methods=["GET"])
def home():
    try:
        new_data = AuthController.home()
        response_message = {
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


@auth.route("/verify-sms", methods=["POST"])
def validate_sms_otp():
    return AuthController.validate_sms_otp(request)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    return AuthController.check_if_token_is_revoked(jwt_header, jwt_payload)


@auth.route("/logout", methods=["DELETE"])
def logout():
    return AuthController.logout()


@auth.route("/refresh", methods=["POST"])
def refresh_access():
    return AuthController.refresh_access()


@auth.route('/forgot-password', methods=["POST"])
def forgot_password():
    return AuthController.forgot_password()


@auth.route('/reset-password/<token>', methods=["GET", "POST"])
def reset_password(token):
    return AuthController.reset_password(token)
