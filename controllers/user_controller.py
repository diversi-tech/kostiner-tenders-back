from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from flask import request
from bson import ObjectId

# from models import user
from models_swagger.user_model import nameSpace_user as namespace, user_model
from services import user_service
from services.auth_service import policy_required


@namespace.route('/')
class userList(Resource):
    def __init__(self, *args, **kwargs):
        super(userList, self).__init__(*args, **kwargs)
        self.user_service = user_service

    @namespace.doc('list_user',security='jwt')
    @namespace.marshal_list_with(user_model)
    @jwt_required()
    @policy_required('user')
    def get(self):
        '''get all users'''
        return self.user_service.get()

    @namespace.doc('create_user')
    @namespace.expect(user_model)
    def post(self):
        '''create a new user'''
        print('post in user_controller')
        new_user = request.json
        result = self.user_service.insert(new_user)
        print(result.acknowledged)
        return {'message': f'User created successfully'}, 201


@namespace.route('/<string:user_id>')
@namespace.response(404, 'user not found')
class user(Resource):
    def __init__(self, *args, **kwargs):
        super(user, self).__init__(*args, **kwargs)
        self.user_service = user_service

    @namespace.doc('get_user')
    # @namespace.marshal_with(user_model)
    @jwt_required()
    @policy_required('user')
    def get(self, user_id):
        '''get user by Id'''
        print('user_controller // def get(self, user_id):')
        user = self.user_service.get_by_id(user_id)
        if user:
            return user
        namespace.abort(404, f"user {user_id} doesn't exist")


    @namespace.doc('update_user')
    @namespace.expect(user_model)
    @namespace.marshal_with(user_model)
    def put(self, user_id):
        '''update user by id'''
        print('user_controller //def put(self, user_id)')
        update_user = request.json
        result = self.user_service.update(user_id, update_user)
        if result.modified_count > 0:
            updated_user = self.user_service.get_by_id(user_id)
            return updated_user
        namespace.abort(404, f"user {user_id} doesn't exist")
    @namespace.doc('delete_user')
    @namespace.marshal_with(user_model)
    def delete(self, user_id):
        '''delete user by Id'''
        count_delete = self.user_service.delete(user_id)
        if count_delete is not None and count_delete > 0:
            return count_delete
        namespace.abort(404, f"user {user_id} doesn't exist")