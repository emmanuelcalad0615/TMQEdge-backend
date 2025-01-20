from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()

class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_TOKEN_LOCATION = 'headers'
    JWT_COOKIE_SECURE = False  # Cambiar a True en producción si usas HTTPS
    JWT_COOKIE_HTTPONLY = True  # Proteger la cookie contra accesos desde JavaScript
    JWT_ACCESS_COOKIE_NAME = 'access_token'  
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=50)
    #SECRET_KEY = os.getenv('FLASK_SECRET_KEY')