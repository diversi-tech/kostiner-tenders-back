from flask_restx import Namespace, fields, namespace

namespace_request = Namespace(name=str('Request'),
                              description='requests', path='/api',
                              ordered=True)

request_model = namespace_request.model('Request', {
    'request_id': fields.String(required=True, description='Request id'),
    'tender_id': fields.String(required=True, description='tender id'),
    'tender_name': fields.String(required=True, description='Name of tender'),
    'approved': fields.Boolean(required=True, description='approved true or false', default= False),
    'date': fields.Date(required=True, description=' Date of Submission'),
    'userID': fields.String(required=True, description=' ID of user')


})
