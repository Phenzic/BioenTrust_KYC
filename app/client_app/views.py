
from flask import Blueprint, jsonify
from .controllers import AppController

c_app = Blueprint("app", __name__)


@c_app.route("/home", methods=["GET"])
def home():
    try:
        new_data = AppController.home()
        response_message = {
            "new_data": str(new_data),
        }
        print(new_data)
        return jsonify(response_message), 200

    except Exception as e:
        error_message = {"status": "error", "message": str(e)}
    return jsonify(error_message), 500


@c_app.route('/create-app', methods=['POST'])
def create_app():
    return AppController.create_app()
