from flask_restx import Namespace, fields, Resource

auth_ns = Namespace('auth', description='Authentication operations')

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True, description='username'),
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password'),
    'role' : fields.String(default='user', choices=('user', 'subscriber', 'admin'))
})
token_model = auth_ns.model('Token', {
    'access_token': fields.String(description='The JWT access token')
})