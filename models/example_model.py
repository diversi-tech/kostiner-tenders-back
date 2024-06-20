# from flask_restx import Namespace, fields
#
# nameSpace = Namespace(name=str('<nameController = data>'),
#                       description='here write description on namespace = controller',
#                       path='/api/data',
#                       ordered=True
#                       )
#
# data_model = nameSpace.model('data', {
#     'id': fields.Integer(readOnly=True, description='The unique identifier of a data'),
#     'name': fields.String(required=True, description='name of the data'),
#     'description': fields.String(required=True, description='description of data'),
#     'size': fields.String(required=True, description='size of the data'),
# })
from flask_restx import Namespace, fields, Resource

# Create a namespace for your API
nameSpace = Namespace('example', description='Example Namespace')

# Define a model for your data
data_model = nameSpace.model('Data', {
    'id': fields.String(required=True, description='Data identifier'),
    'first_name': fields.String(required=True, description='Name of the data'),
    'last_name': fields.String(required=True, description='Value of the data'),
    'telephone_number': fields.Integer(required=True, description='Value of the data'),
})

