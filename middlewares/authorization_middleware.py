# from flask import jsonify, request
# from flask_jwt_extended import verify_jwt_in_request
#
#
# def before_request_middleware():
#     def middleware():
#         excluded_endpoints = {
#             'static', 'specs', 'doc', 'root', 'restx_doc.static',
#             'auth_login', 'auth_password_reset_request','auth_password_reset_response','api_user_post_user'
#             'password_reset_request','password_reset_response', 'http://localhost:5000/auth/login'
#         }
#
#         if request.endpoint not in excluded_endpoints:
#             try:
#                 verify_jwt_in_request()
#             except Exception as e:
#                 print(f"JWT verification error: {str(e)}")
#                 return jsonify({"msg": "Unauthorized"}), 401
#     return middleware
#
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request

def before_request_middleware():
    def middleware():
        excluded_endpoints = {
            'static', 'specs', 'doc', 'root', 'restx_doc.static',
            'auth_login', 'auth_password_reset_request', 'auth_password_reset_response',
            'password_reset_request', 'password_reset_response', 'user_post_user',
            # יש לבטל אפשרות זו בפרודקשיין ->
            'user_get_all_users'
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

