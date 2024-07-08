from flask_restx import Namespace, fields

nameSpace = Namespace(name=str('<nameController = data>'),
                      description='here write description on namespace = controller',
                      path='/api/data',
                      ordered=True
                      )

data_model = nameSpace.model('data', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a data'),
    'name': fields.String(required=True, description='name of the data'),
    'description': fields.String(required=True, description='description of data'),
    'size': fields.String(required=True, description='size of the data'),
})
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
