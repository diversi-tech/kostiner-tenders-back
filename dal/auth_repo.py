import json
import os
import jwt
# from jwt.algorithms import RSAAlgorithm
# from jwt.algorithms import RSAAlgorithm
import requests
from bson import ObjectId
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from config.config import db

from dal.createDB.connectDB import connect_to_mongodb


class AuthRepo:
    def __init__(self):
        client = connect_to_mongodb()
        db_kostiner = client['Kostiner']
        self.user_collection = db_kostiner['users']
        print("user-repo", self.user_collection.find_one({}))
        # self.user_collection = c['users']
        # print("self",self.user_collection)
        # self.user_collection = db['users']
        self.token_collection = db['tokenForUUID']



    def create_user(self, username, password):
        hashed_password = generate_password_hash(password)
        self.user_collection.insert_one({'username': username, 'password': hashed_password})
        user = self.user_collection.find_one({'username': username, 'password': hashed_password})
        if user:
            print(f'new user = {user}')
            return user
        return None
    def verify_user(self, username, password):
        print("username", username)
        user = self.user_collection.find_one({'user_name': username})
        print("user",user)
        if user['password']== password:
            return user, True

        return None,False

    def find_user_by_email(self, email):
        user = self.user_collection.find_one({'email': email})
        return user

    def user_exists(self, email):
        # print(email)
        # print("list", list(self.user_collection.find({})))
        return self.user_collection.find_one({'email': email}) is not None

    def get_reset_token_entry(self, token):
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None, None
        except jwt.InvalidTokenError:
            return None, None

    def decode_google_jwt(self, token):
        try:
            # קבלת המפתחות הפומביים של גוגל
            google_keys_url = "https://www.googleapis.com/oauth2/v3/certs"
            response = requests.get(google_keys_url)
            keys = response.json().get('keys', [])
            # k = 'zaUomGGU1qSBxBHOQRk5fF7rOVVzG5syHhJYociRyyvvMOM6Yx_n7QFrwKxW1Gv-YKPDsvs-ksSN5YsozOTb9Y2HlPsOXrnZHQTQIdjWcfUz-TLDknAdJsK3A0xZvq5ud7ElIrXPFS9UvUrXDbIv5ruv0w4pvkDrp_Xdhw32wakR5z0zmjilOHeEJ73JFoChOaVxoRfpXkFGON5ZTfiCoO9o0piPROLBKUtIg_uzMGzB6znWU8Yfv3UlGjS-ixApSltsXZHLZfat1sUvKmgT03eXV8EmNuMccrhLl5AvqKT6E5UsTheSB0veepQgX8XCEex-P3LCklisnen3UKOtLw'

            # נסה לפענח את הטוקן עם כל אחד מהמפתחות הפומביים
            for key in keys:
                try:
                    print(key)
                    payload = jwt.decode(token, key=key, algorithms=['RS256'], audience=os.getenv('GOOGLE_CLIENT_ID'))
                    return payload, 200
                except jwt.ExpiredSignatureError:
                    return {'message': 'Token has expired'}, 401
                except jwt.InvalidTokenError:
                    continue

            # אם לא הצלחת לפענח את הטוקן עם אף אחד מהמפתחות
            return {'message': 'Invalid token'}, 400

        except requests.RequestException as e:
            return {'message': f'Failed to fetch Google public keys: {str(e)}'}, 500

    def reset_password(self, email, role, new_password, username):
        # חיפוש המשתמש לפי האימייל והשם משתמש
        user = self.user_collection.find_one({'$and': [{'email': email}, {'user_name': username}, {'role': role}]})
        if not user:
            return 'User not found', 400

        # עדכון הסיסמה למשתמש המתאים
        query = {'$and': [{'user_name': username}, {'email': email}]}
        update = {'$set': {'password': new_password}}
        self.user_collection.update_one(query, update)

        # החזרת הודעה כי הסיסמה עודכנה בהצלחה
        return 'Password has been reset successfully', 200

        # פונקציה למחיקת רשומת הטוקן מהמסד הנתונים

    def delete_reset_token_entry(self, identifier):
        query = {'identifier': identifier}
        self.reset_token_collection.delete_one(query)

    # def generate_reset_token(self,email, username):
    #     user = self.user_collection.find_one({'$and': [{'email': email}, {'first_name': username}]})
    #     if not user:
    #         raise Exception("User not found")
    #     role = user['role']
    #     expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    #     token = jwt.encode({'email': email, 'first_name': username,role:role, 'exp': expires}, os.getenv(['JWT_SECRET_KEY']),
    #                        algorithm='HS256')
    #     return token
    def generate_reset_token(self, email, username):
        user = self.user_collection.find_one({'$and': [{'email': email}, {'user_name': username}]})
        print(user)
        if not user:
            raise Exception("User not found")

        role = user['role']
        token_data = {
            'email': email,
            'user_name': username,
            'role': role,
            'exp': datetime.utcnow() + timedelta(minutes=30)  # Token expiration time
        }
        token = jwt.encode(token_data, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
        return token

        # identifier = str(uuid.uuid4())
        # # Save the token and identifier in the database
        # self.token_collection.insert_one({
        # 'identifier': identifier,
        # 'token': token,
        # 'created_at': datetime.utcnow(),
        # 'expires_at': datetime.utcnow() + timedelta(minutes=30),
        # 'email': email,
        # 'username': username
        # })
        # return identifier

    def reset_password(self, email, role, new_password, username):
        user = self.user_collection.find_one({'$and': [{'email': email}, {'user_name': username}, {'role': role}]})
        if user['email'] != email:
            return 'Email does not match the user', 400
        print("user", user)
        if not user:
            return 'User not found.', 400
        query = {
            '$and': [
                {'user_name': username},
                {'email': email}
            ]
        }
        update = {'$set': {'password': new_password}}
        self.user_collection.update_one(query, update)
        user = self.user_collection.find_one({'$and': [{'email': email}, {'user_name': username}, {'role': role}]})
        print(user['password'])
        return 'שינוי הסיסמא עודכן בהצלחה', 200
