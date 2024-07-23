from flask import jsonify, request
import requests
import jsonpickle
from datetime import datetime
from .models import ServiceModel
from ..config import Config

youverify = Config.YOUVERIFY_BASE
token = Config.YOUVERIFY_TOKEN


class ServiceController:

    @staticmethod
    def get_user_details(client_user_id):
        user_detail = ServiceModel.find_user_by_id(client_user_id)
        if user_detail:
            return jsonify({"user_detail": user_detail}), 200
        else:
            return jsonify(
                {"error": "Something went wrong! Confirm if user exists!"}), 404

    @staticmethod
    def bvn_verification():
        try:
            bvn = request.json["bvn"]
            existing_data = ServiceModel.find_data_by_bvn(bvn)

            if existing_data:
                response_data = {
                    "data": {
                        "_id": existing_data["id"],
                        "firstName": existing_data['firstName'],
                        "middleName": existing_data['middleName'],
                        "lastName": existing_data['lastName'],
                        "image": existing_data["image"],
                        "status": existing_data["status"],
                        "mobile": existing_data["mobile"],
                        "requesTime": datetime.utcnow().isoformat(),
                    },
                }
                return jsonpickle.encode(response_data), 200

            data = {
                "id": bvn,
                "isSubjectConsent": True,
            }
            if "image" in request.json:
                data["validations"] = {
                    "selfie": {"image": request.json["image"]}
                }
            if all(
                field in request.json for field in [
                    "firstName",
                    "lastName",
                    "dateOfBirth"]):
                data.setdefault("validations", {})["data"] = {
                    "firstName": request.json["firstName"],
                    "lastName": request.json["lastName"],
                    "dateOfBirth": request.json["dateOfBirth"],
                }
            if request.json.get("shouldRetrieveBVN"):
                data["shouldRetrieveBVN"] = True
            if request.json.get("premiumBVN"):
                data["premiumBVN"] = True

            url = f"{youverify}/v2/api/identity/ng/bvn"
            headers = {
                'Content-Type': 'application/json',
                'token': token
            }
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()

            if response_data["data"]["status"] == "found":
                ServiceModel.insert_data(response_data["data"])

            new_entry = ServiceModel.find_data_by_bvn(bvn)
            response_data = {
                "data": {
                    "_id": new_entry["id"],
                    "firstName": new_entry['firstName'],
                    "middleName": new_entry['middleName'],
                    "lastName": new_entry['lastName'],
                    "image": new_entry["image"],
                    "status": new_entry["status"],
                    "mobile": new_entry["mobile"],
                    "requesTime": datetime.utcnow().isoformat(),
                },
            }
            return jsonpickle.encode(response_data), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def vnin_verification():
        try:
            vnin = request.json["vnin"]
            existing_data = ServiceModel.find_data_by_id(vnin)

            if existing_data:
                response_data = {
                    "data": {
                        "_id": existing_data["id"],
                        "firstName": existing_data['firstName'],
                        "middleName": existing_data['middleName'],
                        "lastName": existing_data['lastName'],
                        "image": existing_data["image"],
                        "status": existing_data["status"],
                        "mobile": existing_data["mobile"],
                        "requesTime": datetime.utcnow().isoformat(),
                    },
                }
                return jsonpickle.encode(response_data), 200

            # Gather data from request
            data = {
                "id": vnin,
                "isSubjectConsent": True,
            }
            if "image" in request.json:
                data["validations"] = {
                    "selfie": {"image": request.json["image"]}
                }
            if all(
                field in request.json for field in [
                    "firstName",
                    "lastName",
                    "dateOfBirth"]):
                data.setdefault("validations", {})["data"] = {
                    "firstName": request.json["firstName"],
                    "lastName": request.json["lastName"],
                    "dateOfBirth": request.json["dateOfBirth"],
                }

            url = f"{youverify}/v2/api/identity/ng/vnin"
            headers = {
                'Content-Type': 'application/json',
                'token': token
            }
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()

            if response_data["data"]["status"] == "found":
                ServiceModel.insert_data(response_data["data"])

            new_entry = ServiceModel.find_data_by_id(vnin)
            response_data = {
                "data": {
                    "_id": new_entry["id"],
                    "firstName": new_entry['firstName'],
                    "middleName": new_entry['middleName'],
                    "lastName": new_entry['lastName'],
                    "image": new_entry["image"],
                    "status": new_entry["status"],
                    "mobile": new_entry["mobile"],
                    "requesTime": datetime.utcnow().isoformat(),
                },
            }
            return jsonpickle.encode(response_data), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def nin_verification():
        try:
            nin = request.json["nin"]
            existing_data = ServiceModel.find_data_by_id(nin)

            if existing_data:
                response_data = {
                    "data": {
                        "_id": existing_data["id"],
                        "firstName": existing_data['firstName'],
                        "middleName": existing_data['middleName'],
                        "lastName": existing_data['lastName'],
                        "image": existing_data["image"],
                        "status": existing_data["status"],
                        "mobile": existing_data["mobile"],
                        "requesTime": datetime.utcnow().isoformat(),
                    },
                }
                return jsonpickle.encode(response_data), 200

            # Gather data from request
            data = {
                "id": nin,
                "isSubjectConsent": True,
            }
            if "image" in request.json:
                data["validations"] = {
                    "selfie": {"image": request.json["image"]}
                }
            if all(
                field in request.json for field in [
                    "firstName",
                    "lastName",
                    "dateOfBirth"]):
                data.setdefault("validations", {})["data"] = {
                    "firstName": request.json["firstName"],
                    "lastName": request.json["lastName"],
                    "dateOfBirth": request.json["dateOfBirth"],
                }

            url = f"{youverify}/v2/api/identity/ng/nin"
            headers = {
                'Content-Type': 'application/json',
                'token': token
            }
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()

            if response_data["data"]["status"] == "found":
                ServiceModel.insert_data(response_data["data"])

            new_entry = ServiceModel.find_data_by_id(nin)
            response_data = {
                "data": {
                    "_id": new_entry["id"],
                    "firstName": new_entry['firstName'],
                    "middleName": new_entry['middleName'],
                    "lastName": new_entry['lastName'],
                    "image": new_entry["image"],
                    "status": new_entry["status"],
                    "mobile": new_entry["mobile"],
                    "requesTime": datetime.utcnow().isoformat(),
                },
            }
            return jsonpickle.encode(response_data), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def ip_verification():
        try:
            pass_num = request.json["pass_num"]
            existing_data = ServiceModel.find_data_by_id(pass_num)

            if existing_data:
                response_data = {
                    "data": {
                        "_id": existing_data["id"],
                        "firstName": existing_data['firstName'],
                        "middleName": existing_data['middleName'],
                        "lastName": existing_data['lastName'],
                        "image": existing_data["image"],
                        "status": existing_data["status"],
                        "mobile": existing_data["mobile"],
                        "requesTime": datetime.utcnow().isoformat(),
                    },
                }
                return jsonpickle.encode(response_data), 200

            # Gather data from request
            data = {
                "id": pass_num,
                "isSubjectConsent": True,
                "lastName": request.json["lastName"],
            }
            if "image" in request.json:
                data["validations"] = {
                    "selfie": {"image": request.json["image"]}
                }
            if all(
                field in request.json for field in [
                    "firstName",
                    "dateOfBirth"]):
                data.setdefault("validations", {})["data"] = {
                    "firstName": request.json["firstName"],
                    "dateOfBirth": request.json["dateOfBirth"],
                }

            url = f"{youverify}/v2/api/identity/ng/passport"
            headers = {
                'Content-Type': 'application/json',
                'token': token
            }
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()

            if response_data["data"]["status"] == "found":
                ServiceModel.insert_data(response_data["data"])

            new_entry = ServiceModel.find_data_by_id(pass_num)
            response_data = {
                "data": {
                    "_id": new_entry["id"],
                    "firstName": new_entry['firstName'],
                    "middleName": new_entry['middleName'],
                    "lastName": new_entry['lastName'],
                    "image": new_entry["image"],
                    "status": new_entry["status"],
                    "mobile": new_entry["mobile"],
                    "requesTime": datetime.utcnow().isoformat(),
                },
            }
            return jsonpickle.encode(response_data), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @staticmethod
    def ad_phone_verification():
        try:
            mobile = request.json["mobile"]
            print(mobile)

            existing_data = ServiceModel.find_data_by_id(
                "vault", {"idNumber": mobile})

            if existing_data:
                response_data = {
                    "data": {
                        "_id": existing_data["id"],
                        "firstName": existing_data['firstName'],
                        "middleName": existing_data['middleName'],
                        "lastName": existing_data['lastName'],
                        "image": existing_data["image"],
                        "nin": existing_data["nin"],
                        "status": existing_data["status"],
                        "mobile": existing_data["mobile"],
                        "requesTime": datetime.utcnow().isoformat(),
                    },
                }
                print("data from database")
                return jsonpickle.encode(response_data)

            lastName = request.form.get('lastName')
            firstName = request.form.get('firstName')
            dateOfBirth = request.form.get('dateOfBirth')
            image = request.form.get('image')

            data = {
                "mobile": mobile,
                "isSubjectConsent": "true"
            }
            if image:
                data["validations"] = {
                    "selfie": {
                        "image": request.json["image"]
                    }
                }
            if firstName and lastName and dateOfBirth:
                data["validations"]["data"] = {
                    "firstName": request.json["firstName"],
                    "lastName": request.json["lastName"],
                    "dateOfBirth": request.json["dateOfBirth"]
                }
            headers = {
                'Content-Type': 'application/json',
                'token': token
            }

            url = f"{youverify}v2/api/identity/ng/nin-phone"
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            if response_data["data"]["status"] == "found":
                ServiceModel.insert_data("vault", response_data["data"])
            print("request from youverify")
            new_entry = ServiceModel.find_data_by_id(mobile)

            response_data = {
                "data": {
                    "_id": new_entry["id"],
                    "firstName": new_entry['firstName'],
                    "middleName": new_entry['middleName'],
                    "lastName": new_entry['lastName'],
                    "image": new_entry["image"],
                    "status": new_entry["status"],
                    "mobile": new_entry["mobile"],
                    "requestTime": datetime.utcnow().isoformat()
                },
            }
            print("data from database")

            return jsonpickle.encode(response_data)

        except Exception as e:
            return str(e)

    @staticmethod
    def facial_comparison():
        try:
            data = {
                "image1": request.json["image1"],
                "image2": request.json["image2"],
                "isSubjectConsent": True
            }

            url = f"{youverify}v2/api/identity/compare-image"
            headers = {
                'Content-Type': 'application/json',
                'token': token
            }
            print("hello")

            response = requests.post(url, headers=headers, json=data)
            print(response.status_code)
            response_data = response.json()
            print(response_data["data"]["imageComparison"]["match"])
            if response_data["data"]["imageComparison"]["match"]:
                print("data from youverify")
                return jsonify(response_data)
            else:
                return jsonify({"error": "images do not match"})

        except Exception as e:
            print(e)
            return jsonify(str(e))

    @staticmethod
    def cac():
        try:
            cac = request.json["cac"]
            print(cac)

            existing_data = ServiceModel.find_data_by_reg_num(cac)

            if existing_data:
                response_data = {
                    "data": {
                        "_id": existing_data["id"],
                        "status": existing_data["status"],
                        "requestTime": datetime.utcnow().isoformat(),
                    },
                }
                print("data from database")
                return jsonpickle.encode(response_data)

            data = {
                "registrationNumber": cac,
                "countryCode": "NG",
                "isSubjectConsent": "true"
            }
            headers = {
                'Content-Type': 'application/json',
                'token': token
            }

            url = f"{youverify}v2/api/verifications/global/company-advance-check"
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            if response_data["data"]["status"] == "found":
                ServiceModel.insert_data("vault", response_data["data"])
            print("request from youverify")
            new_entry = ServiceModel.find_data_by_reg_num(cac)

            response_data = {
                "data": {
                    "_id": new_entry["id"],
                    "status": new_entry["status"],
                    "requestTime": datetime.utcnow().isoformat()
                },
            }
            print("data from database")

            return jsonpickle.encode(response_data)

        except Exception as e:
            return str(e)
