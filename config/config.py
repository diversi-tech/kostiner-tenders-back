# from pymongo import MongoClient
# import certifi
# from flask_mail import Mail
#
#  = Mail()
# ca = certifi.where()
# try:
#
# #   MONGO_URI = 'mongodb+srv://sh485014:s3273805@sara.kjxve7r.mongodb.net/'
#
# #   client = MongoClient(MONGO_URI, tls=True,tlsAllowInvalidCertificates=True,tlsCAFile=ca)
#
# #   db = client['item']
# #   collection = db['item']
# #   # print("Connected to MongoDB")
# #   result = collection.find_one({})
#   # print(result)
#
#     MONGO_URI = 'mongodb+srv://<userName>:<password>@<cluster>.mongodb.net/'
#
#     client = MongoClient(MONGO_URI)
#
#     db = client['<nameDB>']
# except Exception as e:
#     print("Error: ", e)
# try:
#
#     users_collection = db['users']
#
#     # print("Connected to MongoDB")
#     result = users_collection.find_one({})
#     # print(result)
# except Exception as e:
#     print("Error: ", e)
import certifi
from flask_mail import Mail
from pymongo import MongoClient
import os

mail = Mail()
ca = certifi.where()
class Config:
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('kustiner1@gmail.com')
    MAIL_PASSWORD = os.getenv('i a u m z l p a q x r b d v s d')

