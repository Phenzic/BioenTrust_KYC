from ..config import Config
from flask_mail import Mail
import redis

mail = Mail()


def init_utils(app):
    mail.init_app(app)


redis_client = redis.StrictRedis.from_url(Config.REDIS_HOST)

# try:
#     redis_client.ping()
#     print("Connected to Redis Succesfully")
# except redis.ConnectionError as e:
#     print((f"Could not connect to Redis {e}"))
