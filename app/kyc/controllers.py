import uuid
import requests
from flask import jsonify
from models import UserModel, ClientAppModel, ServiceChargeModel, ClientUserModel
from ..utils import redis_client
# generate_otp # log_wallet_transaction, convert_and_upscale_image,
# send_sms_otp
from ..utils.wallet_handler import Wallet
from ..utils.image_handler import Images
from ..utils.otp_handler import send_sms
from ..config import Config
import face_recognition


class KYCController:
    @staticmethod
    def process_request(endpoint, data):
        sms_otp = redis_client.generate_otp()
        app_id = data.get("app_id")
        document = ClientAppModel.find_by_app_id(app_id)
        if not document:
            return jsonify({"error": "Invalid app_id"}), 400
        user_id = document["_id"]
        user = UserModel.find_by_id(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        old_wallet_balance = user["wallet"]
        service_charge = ServiceChargeModel.find_by_user_id(user_id)["service"]

        charge_amount = service_charge.get("kyc", 0)

        if old_wallet_balance < charge_amount:
            Wallet.transaction_log(
                user_id,
                f"Debit {endpoint}",
                charge_amount,
                old_wallet_balance,
                old_wallet_balance,
                "Failed (Insufficient funds)",
            )
            return jsonify({"message": "Insufficient funds"}), 403

        microservice_url = f"{Config.SERVICES}/{endpoint}"
        response = requests.post(microservice_url, json=data)

        if response.status_code != 200:
            return (
                jsonify(
                    {
                        "message": f"Microservice request failed with status code: {response.status_code}"
                    }
                ),
                400,
            )

        microservice_details = response.json()
        new_wallet_balance = old_wallet_balance - charge_amount

        Wallet.transaction_log(
            user_id,
            f"Debit {endpoint}",
            charge_amount,
            old_wallet_balance,
            new_wallet_balance,
            "Success",
        )
        UserModel.update_wallet(user_id, new_wallet_balance)

        document = ClientAppModel.find_by_app_id(app_id)
        new_request = {
            "_id": user_id,
            "user_id": microservice_details["data"]["_id"],
            "firstName": microservice_details["data"]["firstName"],
            "middleName": microservice_details["data"]["middleName"],
            "lastName": microservice_details["data"]["lastName"],
            "kyc_image": microservice_details["data"]["image"],
            "requestTime": microservice_details["data"]["requestTime"],
            "charges": charge_amount,
            "app_name": document["apps"][0].get("name"),
            "geolocation": data["geolocation"],
        }

        otp_request_id = uuid.uuid4().hex
        redis_client.hmset(f"new_request:{otp_request_id}", new_request)
        redis_client.expire(f"new_request:{otp_request_id}", 600)

        redis_client.set(f"{otp_request_id}", int(sms_otp), ex=600)

        phone_number = microservice_details["data"]["mobile"]
        res, code = send_sms(sms_otp, phone_number)

        if code != 200:
            return (
                jsonify(
                    {"error": "Something went wrong with sending the OTP. (Check Kudi)"}
                ),
                500,
            )

        return (
            jsonify(
                {
                    "success": "OTP sent!",
                    "status": "Success",
                    "otp_request_id": otp_request_id,
                    "det": microservice_details["data"],
                }
            ),
            200,
        )

    @staticmethod
    def process_facial_comparison(data):
        user_id = data.get("user_id")
        user = UserModel.find_by_id(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        old_wallet_balance = user["wallet"]
        charge_amount = ServiceChargeModel.find_by_user_id(
            user_id)["service"].get("kyc", 0)

        if old_wallet_balance < charge_amount:
            Wallet.transaction_log(
                user_id,
                "Debit facial_comparison",
                charge_amount,
                old_wallet_balance,
                old_wallet_balance,
                "Failed (Insufficient funds)",
            )
            return jsonify({"message": "Insufficient funds"}), 403

        client_user = ClientUserModel.find_by_user_id(data.get("user_id"))
        if not client_user:
            return jsonify({"error": "Client user not found"}), 404

        ClientUserModel.update_live_image(data.get("user_id"), data["image2"])

        face_recognition_face_encoding1 = Images.convert_and_upscale_image(
            data["image1"])
        face_recognition_face_encoding2 = Images.convert_and_upscale_image(
            requests.get(data["image2"]).content
        )

        try:
            encoding1 = face_recognition.face_encodings(
                face_recognition_face_encoding1
            )[0]
            encoding2 = face_recognition.face_encodings(
                face_recognition_face_encoding2
            )[0]
            distance = round(
                100 -
                face_recognition.face_distance(
                    [encoding1],
                    encoding2)[0] *
                100,
                2)
        except Exception as e:
            return jsonify({"error": "Invalid Image"}), 400

        if distance >= 52:
            return (
                jsonify(
                    {
                        "success": True,
                        "confidence_level": distance,
                        "balance": old_wallet_balance - charge_amount,
                        "live_image": data["image1"],
                        "kyc_image": data["image2"],
                    }
                ),
                200,
            )

        return (
            jsonify(
                {
                    "error": "Image doesn't match",
                    "confidence_level": distance,
                    "balance": old_wallet_balance - charge_amount,
                }
            ),
            400,
        )
