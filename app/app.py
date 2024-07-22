from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from flask_restx import Api
from middlewares.authorization_middleware import before_request_middleware
from controllers.login_controller import auth_ns
from controllers.user_controller import namespace as namespace_user
from controllers.tender_controller import namespace as namespace_tender
from config.config import mail

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
api = Api(app, version='1.0', title='Kostiner Tender Records', description='Information from the world of auctions', authorizations=authorizations, security='jwt')
api.add_namespace(namespace_user)
api.add_namespace(namespace_tender)
api.add_namespace(auth_ns, path='/auth')

if __name__ == '__main__':
    print('in app')
    app.run(debug=True)
