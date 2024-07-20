from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from . import redis_client


def is_refresh_token_revoked(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request(refresh=True)
        jti = get_jwt()["jti"]
        if redis_client.get(jti) is not None:
            return jsonify({"msg": "Token has been revoked"}), 401
        return fn(*args, **kwargs)
    return wrapper


def is_access_token_revoked(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        jti = get_jwt()["jti"]
        if redis_client.get(jti) is not None:
            return jsonify({"msg": "Token has been revoked"}), 401
        return fn(*args, **kwargs)
    return wrapper
