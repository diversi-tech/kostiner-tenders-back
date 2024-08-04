from flask import Flask, request, jsonify
from flask_restx import Api, Resource, Namespace, abort

from models_swagger.document_model import document_model
from models_swagger.payment_model import nameSpace_payment, payment_model
from services.payment_service import payment_service


@nameSpace_payment.route('/')
class Hello(Resource):
    def post(self):
        return {'hello'}, 200


@nameSpace_payment.route('/document')
@nameSpace_payment.expect(document_model)
class Documents(Resource):
    def post(self):
        document_data = request.json
        print("documents")
        try:
            access_token = payment_service.get_access_token(self)
            print(access_token)
            response = payment_service.create_document(self, access_token, document_data)
            return response, 200
        except Exception as e:
            abort(500, str(e))


@nameSpace_payment.route('/create-payment')
class CreatePayment(Resource):
    @nameSpace_payment.expect(payment_model)
    def post(self):
        payment_data = request.json
        # ביצוע הבדיקות הנדרשות על הנתונים כאן
        try:
            access_token = payment_service.get_access_token(self)
            print(access_token)
            response = payment_service.purchase_product(self, access_token, payment_data)
            print(f'response Ypay: {response}')
            return response
        except Exception as e:
            abort(500, str(e))
        # # שליחת הנתונים ל-YPAY API
        # ypay_response = send_to_ypay_api(payment_data)
        #
        # if ypay_response['status'] == 'success':
        #     return jsonify({
        #         'message': 'Payment created successfully',
        #         'ypay_data': ypay_response
        #     }), 200
        # else:
        #     return jsonify({
        #         'message': 'Payment creation failed',
        #         'ypay_data': ypay_response
        #     }), 400

# def send_to_ypay_api(payment_data):
#   import requests

#  url = 'https://ypay.example.com/api/payments'
# headers = {
#    'Content-Type': 'application/json'
# }
# response = requests.post(url, json=payment_data, headers=headers)

# return response.json()

# @nameSpace_payment.route('create-document')
# class Documents:
#     def post(self):
#         return True
