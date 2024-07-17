import os


class Config:
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    CORS_ORIGINS = "*"
    MONGO_URI = os.getenv("MONGO_URI")
    REDIS_HOST = os.getenv("REDIS_CLIENT")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_USERNAME")

    # app.config['CACHE_TYPE'] = 'redis'
    # app.config['CACHE_REDIS_HOST'] = 'localhost'
    # app.config['CACHE_REDIS_PORT'] = 6379
    # app.config['CACHE_REDIS_DB'] = 0
    # app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
