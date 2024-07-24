import datetime
import random
import string
from flask import current_app as app


class Wallet:

    @staticmethod
    def transaction_log(
        user_id,
        transaction_type,
        transaction_amount,
        old_wallet_balance,
        new_wallet_balance,
        status,
    ):
        transaction_id = "".join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )

        transaction = {
            "_id": transaction_id,
            "user_id": user_id,
            "transaction_type": transaction_type,
            "transaction_amount": transaction_amount,
            "old_wallet_balance": old_wallet_balance,
            "new_wallet_balance": new_wallet_balance,
            "transaction_time": datetime.datetime.now(),
            "staus": status,
        }
        db = app.db.wallet
        db["transactions"].insert_one(transaction)
        return True
