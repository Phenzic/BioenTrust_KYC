from app import create_app
from flask import jsonify
from .app.auth.controllers import AuthController



app = create_app()


@app.route("/", methods=["GET"])
def home():
    try:
        new_data = AuthController.home()
        response_message = {
            "status": "Running Successfully...",
            "message": "https://docs.bioentrust.com",
            "new_data": str(new_data),
        }
        print(new_data)
        return jsonify(response_message), 200

    except Exception as e:
        error_message = {"status": "error", "message": str(e)}
        return jsonify(error_message), 500
    

if __name__ == "__main__":
    app.run(host="0.0.0.0")
