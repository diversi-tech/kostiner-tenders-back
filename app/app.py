from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
import middlewares.authorization_middleware

from controllers.controller_login import auth_ns
from controllers.user_controller import namespace as namespace_user
from controllers.tender_controller import namespace as namespace_tender
from controllers.subscription_registration_controller import nameSpace_subscription
from config.config import mail
from middlewares.blackList import check_if_token_in_blacklist

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
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='kustiner1@gmail.com', # החלף באימייל האמיתי שלך
    # MAIL_PASSWORD='m p q y j x r b b h m b o n h v' ,# החלף בסיסמא האמיתית שלך
    MAIL_PASSWORD='i a u m z l p a q x r b d v s d',
    MAIL_DEFAULT_SENDER='kustiner1@gmail.com'
)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
mail.init_app(app)
jwt = JWTManager(app)
app.before_request(middlewares.authorization_middleware.before_request_middleware())
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist_callback(jwt_header, jwt_payload):
    return check_if_token_in_blacklist(jwt_header, jwt_payload)

CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:5174"}})

api = Api()

api = Api(app, version='1.0', title='Kostiner Tender Records', description='Information from the world of auctions', authorizations=authorizations, security='jwt')

api.add_namespace(namespace_user)
api.add_namespace(namespace_tender)
api.add_namespace(auth_ns, path='/auth')
api.add_namespace(namespace_user, path='/users')
api.add_namespace(nameSpace_subscription,"/subscribertion")



if __name__ == '__main__':
    print('in app')
    app.run(debug=True)
