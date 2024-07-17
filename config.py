import os

class Config:
    SECRET_KEY = os.urandom(24)
    MONGO_URI = 'your_mongodb_uri_here'  # Replace with your MongoDB Atlas URI
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Replace with your JWT secret key
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
