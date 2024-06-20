# from flask_restx import Namespace, Resource, fields
# from flask import request
# from flask_jwt_extended import create_access_token
#
# from models.example_model import login_model
# from services.auth_service import AuthRepo
#
#
#
# auth_service = AuthRepo()
#
# @auth_ns.route('/login')
# class Login(Resource):
#     @auth_ns.expect(login_model)
#     def post(self):
#         '''User login and token generation'''
#         data = request.json
#         username = data.get('username')
#         password = data.get('password')
#
#         if auth_service.verify_user(username, password):
#             access_token = create_access_token(identity={'username': username})
#             return {'access_token': access_token}, 200
#         else:
#             return {'message': 'Invalid credentials'}, 401
# from flask_restx import Namespace, Resource, fields
# from flask import request, jsonify
# from flask_jwt_extended import create_access_token, get_jwt_identity
#
# from models.login_model import login_model, auth_ns,token_model
# from services.auth_service import AuthService
#
#
# auth_service = AuthService()
#
# @auth_ns.route('/login')
# class Login(Resource):
#     @auth_ns.expect(login_model)
#     @auth_ns.response(200, 'Success', token_model)
#     @auth_ns.response(401, 'Unauthorized')
#     def post(self):
#         '''User login and token generation'''
#         data = request.json
#         username = data.get('username')
#         password = data.get('password')
#         print("username", username)
#
#         if auth_service.verify_user(username, password):
#             access_token = create_access_token(identity={'username': username})
#             return {'access_token': 'Bearer ' + access_token}, 200
#         else:
#             return {'message': 'Invalid credentials'}, 401
        # if auth_service.verify_user(username, password):
        #     print("username",username)
        #     access_token = create_access_token(identity={'username': username,'role':'client'})
        #     return {'access_token': 'Bearer ' + access_token}, 200
        # else:
        #     return {'message': 'Invalid credentials'}, 401
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import create_access_token

from models.login_model import login_model, auth_ns, token_model
from services.auth_service import AuthService

auth_service = AuthService()

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Success', token_model)
    @auth_ns.response(401, 'Unauthorized')
    def post(self):
        '''User login and token generation'''
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if auth_service.verify_user(username, password):
            access_token = create_access_token(identity={'username': username})
            return {'access_token': 'Bearer ' + access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

    # return jsonify(msg="Access granted to protected route"), 200
