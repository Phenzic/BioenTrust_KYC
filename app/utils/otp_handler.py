import requests
from flask import jsonify
from flask_mail import Message
from . import mail
from ..config import Config


class otp_handler:

    @staticmethod
    def send_otp(otp, user_email):
        msg = Message(
            subject="OTP: Verify your Email",
            sender=Config.MAIL_DEFAULT_SENDER,
            recipients=[user_email],
        )
        msg.body = str(otp)
        mail.send(msg)
        return jsonify({"message": "OTP sent!"}), otp

    @staticmethod
    def send_email(subject, sender, recipients, text_body, html_body):
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)


def send_sms(otp, client_phone_number):
    param = {
        "token": "x79ZY4haVk61uEdX2Ivm0HKSjqAFRgLfWnsoTBODtUiNyp5QMz3Jw8blGcPreC",
        "senderID": "bioentrust",
        "recipients": f"{client_phone_number}",
        "otp": f"{otp}",
        "appnamecode": "8316644185",
        "templatecode": "9854674317",
    }

    response = requests.post(url="https://my.kudisms.net/api/otp", json=param)
    if response.status_code != 200:
        return jsonify({"error": "Something went wrong!"}
                       ), response.status_code

    return jsonify({"success": response.text}), response.status_code
