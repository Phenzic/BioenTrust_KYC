import datetime
from .models import User, ClientApp, ServiceCharge, TokenBlocklist, EmailService
from flask import jsonify, render_template, request
import uuid
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from ..utils.redis_handler import redis_handler
from ..utils.otp_handler import otp_handler
from .models import ClientUser
from ..config import Config
from app.utils.token_handler import is_refresh_token_revoked, is_access_token_revoked


class AuthController:
    @staticmethod
    def home():
        return "Welcome to BioEntrust Auth server"

    @staticmethod
    def signup(request):
        user = {
            "_id": uuid.uuid4().hex,
            "first_name": request.json["first_name"],
            "last_name": request.json["last_name"],
            "email": request.json["email"],
            "password": pbkdf2_sha256.hash(
                request.json["password"]
            ),
            "wallet": 0,
        }

        if User.find_by_email(user["email"]):
            return jsonify({"error": "Email address already in use"}), 409

        password = request.json["password"]
        if len(password) < 8:
            return jsonify(
                {"error": "Password should be more than 7 characters"}), 400

        new_user = User(**user)
        otp_request_id = uuid.uuid4().hex
        email_otp = redis_handler.generate_otp()
        redis_handler.save_otp(otp_request_id, email_otp, new_user.to_dict())
        otp_handler.send_otp(email_otp, user["email"])

        return jsonify(
            {"otp_request_id": otp_request_id, "response": "otp sent"})

    @staticmethod
    def verify_email(request):
        user_otp = request.json["otp"]
        otp_request_id = request.json["otp_request_id"]

        email_otp = redis_handler.get_otp(otp_request_id)
        if int(email_otp) == int(user_otp):
            user_data = redis_handler.get_user(otp_request_id)
            new_user = User(**user_data)
            redis_handler.delete_otp(otp_request_id)
            redis_handler.delete_user(otp_request_id)

            new_user.save_to_db()
            client_app = ClientApp(new_user._id)
            service_charge = ServiceCharge(new_user._id, new_user.email)

            client_app.save_to_db()
            service_charge.save_to_db()

            access_token = create_access_token(identity=new_user._id)
            refresh_token = create_refresh_token(identity=new_user._id)

            return (jsonify({"message": "Logged In", "token": {
                "access": access_token, "refresh": refresh_token}, }), 200, )
        else:
            return jsonify({"error": "Signup Failed"}), 401

    @staticmethod
    def signin(request):
        email = request.json["email"]
        password = str(request.json["password"])
        user = User.find_by_email(email)
        if not user:
            return jsonify({"error": "email not registered"}), 401

        if user and pbkdf2_sha256.verify(password, user["password"]):
            access_token = create_access_token(identity=user["_id"])
            refresh_token = create_refresh_token(identity=user["_id"])
            return (jsonify({"message": "Logged In", "token": {
                "access": access_token, "refresh": refresh_token}, }), 200, )

        return jsonify({"error": "Invalid login credentials"}), 401

    @staticmethod
    def verify_sms(request):
        app_id = request.json["app_id"]
        document = ClientApp.find_by_app_id(app_id)
        user_otp = request.json["otp"]
        otp_request_id = request.json["otp_request_id"]

        sms_otp = redis_handler.get_otp(otp_request_id)
        new_request = redis_handler.get_new_request(otp_request_id)

        if int(sms_otp) == int(user_otp):
            new_request["status"] = "Success"
            new_request["status_description"] = "Phone Number Verified"
            new_request["requestTime"] = datetime.strptime(
                new_request["requestTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )

            ClientUser.insert_new_request(new_request)

            redis_handler.delete_otp(otp_request_id)
            redis_handler.delete_new_request(otp_request_id)

            user_details = ClientUser.get_user_details(new_request["user_id"])

            return (
                jsonify(
                    {
                        "success": "you've been verified!",
                        "user_detail": user_details,
                        "geolocation": new_request["geolocation"],
                    }
                ),
                200,
            )
        else:
            new_request["status"] = "Error"
            new_request["status_description"] = "Could not verify phone number"
            new_request["requestTime"] = datetime.strptime(
                new_request["requestTime"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            ClientUser.insert_new_request(new_request)
            return jsonify({"error": "Invalid OTP key"}), 400

    @staticmethod
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        return TokenBlocklist.is_token_revoked(jti)

    @staticmethod
    @jwt_required(refresh=True)
    @is_refresh_token_revoked
    def signout():
        token = get_jwt()
        jti = token["jti"]
        ttype = token["type"]
        TokenBlocklist.add_to_blocklist(jti, Config.ACCESS_EXPIRES)
        return jsonify(
            msg=f"{ttype.capitalize()} token successfully revoked"), 200

    @staticmethod
    @jwt_required(refresh=True)
    @is_refresh_token_revoked
    def refresh_access():
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        return jsonify({"access": new_access_token})

    @staticmethod
    def forgot_password():
        email = request.json["email"]
        url = request.host_url + "reset-password/"

        client = User.find_by_email(email)
        if not client:
            return jsonify({"error": "Invalid email"}), 400

        client_id = client["_id"]
        expires = datetime.timedelta(hours=1)
        new_access_token = create_access_token(
            identity=client_id, expires_delta=expires
        )

        EmailService.send_password_reset(
            email,
            "Reset Your Password",
            "mlsayabatech@gmail.com",
            [email],
            render_template(
                "email/reset_password.txt",
                url=url + new_access_token,
                name=client["first_name"],
            ),
            render_template(
                "email/reset_password.html",
                url=url + new_access_token,
                name=client["first_name"],
            ),
        )

        return jsonify(
            {"message": "Password reset link sent to your email"}), 200

    @staticmethod
    @jwt_required()
    @is_access_token_revoked
    def reset_password():
        user_id = get_jwt_identity()
        try:
            # client_id = decode_token(token)['sub']
            user = User.find_by_id(user_id)

            if user:
                new_password = request.json["password"]
                User.update_password(user_id, new_password)
                return jsonify({"message": "Password reset successful"}), 200
            else:
                return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 400



