import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kustiner1@gmail.com'
    MAIL_PASSWORD = 'i a u m z l p a q x r b d v s d'
    MAIL_DEFAULT_SENDER = 'kustiner1@gmail.com'
    MONGO_URI = os.getenv('MONGO_URI')
