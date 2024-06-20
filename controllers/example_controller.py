from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, fields
from services.example_service import dataService
from models.example_model import nameSpace, data_model
from flask import Flask, request, jsonify

data_service = dataService()

@nameSpace.route('/')
class dataList(Resource):
    @nameSpace.doc('list_data',security='jwt')
    @nameSpace.marshal_list_with(data_model)
    @jwt_required()
    def get(self):
        '''here write description of method'''
        return data_service.get_all_datas()

    @nameSpace.doc('create_data',security='jwt')
    @nameSpace.expect(data_model)
    @nameSpace.marshal_with(data_model, code=201)
    @jwt_required()
    def post(self):
        '''Create a new data entry'''
        data = nameSpace.payload
        return data_service.create_data(data), 201

@nameSpace.route('/<string:data_id>')
class dataDetail(Resource):
    @nameSpace.doc('get_data')
    @nameSpace.marshal_with(data_model)
    @nameSpace.doc(security='jwt')
    @jwt_required()
    def get(self, data_id):
        '''Get data entry by ID'''
        current_user = get_jwt_identity()
        data = data_service.get_data_by_id(data_id)
        if data:
            return data
        nameSpace.abort(404, f"Data {data_id} doesn't exist")

    @nameSpace.doc('update_data')
    @nameSpace.expect(data_model)
    @nameSpace.marshal_with(data_model)
    @nameSpace.doc(security='jwt')
    @jwt_required()
    def put(self, data_id):
        '''Update data entry by ID'''
        current_user = get_jwt_identity()
        data = nameSpace.payload
        updated_data = data_service.update_data(data_id, data)
        if updated_data:
            return updated_data
        nameSpace.abort(404, f"Data {data_id} doesn't exist")

    @nameSpace.doc('delete_data')
    @nameSpace.response(204, 'Data deleted')
    @nameSpace.doc(security='jwt')
    @jwt_required()
    def delete(self, data_id):
        '''Delete data entry by ID'''
        current_user = get_jwt_identity()
        if data_service.delete_data(data_id):
            return '', 204
        nameSpace.abort(404, f"Data {data_id} doesn't exist")

# Other controllers methods
