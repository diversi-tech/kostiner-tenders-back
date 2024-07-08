import os
from functools import wraps
from datetime import datetime

import jwt
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_current_user
from itsdangerous import SignatureExpired, BadSignature

from dal.auth_repo import AuthRepo

class AuthService:
    def __init__(self):
        self.auth_repo = AuthRepo()

    def create_user(self, username, password):
        return self.auth_repo.create_user(username, password)

    def verify_user(self, username, password):

        return self.auth_repo.verify_user(username, password)



    def find_user_by_email(self, email):
        return self.auth_repo.find_user_by_email(email)

    def user_exists(self,email):
        # print("service",email)
        return self.auth_repo.user_exists(email)

    def generate_reset_token(self,email,username):
        # print("service 2",email)
        return self.auth_repo.generate_reset_token(email,username)

    # def reset_password(self,token,new_password):
    #     try:
    #         token_data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
    #         email = token_data['email']
    #         username = token_data['username']
    #         role = token_data['role']
    #         now = datetime.utcnow()
    #         if token_data['exp'] < now.timestamp():
    #             return 'Token has expired', 400
    #     except SignatureExpired:
    #         return  'The reset link has expired.', 400
    #     except BadSignature:
    #         return 'Invalid reset link.', 400
    #     result= self.auth_repo.reset_password(email,role,new_password,username)
    #     return 'Password has been reset successfully.', 200

    def get_reset_token_entry(self, identifier):
        token_entry = self.auth_repo.token_collection.find_one({'identifier': identifier})
        if not token_entry or token_entry['expires_at'] < datetime.utcnow():
            return None
        return token_entry

    def reset_password(self, identifier, new_password):

        reset_token_entry = self.auth_repo.get_reset_token_entry(identifier)
        if not reset_token_entry:
            return 'Invalid or expired token', 400

        email = reset_token_entry['email']
        username = reset_token_entry['username']
        role = reset_token_entry['role']


        now = datetime.utcnow()
        if reset_token_entry['exp'] < now.timestamp():
            return 'Token has expired', 401


        result = self.auth_repo.reset_password(email, role, new_password, username)
        if isinstance(result, tuple):
            message, status_code = result
            return message, status_code

        self.auth_repo.delete_reset_token_entry(identifier)
        return 'Password has been reset successfully', 200

policies = {
        "AdminPolicy": lambda user: user.get("role") == "admin",
        "ClientPolicy": lambda user: user.get("role") == "client",
        "UserPolicy": lambda user: user.get("role") == "user"
    }

def get_current_user():
        user = get_jwt_identity()
        return user

def policy_required(policy_name):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):

                user = get_current_user()
                # print("user", user)
                if not user:
                    raise ValueError(401)

                policy = policies.get(policy_name)
                # if not policy or not policy(user):
                # print(policy_name,"role",user)
                if user != policy_name:
                    raise ValueError(403)
                return f(*args, **kwargs)

            return decorated_function

        return decorator








    # def generate_reset_token(self, email):
    #     return self.auth_repo.generate_reset_token(email)
    #
    #
    # def initiate_password_reset(self, email):
    #     user = self.user_repo.find_user_by_email(email)
    #     if not user:
    #         return False, 'User not found'
    #
    #     reset_token = self.user_repo.generate_reset_token(email)
    #     self.send_reset_email(email, reset_token)
    #
    #     return True, 'Password reset email sent successfully'
    #
    # def send_reset_email(self, email, reset_token):
    #     msg = Message('Password Reset Request', recipients=[email])
    #     reset_link = f'http://example.com/reset-password/{reset_token}'
    #     msg.body = f'Click the link to reset your password: {reset_link}'
    #     self.mail.send(msg)
    #
    # def reset_password(self, reset_token, new_password):
    #     token_entry = self.user_repo.reset_tokens_collection.find_one({'token': reset_token})
    #     if not token_entry:
    #         return False, 'Invalid or expired token'
    #
    #     email = token_entry['email']
    #     self.user_repo.update_password(email, new_password)
    #     return True, 'Password updated successfully'


    # def send_password_reset_email(self, email, reset_token):
    #     return self.auth_repo.send_password_reset_email(email,reset_token)
    #
    # def reset_password(self, email, new_password):
    #     return self.auth_repo.reset_password(email,new_password)
    #