from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request

def before_request_middleware():
    def middleware():
        excluded_endpoints = {
            'static', 'specs', 'doc', 'root', 'restx_doc.static',
            'auth_login', 'auth_password_reset_request'
        }
        if request.endpoint not in excluded_endpoints:
            try:
                verify_jwt_in_request()
            except Exception as e:
                return jsonify({"msg": "Unauthorized"}), 401
    return middleware