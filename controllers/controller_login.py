from bson import json_util
import json

from flask_restx import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity

# from app.app import BLACKLIST
from config.config import mail
from middlewares.blackList import BLACKLIST
from models.login_model import login_model, auth_ns, reset_password_model,token_model
from services.auth_service import AuthService
from flask_mail import Message

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


# @auth_ns.route('/login', methods=['OPTIONS','POST'])
# class Login(Resource):
#     @auth_ns.expect(login_model)
#     @auth_ns.response(200, 'Success')
#     @auth_ns.response(401, 'Unauthorized')
#     def post(self):
#         data = request.json
#         username = data.get('username')
#         password = data.get('password')
#         user_tuple=auth_service.verify_user(username, password)
#         user_dict = user_tuple[0]
#         print(user_dict)
#         user_id = str(user_dict['_id'])  # להמיר את ה-ObjectId למחרוזת
#         print(f"user_id: {user_id}")
#         if user_dict:
#             userrole = user_dict['role']
#             additional_claims = {
#                 'role': userrole,
#                 'user_id': user_id
#             }
#             access_token =create_access_token(identity=userrole, additional_claims=additional_claims)
#
#             print(access_token)
#             return {'access_token': 'Bearer ' + access_token}, 200
@auth_ns.route('/login', methods=['OPTIONS','POST'])
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Success', token_model)
    @auth_ns.response(401, 'Unauthorized')
    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user, is_valid = auth_service.verify_user(username, password)
        if is_valid:
            user_id = str(user['user_id'])
            user_role = user['role']
            additional_claims = {
                'role': user_role,
                'user_id': user_id
            }
            access_token = create_access_token(identity=user_role, additional_claims=additional_claims)
            return {'access_token': 'Bearer ' + access_token}, 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    def options(self):
        """
        מתודת OPTIONS - מאפשרת בקשות CORS.
        """
        return {'Allow': 'POST, OPTIONS'}, 200, {

            'Access-Control-Allow-Origin': 'http://localhost:5173',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true'

        }
# @auth_ns.route('/reset-password/request')
# class PasswordResetRequest(Resource):
#     @auth_ns.expect(reset_password_model)
#     @auth_ns.response(200, 'Password reset email sent successfully')
#     @auth_ns.response(400, 'User not found')
#     def post(self):
#         '''Initiate password reset'''
#         data = request.json
#         email = data.get('email')
#         username = data.get('username')
#
#         if not auth_service.user_exists(email):
#             return {'message': 'User not found'}, 400
#
#         # Generate a reset token and identifier
#         token = auth_service.generate_reset_token(email, username)
#         reset_link = f"https://kostiner-tenders.onrender.com/resetPasword"  # Use the identifier in the reset link
#         body = f"""
#         <html>
#         <body style="font-family: Arial, sans-serif;">
#
#         <p>היי, {username}</p>
#         <p>נראה שביקשת לאפס את הסיסמה שלך. לחץ על הקישור למטה כדי לאפס אותה:</p>
#         <p><a href="{reset_link}" style="background-color: #0A3F3D; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 5px;">לאפס את הסיסמה</a></p>
#         <p>הקישור זה יפוג בעוד 30 דקות.</p>
#         <p>אם לא ביקשת זאת, אנא התעלם מאימייל זה.</p>
#         </body>
#         </html>
#         """
#         try:
#             auth_service.send_email(email, 'Password Reset Request', body)
#             print('Email sent successfully')
#         except Exception as e:
#             print(f'Failed to send email: {e}')
#             return {'message': f'Failed to send email: {str(e)}'}, 500
#
#         print(token)
#         return token

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
        reset_link = f"https://kostiner-tenders.onrender.com/resetPasword"  # Use the identifier in the reset link
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
        print(token)
        return token


@auth_ns.route('/reset-password/response', methods=['OPTIONS','POST'])
class PasswordResetResponse(Resource):
    @auth_ns.response(200, 'Password reset successful')
    @auth_ns.response(400, 'Invalid or expired token')
    @auth_ns.response(401, 'Token has expired')
    @auth_ns.response(404, 'User not found')
    @auth_ns.response(500, 'Unknown error')
    @auth_ns.expect(token_model)
    def options(self):
        """
        מתודת OPTIONS - מאפשרת בקשות CORS.
        """
        return {'Allow': 'POST, OPTIONS'}, 200, {

            'Access-Control-Allow-Origin': 'http://localhost:5173',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true'

        }
    @auth_ns.expect(token_model)
    @auth_ns.response(200, 'Password reset successful')
    @auth_ns.response(400, 'Invalid token')
    @auth_ns.response(401, 'Token expired')
    @auth_ns.response(500, 'Unknown error')
    def post(self):
        data = request.json
        token = data.get('token')
        new_password = data.get('new_password')
        result = auth_service.reset_password(token, new_password)
        if isinstance(result, tuple):
            message, status_code = result
            return {'message': message}, status_code

        return {'message': 'Unknown error occurred'}, 500

@auth_ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    def options(self):
        """
        מתודת OPTIONS - מאפשרת בקשות CORS.
        """
        return {'Allow': 'POST, OPTIONS'}, 200, {

            'Access-Control-Allow-Origin': 'http://localhost:5174',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true'

        }
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        try:
            print(jti)
            BLACKLIST.add(jti)
            return {'message': 'Logged out successfully'}, 200
        except Exception as e:
            return jsonify({"msg": "Logout failed"}), 500



