from ..config import Config
from flask_mail import Mail
import redis

mail = Mail()

def init_utils(app):
    mail.init_app(app)
    
redis_client = redis.StrictRedis(host=Config.REDIS_HOST)
