<<<<<<< HEAD
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

app.config.update(
    MAIL_SERVER='smtp.gmail.com', # שדרג לשימוש בשרת האימייל שלך
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='kustiner1@gmail.com', # החלף באימייל האמיתי שלך
    MAIL_PASSWORD='m p q y j x r b b h m b o n h v' ,# החלף בסיסמא האמיתית שלך
    MAIL_DEFAULT_SENDER= 'kustiner1@gmail.com'
)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
mail.init_app(app)
jwt = JWTManager(app)
app.before_request(before_request_middleware())

CORS(app, supports_credentials=True)
api = Api()

api = Api(app, version='1.0', title='Kostiner Tender Records', description='Information from the world of auctions', authorizations=authorizations, security='jwt')


from controllers.controller_login import auth_ns
from controllers.example_controller import nameSpace
from controllers.user_controller import namespace as nameSpace_user

api.add_namespace(nameSpace,path='/data')
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(nameSpace_user, path='/users')


# for rule in app.url_map.iter_rules():
#     print(rule.endpoint, rule)
=======
from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from controllers.example_controller import nameSpace

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Kostiner Tender Records', description='Information from the world of auctions')

api.add_namespace(nameSpace)

>>>>>>> fab2a8b2527d0c9a0bddc2a0f26c15ef35e2626e
if __name__ == '__main__':
    app.run(debug=True)
