from random import randint
import os
from . import redis_client


class redis_handler:
    @staticmethod
    def generate_otp():
        otp = 0
        while len(str(otp)) < 4:
            otp = randint(0000, 9999)
        return otp

    @staticmethod
    def save_otp(otp_request_id, otp, user):
        redis_client.hmset(f"user:{otp_request_id}", user)
        redis_client.set(
            f"{otp_request_id}", int(otp), ex=600
        )  # 600 seconds = 10 minutes

    @staticmethod
    def get_otp(otp_request_id):
        return redis_client.get(f"{otp_request_id}")

    @staticmethod
    def get_user(otp_request_id):
        user = redis_client.hgetall(f"user:{otp_request_id}")
        return {k.decode("utf-8"): v.decode("utf-8") for k, v in user.items()}

    @staticmethod
    def delete_otp(otp_request_id):
        redis_client.delete(f"{otp_request_id}")

    @staticmethod
    def delete_user(otp_request_id):
        redis_client.delete(f"user:{otp_request_id}")
