from flask_mongoengine import MongoEngine

db = MongoEngine()

class User:
    def __init__(self, user_id, username=None, password=None, email=None,role=None,
                 first_name=None, last_name=None, business_name=None):
        self.user_id = user_id
        self.user_name = username
        self.password = password
        self.email = email
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.business_name = business_name