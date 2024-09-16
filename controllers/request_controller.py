from flask_jwt_extended import jwt_required, verify_jwt_in_request
from flask_restx import Resource
from flask import request, jsonify
from services import request_service
from models_swagger.request_model import namespace_request as namespace, request_model
from dal.user_repo import user_repo
from services import user_service

user_repo = user_repo()

#שליפת כל הבקשות
@namespace.route('/get-all-requests')
class GetAllRequests(Resource):
    @namespace.doc('list_request')
    @namespace.marshal_list_with(request_model)
    def get(self):
        '''get all request'''
        return request_service.get_all()

@namespace.route('/get-request-by-id/<string:request_id>')
@namespace.response(404, 'request not found')
class GetRequestById(Resource):
    @namespace.doc('get_tender')
    @namespace.marshal_with(request_model)
    def get(self, request_id):
        '''get request by Id'''
        request = request_service.get_by_id(request_id)
        if request:
            return request
        namespace.abort(404, f"request {request_id} doesn't exist")

@namespace.route('/get-all-users-requests')
class GetAllUsersRequests(Resource):
    @namespace.doc('list_request')
    @namespace.marshal_list_with(request_model)
    def get(self):
        '''get all request'''
        detail = verify_jwt_in_request()
        user_id = detail[1].get("user_id")
        return request_service.get_all_users_request(user_id)

#שליפת בקשות לא מאושרות
@namespace.route('/get-unapproved-requests')
class GetUnapprovedRequests(Resource):
    @namespace.doc('list_unapproved_request')
    @namespace.marshal_list_with(request_model)
    def get(self):
        '''get unapproved requests'''
        unapproved_requests = request_service.get_unapproved_requests()
        if not unapproved_requests:
            return {'message': 'No unapproved requests found'}, 404

        return unapproved_requests, 200

#הוספת בקשה
@namespace.route('/post-request/<string:tender_name>')
class PostRequest(Resource):
    @namespace.doc('create_request')
    @namespace.marshal_with(request_model)
    @jwt_required()
    def post(self, tender_name):
        '''create a new request'''
        detail = verify_jwt_in_request()
        user_id = detail[1].get("user_id")
        result, status = request_service.create(tender_name, user_id)
        return result, status

#מחיקת בקשה
@namespace.route('/delete-request/<string:request_id>')
class DeleteRequestById(Resource):
    @namespace.doc('delete_request')
    def delete(self, request_id):
        '''delete request by Id'''
        count_delete = request_service.delete(request_id)
        if count_delete is not None and count_delete > 0:
            return 'The request deleted successfully'
        namespace.abort(404, f"request {request_id} doesn't exist")


@namespace.route('/approve-request/<string:request_id>')
class ApproveRequest(Resource):
    @namespace.doc('approve_request')
    def put(self, request_id):
        '''approve a request by Id'''
        print("request_id",request_id)
        result = request_service.approve_request(request_id)
        if result:
            return 'Request approved successfully', 200
        return {'message': 'Request not found or already approved'}, 404


@namespace.route('/paid_up/<string:request_id>')
class PaidUp(Resource):
    namespace.doc('paid_up_request')
    def options(self, request_id):
        '''paid up request'''
        return request_service.paid_up(request_id)


namespace.add_resource(PostRequest, '/post-request/<string:tender_name>')
namespace.add_resource(GetAllRequests, '/get-all-requests')
namespace.add_resource(GetUnapprovedRequests, '/get-unapproved-requests')
namespace.add_resource(DeleteRequestById, '/delete-request/<string:request_id>')
namespace.add_resource(ApproveRequest, '/approve-request/<string:request_id>')


