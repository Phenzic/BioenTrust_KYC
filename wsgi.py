from app import create_app
from flask import jsonify

app = create_app()


@app.route("/", methods=["GET"])
def home():
    try:
        response_message = {
            "status": "Running Successfully...",
            "message": "https://docs.bioentrust.com",
            "new_data": "Welcome to BioEntrust Auth server",
        }
        return jsonify(response_message), 200

    except Exception as e:
        error_message = {"status": "error", "message": str(e)}
        return jsonify(error_message), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=True)
