from flask import jsonify
from flask_mail import Message
from . import mail
from ..config import Config

class otp_handler:

    @staticmethod
    def send_otp(otp, user_email):
            msg = Message(subject="OTP: Verify your Email", sender=Config.MAIL_DEFAULT_SENDER , recipients=[user_email])
            msg.body = str(otp)
            mail.send(msg)
            return jsonify({"message": "OTP sent!"}), otp

    @staticmethod
    def send_email(subject, sender, recipients, text_body, html_body):
        msg = Message(subject, sender=sender , recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)
