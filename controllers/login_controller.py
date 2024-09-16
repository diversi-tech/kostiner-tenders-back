import jwt
import requests
from bson import ObjectId, json_util
import json
import os
from flask_restx import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity, create_refresh_token

from config import settings
from config.config import mail
from middlewares.blackList import BLACKLIST
from models.login_model import login_model, auth_ns, reset_password_model,token_model,contact_model as c, googleToken_model
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


@auth_ns.route('/login')
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
            refresh_token = create_refresh_token(identity=user_role, additional_claims=additional_claims)

            return {
                'access_token': f'Bearer {access_token}',
                'refresh_token': f'Bearer {refresh_token}'
            }, 200
        else:
            return {'message': 'Invalid credentials'}, 401
@auth_ns.route('/refresh-token')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    def post(self):
        print("refresh-token")
        identity = get_jwt_identity()
        new_access_token = create_access_token(identity=identity)
        new_refresh_token = create_refresh_token(identity=identity)
        return jsonify(newToken=new_access_token, newRefreshToken=new_refresh_token)


@auth_ns.route('/continue-with-google')
class Google(Resource):
    @auth_ns.expect(googleToken_model)
    @auth_ns.response(200, 'Success', googleToken_model)
    @auth_ns.response(400, 'failed')
    def post(self):
        data = request.json
        token = data['token']

        # אימות אסימון ההתחברות של גוגל
        response = requests.get(
            f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        print(response)
        if response.status_code != 200:
            return {'error': 'Failed to fetch user profile', 'status_code': response.status_code}, 400

        profile_info = response.json()
        print(f'response.json() = {response.json()}')
        email = profile_info['email']
        name = profile_info['name']
        user = auth_service.find_user_by_email(email)

        if user is not None:
            additional_claims = {
                'role': user['role'],
                'user_id': serialize_user(user)['_id']
            }
            access_token = create_access_token(identity=user['role'], additional_claims=additional_claims)
            return {'access_token': 'Bearer ' + access_token}, 200

        # הוספת המשתמש למסד הנתונים
        user = auth_service.create_user(name, email)
        print(f'user = {user}')
        additional_claims = {
            'role': 'client',  # need a function to know if role is admin or client---!
            'user_id': serialize_user(user)['_id']
        }

        access_token = create_access_token(identity="client", additional_claims=additional_claims)
        return {'access_token': 'Bearer ' + access_token}, 200

    def options(self):
        """
        מתודת OPTIONS - מאפשרת בקשות CORS.
        """
        return {'Allow': 'POST, OPTIONS'}, 200, {

            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Credentials': 'true'

        }

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
        reset_link = f"https://kostiner-tenders.onrender.com/#/resetPasword"  # Use the identifier in the reset link
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
        return {'Allow': 'POST, OPTIONS'}, 200


    @auth_ns.expect(token_model)
    @auth_ns.response(200, 'Password reset successful')
    @auth_ns.response(400, 'Invalid token')
    @auth_ns.response(401, 'Token expired')
    @auth_ns.response(500, 'Unknown error')
    def post(self):
        data = request.json
        # token = data.get('token')
        token = data.get('access_token')
        new_password = data.get('new_password')
        print("token",token)
        print("new_password",new_password)
        result = auth_service.reset_password(token, new_password)
        if isinstance(result, tuple):
            message, status_code = result
            return {'message': message}, status_code

        return {'message': 'Unknown error occurred'}, 500

@auth_ns.route('/logout')
class Logout(Resource):
    @jwt_required()
    def options(self):
        origin = request.headers.get('Origin')
        allowed_origins = ["https://kostiner-tenders.onrender.com", "http://localhost:5174","http://localhost:5173"]

        if origin in allowed_origins:
            return {'Allow': 'POST, OPTIONS'}, 200, {
                'Access-Control-Allow-Origin': origin,
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Credentials': 'true'
            }
        else:
            return {'Allow': 'POST, OPTIONS'}, 403, {
                'Access-Control-Allow-Origin': 'null',
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

@auth_ns.route('/contact')
class Connect(Resource):
        @auth_ns.expect(c)
        @auth_ns.response(200, 'Success')
        @auth_ns.response(401, 'Unauthorized')
        def post(self):
            data = request.json
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            phone = data.get('phone')
            message_content = data.get('message')

            try:
                msg = Message('שליחת טופס יצירת קשר', sender=email, recipients=[settings.Config.MAIL_USERNAME])
                msg.body = f'Name: {first_name} {last_name}\nEmail: {email}\nPhone: {phone}\nMessage: {message_content}'
                mail.send(msg)

                user_msg = Message('תודה שפנית אלינו', sender=settings.Config.MAIL_USERNAME, recipients=[email])
                user_msg.body = 'תודה שפנית אלינו. קיבלנו את הודעתך ונחזור אליך בהקדם.'
                mail.send(user_msg)

                return {'message': 'ההודעה נשלחה בהצלחה'}, 200
            except Exception as e:
                return {'message': f'An error occurred: {str(e)}'}, 500

        def options(self):
            allowed_origins = [
                "http://localhost:5174",
                "http://localhost:5173",
                "https://kostiner-tenders.onrender.com"
            ]
            origin = request.headers.get('Origin')
            response = jsonify({})
            if origin in allowed_origins:
                response.headers['Access-Control-Allow-Origin'] = origin
            response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
