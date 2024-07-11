from bson import ObjectId, json_util
import json

from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, set_access_cookies

from config import mail
from models.login_model import login_model, auth_ns, token_model, reset_password_model, token_verify_model
from services.auth_service import AuthService
from flask_mail import  Message

auth_service = AuthService()

def serialize_user(user):
    """Convert ObjectId instances in a user dictionary to strings."""
    if isinstance(user, tuple) and len(user) > 0 and isinstance(user[0], dict):
        user_data = user[0]
        # Remove password field if it exists
        user_data.pop('password', None)
        serialized_user = json.loads(json_util.dumps(user_data, default=str))
        return serialized_user
    elif isinstance(user, dict):
        # Remove password field if it exists
        user.pop('password', None)
        serialized_user = json.loads(json_util.dumps(user, default=str))
        return serialized_user
    return None


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Success', token_model)
    @auth_ns.response(401, 'Unauthorized')
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user_tuple=auth_service.verify_user(username, password)
        user_dict = user_tuple[0]
        user_id = str(user_dict['_id'])  # להמיר את ה-ObjectId למחרוזת
        print(f"user_id: {user_id}")
        if user_dict:
            userrole = user_dict['role']
            additional_claims = {
                'role': userrole,
                'user_id': user_id
            }
            access_token =create_access_token(identity=userrole, additional_claims=additional_claims)
            return {'access_token': 'Bearer ' + access_token}, 200
        #     print("access_token",access_token)
        #     serialized_user = serialize_user(user_tuple)
        #     print("serialized_user1",serialized_user)  # For debugging
        #
        #     # Create JSON response data
        #     response_data = {
        #         'message': 'Login successful',
        #         'access_token': 'Bearer ' + access_token,
        #         'user':serialized_user
        #     }
        #     response = make_response(jsonify(response_data))
        #     response.set_cookie('access_token', access_token,
        #                         httponly=True,
        #                         secure=False,
        #                         samesite='None',
        #                         domain='localhost',
        #                         path='/')
        #     print( response.headers)
        #     #response.set_cookie('access_token', access_token, httponly=True, secure=True, samesite='Strict')
        #     return response
        # else:
        #      return jsonify({'message': 'Invalid credentials'}), 401

@auth_ns.route('/reset-password/request')
class PasswordResetRequest(Resource):
    @auth_ns.expect(reset_password_model)
    @auth_ns.response(200, 'Password reset email sent successfully')
    @auth_ns.response(400, 'User not found')
    def post(self):
        '''Initiate password reset'''
        data = request.json
        email = data.get('email')
        username = data.get('username')

        if not auth_service.user_exists(email):
            return {'message': 'User not found'}, 400

        # Generate a reset token and identifier
        token = auth_service.generate_reset_token(email, username)
        reset_link = f"http://localhost:5173/reset-password/?id"  # Use the identifier in the reset link

        msg = Message('Password Reset Request', recipients=[email])
        msg.html = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">

        <p>היי, {username}</p>
        <p>נראה שביקשת לאפס את הסיסמה שלך. לחץ על הקישור למטה כדי לאפס אותה:</p>
        <p><a href="{reset_link}" style="background-color: #0A3F3D; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">לאפס את הסיסמה</a></p>
        <p>הקישור זה יפוג בעוד 30 דקות.</p>
        <p>אם לא ביקשת זאת, אנא התעלם מאימייל זה.</p>
        </body>
        </html>
        """
        try:
            mail.send(msg)
            print('Email sent successfully')
        except Exception as e:
            print(f'Failed to send email: {e}')
            return {'message': f'Failed to send email: {str(e)}'}, 500

        return token

# @auth_ns.route('/reset-password/verify')
# class PasswordResetVerify(Resource):
#     @auth_ns.expect(token_verify_model)
#     @auth_ns.response(200, 'Token verified')
#     @auth_ns.response(400, 'Invalid or expired token')
#     def post(self):
#         '''Verify password reset token'''
#         data = request.json
#         identifier = data.get('identifier')
#
#         reset_token_entry = auth_service.get_reset_token_entry(identifier)
#         if not reset_token_entry:
#             return {'message': 'Invalid or expired token'}, 400
#
#         return {'message': 'Token verified', 'email': reset_token_entry['email'], 'username': reset_token_entry['username']}, 200

@auth_ns.route('/reset-password/response', methods=['OPTIONS','POST'])
class PasswordResetResponse(Resource):
    # @auth_ns.expect(token_model)
    # @auth_ns.response(200, 'Password reset successful')
    # @auth_ns.response(200, 'Password reset email sent successfully')
    # @auth_ns.response(400, 'Invalid or expired reset token')
    # @auth_ns.expect(token_model)
    # @auth_ns.response(200, 'Password reset successful')
    # @auth_ns.response(400, 'Invalid or expired token')
    # @auth_ns.response(401, 'Token has expired')
    # @auth_ns.response(404, 'User not found')
    # @auth_ns.response(500, 'Unknown error')
    # def options(self):
    #     """
    #     מתודת OPTIONS - מאפשרת בקשות CORS.
    #     """
    #     return {'Allow': 'POST, OPTIONS'}, 200, {
    #
    #         'Access-Control-Allow-Origin': 'http://localhost:5173',
    #         'Access-Control-Allow-Methods': 'POST, OPTIONS',
    #         'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    #         'Access-Control-Allow-Credentials': 'true'
    #
    #     }

    # @auth_ns.expect(token_model)
    @auth_ns.response(200, 'Password reset successful')
    @auth_ns.response(400, 'Invalid token')
    @auth_ns.response(401, 'Token expired')
    @auth_ns.response(500, 'Unknown error')
    def post(self):
        data = request.json
        token = data.get('token')  # קבלת ה-UUID מהבקשה
        new_password=data.get('new_password')
        result = auth_service.reset_password(token, new_password)
        if isinstance(result, tuple):
            message, status_code = result
            return {'message': message}, status_code

        return {'message': 'Unknown error occurred'}, 500


