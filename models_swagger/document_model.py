from flask_restx import Namespace, fields


nameSpace_document = Namespace(name='document',
                              description='document related operations',
                              path='/api',
                              ordered=True)

contact_model = nameSpace_document.model('contact', {
    'email': fields.String(required=True, description='Email address of the customer', default='test@mail.com'),
    'businessID': fields.String(required=True, description='Business ID of the customer', default='040888888'),
    'name': fields.String(required=True, description='Full name of the customer', default='John Black'),
    'phone': fields.String(required=True, description='Phone number of the customer', default='09-6666660'),
    'mobile': fields.String(required=True, description='Mobile number of the customer', default='0506666660'),
    'zipcode': fields.String(required=True, description='Zipcode of the customer', default='5260170'),
    'website': fields.String(required=True, description='Website of the customer', default='www.mywebsite.co.il'),
    'address': fields.String(required=True, description='Physical address of the customer', default='Hgavish 2, R’annana'),
    'comments': fields.String(required=True, description='Comments about the customer', default='Just a comment')
})

item_model = nameSpace_document.model('item', {
    'price': fields.Float(required=True, description='Price per unit of the product/service', default=1.0),
    'quantity': fields.Float(required=True, description='Quantity of the product/service', default=1.0),
    'vatIncluded': fields.Boolean(required=True, description='Whether the price includes VAT', default=False),
    'name': fields.String(required=True, description='Name of the product/service', default='Product Name'),
    'description': fields.String(required=True, description='Description of the product/service',
                                 default='Product Description')
})

methods = nameSpace_document.model('method', {
    'type': fields.Integer(required=True, description='Type of payment method'),
    'total': fields.Float(required=True, description='Total payment amount'),
    'date': fields.Date(required=True, description='Date format is Y-m-d. Default is current date')

})

document_model = nameSpace_document.model('document', {
    'docType': fields.Integer(required=True, description='Type of document to generate', default=108),
    'mail': fields.Boolean(required=True, description='Whether to send email or not', default=True),
    'discount': fields.Float(required=True, description='Discount amount', default=2.0),
    'discountType': fields.String(required=True, description='Type of discount (percent or absolute)', enum=['percent', 'absolute'], default='absolute'),
    'rounding': fields.Boolean(required=True, description='Whether to round the amount or not', default=False),
    'signDoc': fields.Boolean(required=True, description='Whether to sign the document or not', default=True),
    'details': fields.String(required=True, description='Additional details about the payment', default='Few Details'),
    'lang': fields.String(required=True, description='Language of the payment page', default='he'),
    'currency': fields.String(required=True, description='Currency of the transaction', default='ILS'),
    'contact': fields.Nested(contact_model, required=True),
    'items': fields.List(fields.Nested(item_model), required=True, description='List of items in the transaction'),
    'methods': fields.Nested(methods, required=True, description='method of document')
})



