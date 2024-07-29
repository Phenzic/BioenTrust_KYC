import hmac
import hashlib
import binascii
import os


class HMACHelper:
    def __init__(self, secret_key):
        self.secret_key = secret_key.encode()

    def generate_key(self):
        key = binascii.hexlify(os.urandom(24)).decode()
        signature = hmac.new(
            self.secret_key,
            key.encode(),
            hashlib.sha256).hexdigest()
        return key, signature

    def verify_key(self, key, signature):
        expected_signature = hmac.new(
            self.secret_key, key.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_signature, signature)
