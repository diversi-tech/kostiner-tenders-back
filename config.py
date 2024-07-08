from pymongo import MongoClient
import certifi
from flask_mail import Mail

mail = Mail()
ca = certifi.where()
try:


  MONGO_URI = 'mongodb+srv://sh485014:s3273805@sara.kjxve7r.mongodb.net/'

  client = MongoClient(MONGO_URI, tls=True,tlsAllowInvalidCertificates=True,tlsCAFile=ca)

  db = client['item']
  collection = db['item']
  # print("Connected to MongoDB")
  result = collection.find_one({})
  # print(result)
except Exception as e:
    print("Error: ", e)
try:

    users_collection = db['users']

    # print("Connected to MongoDB")
    result = users_collection.find_one({})
    # print(result)
except Exception as e:
    print("Error: ", e)
