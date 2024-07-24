from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


def admin_required(refresh=False):
    def decorator(func):
        @wraps(func)
        @jwt_required(refresh=refresh)
        def wrapper(*args, **kwargs):
            jwt = get_jwt_identity()
            try:
                if jwt["role"] != "admin":
                    return jsonify({"msg": "Admin role required"}), 403
                if refresh and jwt["type"] != "refresh":
                    return jsonify({"msg": "Refresh token required"}), 403
            except KeyError:
                return jsonify({"msg": "Admin role required"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
