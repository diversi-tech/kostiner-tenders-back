import uuid
from datetime import datetime, timedelta

from flask_restx import Namespace, fields, Resource

auth_ns = Namespace('auth', description='Authentication operations')

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='username'),
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password'),
    'role': fields.String(default='user', choices=('user', 'subscriber', 'admin'))
})
token_verify_model = auth_ns.model('TokenVerify', {
    'identifier': fields.String(required=True, description='Unique identifier for the reset token')
})
token_model = auth_ns.model('Token', {
    'access_token': fields.String( required=True,description='The JWT access token'),
    'new_password': fields.String(required=True, description='New password'),
})

reset_password_verify_model = {
    'identifier': str(uuid.uuid4()),  # Unique identifier for the reset request
    'email': 'user@example.com',  # User's email address
    'username': 'user123',  # User's username
    'token': 'jwt_encoded_token',  # The JWT token
    'created_at': datetime.utcnow(),  # Timestamp when the reset request was created
    'expires_at': datetime.utcnow() + timedelta(minutes=30)  # Expiration time
}
reset_password_model = auth_ns.model('ResetPassword', {
    'email': fields.String(required=True, description='User email address'),
    'username':fields.String(requests=True, desctiption='username')
})

contact_model = auth_ns.model('Contact', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'phone': fields.String(required=True, description='Phone number'),
    'message': fields.String(required=True, description='Message content')
})