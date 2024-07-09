from flask_restx import Namespace, fields

nameSpace = Namespace(name=str('<nameController = data>'),
                      description='here write description on namespace = controller',
                      path='/api/data',
                      ordered=True
                      )

data_model = nameSpace.model('data', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a data'),
    'name': fields.String(required=True, description='name of the data'),
    'description': fields.String(required=True, description='description of data'),
    'size': fields.String(required=True, description='size of the data'),
})
