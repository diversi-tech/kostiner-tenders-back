from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def before_request_middleware():

    def middleware():
        excluded_endpoints = {
            'static', 'specs', 'doc', 'root', 'restx_doc.static',
            'auth_login', 'auth_password_reset_request','auth_password_reset_response',
            'password_reset_request','password_reset_response','http://localhost:5000/auth/login'
        }
        print("Request endpoint:", request.endpoint)
        print("Request path:", request.path)
        print("Request method:", request.method)
        print("Request headers:", request.headers)
        print("Request cookies:", request.cookies)
        if request.endpoint not in excluded_endpoints:
            try:
                verify_jwt_in_request(optional=True)
                current_user = get_jwt_identity()
                if not current_user:
                    return jsonify({"msg": "Missing or invalid token"}), 401
            except Exception as e:
                print(f"JWT verification error: {str(e)}")
                return jsonify({"msg": "Unauthorized"}), 401
    return middleware