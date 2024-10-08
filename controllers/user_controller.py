from bson import ObjectId
from bson.errors import InvalidId
from flask_jwt_extended import jwt_required
from flask_restx import Resource, abort
from flask import request
from services import user_service
from models_swagger.user_model import nameSpace_user as namespace, user_data_model



# @namespace.route('/get-all-users')
# class GetAllUsers(Resource):
#     @namespace.doc('list_user')
#     # @namespace.marshal_list_with(user_data_model)
#     @jwt_required()
#     def get(self):
#         '''get all users'''
#         print(f'user controller get')
#         users = user_service.get_all()
#         for user in users:
#             user_service.validate_user(user)
#             continue
#         return user_service.get_all()

@namespace.route('/get-all-users')
class GetAllUsers(Resource):
    @namespace.doc('list_user')
    @jwt_required()
    def get(self):
        '''get all users'''
        print(f'user controller get')
        users_list = user_service.get_all()

        # Helper function to convert ObjectId to string and remove _id field
        def process_user(user):
            # Remove _id field
            if '_id' in user:
                del user['_id']
            # Convert ObjectId fields to strings
            for key, value in user.items():
                if isinstance(value, ObjectId):
                    user[key] = str(value)
                elif isinstance(value, dict):
                    user[key] = process_user(value)
                elif isinstance(value, list):
                    user[key] = [process_user(v) if isinstance(v, dict) else v for v in value]
            return user

        # Process each user in the list
        processed_users_list = [process_user(user) for user in users_list]

        print(f'processed_users_list= {processed_users_list}')
        for user in processed_users_list:
            if 'user_id' in user:
                print(user['user_id'])
            if 'user_name' in user:
                print(user['user_name'])
        return processed_users_list


@namespace.route('/get-id-user/<string:user_id>', methods=['GET', 'OPTIONS'])
@namespace.response(404, 'user not found')
class GetUserById(Resource):
    @namespace.doc('get_user')
    @namespace.marshal_with(user_data_model)
    def get(self, user_id):
        '''get user by Id'''
        try:
            ObjectId(user_id)
        except InvalidId:
            abort(400, "The entered value is not of type ObjectId")
        user = user_service.get_by_id(user_id)
        if user:
            user_service.validate_user(user)
            return user
        namespace.abort(404, f"user {user_id} doesn't exist")

    def options(self, user_id):
        origin = request.headers.get('Origin')
        allowed_origins = ["https://kostiner-tenders.onrender.com", "http://localhost:5174", "http://localhost:5173"]

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


@namespace.route('/post-user')
class PostUser(Resource):
    @namespace.doc('create_user')
    @namespace.expect(user_data_model)
    @namespace.marshal_with(user_data_model)
    def post(self):
        '''create a new user'''
        new_user = request.json
        print(f'user controller new_user: {new_user}')
        result = user_service.create(new_user)
        user_service.validate_user(result)
        return result, 201


@namespace.route('/put-user/<string:user_id>')
class PutUserById(Resource):
    @namespace.doc('update_user')
    @namespace.expect(user_data_model)
    @namespace.marshal_with(user_data_model)
    def put(self, user_id):
        '''update user by id'''
        print("1")
        update_user = request.json
        print(update_user)
        # user_service.validate_user(update_user)
        try:
            result = user_service.update(user_id, update_user)
            print(f'result = {result}')
            print(f'result.modified_count = {result.modified_count}')
            if result.modified_count > 0:
                updated_user = user_service.get_by_id(user_id)
                return updated_user
            else:
                abort(404, f"user {user_id} doesn't exist")
        except ValueError as e:
            abort(400, str(e))
        except Exception as e:
            print(f'user controller put type(e) {type(e)}')



@namespace.route('/delete-user/<string:user_id>')
class DeleteUserById(Resource):
    @namespace.doc('delete_user')
    def delete(self, user_id):
        '''delete user by Id'''
        count_delete = user_service.delete(user_id)
        if count_delete is not None and count_delete > 0:
            return 'The user deleted successfully'
        namespace.abort(404, f"user {user_id} doesn't exist")

namespace.add_resource(GetAllUsers, '/get-all-users')
namespace.add_resource(PostUser, '/post-user')
namespace.add_resource(GetUserById, '/get-id-user/<string:user_id>')
namespace.add_resource(PutUserById, '/put-user/<string:user_id>')
namespace.add_resource(DeleteUserById, '/delete-user/<string:user_id>')