# from werkzeug.security import generate_password_hash, check_password_hash
#
# from config import db
#
#
# class AuthRepo:
#     def __init__(self):
#         self.user_collection = db['users']
#     def create_user(self, username, password):
#         hashed_password = generate_password_hash(password)
#         self.user_collection.insert_one({'username': username, 'password': hashed_password})
#
#     def verify_user(self, username, password):
#         user = self.user_collection.find_one({'username': username})
#         if user and check_password_hash(user['password'], password):
#             return True
#         return False
from werkzeug.security import generate_password_hash, check_password_hash
from config import db

class AuthRepo:
    def __init__(self):
        self.user_collection = db['users']

    def create_user(self, username, password):
        hashed_password = generate_password_hash(password)
        self.user_collection.insert_one({'username': username, 'password': hashed_password})

    def verify_user(self, username, password):
        print("list", list(self.user_collection.find({})))
        user = self.user_collection.find_one({'username': username})
        if user['password']== password:
        # if user and check_password_hash(user['password'], password):
            print("password if", user['password'])

            return True
        return False
