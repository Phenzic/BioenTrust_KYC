from .models import User, ClientApp, ServiceCharge
from flask import jsonify
import uuid
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token
from ..utils.redis_handler import redis_handler
from ..utils.otp_handler import otp_handler

class AuthController:
    @staticmethod
    def home():
        return("Welcome to BioEntrust Auth server")
    
    @staticmethod
    def signup(request):
        user = {
            "_id": uuid.uuid4().hex,
            "first_name": request.json["first_name"],
            "last_name": request.json["last_name"],
            "email": request.json["email"],
            "password": request.json["password"],
            "wallet": 0
        }

        if User.find_by_email(user["email"]):
            return jsonify({"error": "Email address already in use"}), 409
        
        password = str(user['password'])        
        if len(password) < 8:
            return jsonify({"error": "Password should be more than 7 characters"}), 400

        new_user = User(**user)
        otp_request_id = uuid.uuid4().hex
        email_otp = redis_handler.generate_otp()
        redis_handler.save_otp(otp_request_id, email_otp, new_user.to_dict())
        otp_handler.send_otp(email_otp, user["email"])

        return jsonify({
            "otp_request_id": otp_request_id,
            "response": "otp sent"
        })

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

            return jsonify(
                {
                    "message": "Logged In",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                    }
                }
            ), 200
        else:
            return jsonify({"error": "Signup Failed"}), 401


    @staticmethod
    def signin(request):
        email = request.json["email"]
        password = str(request.json["password"])
        user = User.find_by_email(email)
        print(pbkdf2_sha256.verify(password, user["password"]))
        if user and pbkdf2_sha256.verify(password, user["password"]):
            print("yes")
            access_token = create_access_token(identity=user["_id"])
            refresh_token = create_refresh_token(identity=user["_id"])
            return jsonify(
                {
                    "message": "Logged In",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token
                        }
                }
            ), 200
            
        return jsonify({"error": "Invalid login credentials"}), 401
