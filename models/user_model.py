from flask_restx import Namespace, fields

nameSpace_user = Namespace(name=str('user'),
                      description='users',
                      path='/api/user',
                      ordered=True
                      )

user_model = nameSpace_user.model('user', {
    'user_id': fields.String(required=True, description='The unique identifier of a user, User MongoDB Object ID'),
    'user_name': fields.String(required=True, description='user_name of the user'),
    'password': fields.String(required=True, description='password of user'),
    'email': fields.String(required=True, description='email of the user'),
    'role': fields.String(required=True, description='role of the user'),
    'first_name': fields.String(required=True, description='first_name of the user'),
    'last_name': fields.String(required=True, description='last_name of the user'),
    'business_name': fields.String(required=True, description='business_name of the user'),
})
