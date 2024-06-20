from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from pymongo import MongoClient

from controllers.controller_login import auth_ns
from controllers.example_controller import nameSpace

authorizations = {
    'jwt': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'chgc#sd1'  # Change to your actual secret key
jwt = JWTManager(app)

CORS(app)
api = Api(app, version='1.0', title='Kostiner Tender Records', description='Information from the world of auctions'
          , authorizations=authorizations, security='jwt')

api.add_namespace(nameSpace,path='/data')
api.add_namespace(auth_ns, path='/auth')


if __name__ == '__main__':
    app.run(debug=True)
