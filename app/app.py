from functools import wraps

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from flask_restx import Api

from authorization_middleware import before_request_middleware
from config import mail

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'chgc#sd1'  # Change to your actual secret key

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
# app.config['JWT_COOKIE_SECURE'] = False
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# app.config['JWT_CSRF_CHECK_FORM'] = True

jwt = JWTManager(app)
# הגדרות Flask-Mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com', # שדרג לשימוש בשרת האימייל שלך
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='kustiner1@gmail.com', # החלף באימייל האמיתי שלך
    MAIL_PASSWORD='m p q y j x r b b h m b o n h v' ,# החלף בסיסמא האמיתית שלך
    MAIL_DEFAULT_SENDER= 'kustiner1@gmail.com'
)

mail.init_app(app)
jwt = JWTManager(app)
app.before_request(before_request_middleware())

CORS(app, resources={r"/*": {
    "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
    "supports_credentials": True,
    "allow_headers": ["Content-Type", "Authorization"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}})
api = Api()

api = Api(app, version='1.0', title='Kostiner Tender Records', description='Information from the world of auctions', authorizations=authorizations, security='jwt')

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS,DELETE,PUT')
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# def jwt_required_from_cookie(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         try:
#             # שליפת העוגיות מהבקשה
#             cookies = request.cookies
#
#             # קבלת הטוקן מתוך העוגיה
#             access_token = cookies.get('access_token')
#
#             if access_token:
#                 # הגדרת הכותרת Authorization עם הטוקן מתוך העוגיה
#                 request.headers['Authorization'] = f'Bearer {access_token}'
#                 verify_jwt_in_request()  # אימות הטוקן
#                 return fn(*args, **kwargs)
#             else:
#                 return jsonify({"msg": "Missing access token"}), 401
#         except Exception as e:
#             return jsonify({"msg": "Token verification failed", "error": str(e)}), 401
#
#     return wrapper
from controllers.controller_login import auth_ns
from controllers.example_controller import nameSpace
from controllers.user_controller import namespace as nameSpace_user

api.add_namespace(nameSpace,path='/data')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(nameSpace_user, path='/users')


# for rule in app.url_map.iter_rules():
#     print(rule.endpoint, rule)
if __name__ == '__main__':
    app.run(debug=True)
