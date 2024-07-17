from flask_restx import Namespace, fields

nameSpace_product = Namespace(name='products', description='Products operations', path='/api')

product_model = nameSpace_product.model('Product', {
    'description': fields.String(required=True, description='Description of the product'),
    'category': fields.String(required=True, description='Category of the product'),
    'price_monthly': fields.Float(required=True, description='Price of the monthly product'),
    'price_subscription': fields.Float(required=True, description='Price of the subscription product')
})