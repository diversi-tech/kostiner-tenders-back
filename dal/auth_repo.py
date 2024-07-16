import os
import jwt
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from config.config import db

from dal.createDB.connectDB import connect_to_mongodb


class AuthRepo:
    def __init__(self):
        client=connect_to_mongodb()
        db_kostiner=client['Kostiner']
        self.user_collection=db_kostiner['users']
        print("user-repo",self.user_collection.find_one({}))
        # self.user_collection = c['users']
        # print("self",self.user_collection)
        #self.user_collection=db['users']
        self.token_collection = db['tokenForUUID']



    def create_user(self, username, password):
        hashed_password = generate_password_hash(password)
        self.user_collection.insert_one({'username': username, 'password': hashed_password})

    def verify_user(self, username, password):
        print("username",username)
        user = self.user_collection.find_one({'user_name': username})
        print("user",user)
        if user and user['password'] == password:
        # if user and check_password_hash(user['password'], password):
        #     print("password if", user['password'])
            return user, True

        return None, False


    def find_user_by_email(self, email):
        user = self.user_collection.find_one({'email': email})
        return user


    def user_exists(self,email):
        # print(email)
        # print("list", list(self.user_collection.find({})))
        return self.user_collection.find_one({'email': email}) is not None

    def get_reset_token_entry(self,token):
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
            username = payload['username']
            email = payload['email']
            role =payload['role']
            return payload
        except jwt.ExpiredSignatureError:
            return None, None
        except jwt.InvalidTokenError:
            return None, None


    def reset_password(self, email, role, new_password, username):
        # חיפוש המשתמש לפי האימייל והשם משתמש
        user = self.user_collection.find_one({'$and': [{'email': email}, {'username': username}, {'role': role}]})
        if not user:
            return 'User not found', 400

        # עדכון הסיסמה למשתמש המתאים
        query = {'$and': [{'username': username}, {'email': email}]}
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
        user = self.user_collection.find_one({'$and': [{'email': email}, {'first_name': username}]})
        print(user)
        if not user:
            raise Exception("User not found")

        role = user['role']
        token_data = {
            'email': email,
            'username': username,
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
    def reset_password(self,email,role,new_password,username):
        user = self.user_collection.find_one({'$and': [{'email': email}, {'first_name': username},{'role': role}]})
        if user['email'] != email:
            return 'Email does not match the user', 400
        print("user",user)
        if not user:
            return 'User not found.', 400
        query = {
            '$and': [
                {'username': username},
                {'email': email}
            ]
        }
        update = {'$set': {'password': new_password}}
        self.user_collection.update_one(query,update)
        user = self.user_collection.find_one({'$and': [{'email': email}, {'first_name': username}, {'role': role}]})
        print(user['password'])
        return  'שינוי הסיסמא עודכן בהצלחה', 200