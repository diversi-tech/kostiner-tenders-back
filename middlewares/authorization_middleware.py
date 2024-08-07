from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request

def before_request_middleware():
    def middleware():
        excluded_endpoints = {
            'static', 'specs', 'doc', 'root', 'restx_doc.static',
            'auth_login', 'auth_password_reset_request', 'auth_password_reset_response','auth_google',
            'password_reset_request', 'password_reset_response', 'user_post_user',
            'payment_create_payment', 'payment_documents',
            # יש לבטל אפשרות זו בפרודקשיין ->
            'user_get_all_users', 'refresh_token', 'auth_connect', 'auth_refresh_token'
        }

        print(f"Request endpoint: {request.endpoint}")
        #print(f"Excluded endpoints: {excluded_endpoints}")

        if request.endpoint not in excluded_endpoints:
            try:
                verify_jwt_in_request()
            except Exception as e:
                print(f"JWT verification error: {str(e)}")
                return jsonify({"msg": "Unauthorized"}), 401
    return middleware

