# ----------------------------------------------------------
# from flask_restx import Namespace, fields

# nameSpace_payment = Namespace(name='payment',
#                             description='Payment related operations',
#                            path='/api',
#                           ordered=True)

# contact_model = nameSpace_payment.model('contact', {
#   'name': fields.String(required=True, description='Full name of the customer'),
#  'email': fields.String(required=True, description='Email address of the customer'),
# 'phone': fields.String(required=True, description='Phone number of the customer'),
# 'address': fields.String(required=True, description='Physical address of the customer'),
#  'businessID': fields.String(required=False, description='Business ID if applicable')
# })

# item_model = nameSpace_payment.model('item', {
#   'name': fields.String(required=True, description='Name of the product/service'),
#  'description': fields.String(required=False, description='Description of the product/service'),
#  'quantity': fields.Float(required=True, description='Quantity of the product/service'),
#  'price': fields.Float(required=True, description='Price per unit of the product/service'),
#  'vatIncluded': fields.Boolean(required=True, description='Whether the price includes VAT')
# })

# payment_model = nameSpace_payment.model('payment', {
#   'payments': fields.Integer(required=True, description='Number of payments'),
#  'chargeIdentifier': fields.String(required=True, description='Charge identifier'),
# 'docType': fields.Integer(required=True, description='Document type'),
# 'mail': fields.Boolean(required=True, description='Send email confirmation'),
#    'discount': fields.Float(required=False, description='Discount amount'),
#   'discountType': fields.String(required=False, description='Type of discount', enum=['percent', 'amount']),
#  'rounding': fields.Boolean(required=False, description='Apply rounding'),
# 'signDoc': fields.Boolean(required=True, description='Sign document'),
# 'details': fields.String(required=False, description='Additional details'),
# 'lang': fields.String(required=True, description='Language', default='he'),
# 'currency': fields.String(required=True, description='Currency', default='ILS'),
# 'contact': fields.Nested(contact_model, required=True, description='Contact details of the customer'),
# 'items': fields.List(fields.Nested(item_model), required=True, description='List of items in the transaction'),
# 'notifyUrl': fields.String(required=True, description='URL to notify upon transaction status change', default='https://ypay.co.il/indicator'),
# 'successUrl': fields.String(required=True, description='URL to redirect to upon successful transaction', default='https://ypay.co.il/success'),
# 'failureUrl': fields.String(required=True, description='URL to redirect to upon failed transaction', default='https://ypay.co.il/failure')
# })


from flask_restx import Namespace, fields
from flask_restx.fields import Date

nameSpace_payment = Namespace(name='payment',
                              description='Payment related operations',
                              path='/api',
                              ordered=True)

contact_model = nameSpace_payment.model('contact', {
    'email': fields.String(required=True, description='Email address of the customer', default='test@mail.com'),
    'businessID': fields.String(required=True, description='Business ID of the customer', default='040888888'),
    'name': fields.String(required=True, description='Full name of the customer', default='John Black'),
    'phone': fields.String(required=True, description='Phone number of the customer', default='09-6666660'),
    'mobile': fields.String(required=True, description='Mobile number of the customer', default='0506666660'),
    'zipcode': fields.String(required=True, description='Zipcode of the customer', default='5260170'),
    'website': fields.String(required=True, description='Website of the customer', default='www.mywebsite.co.il'),
    'address': fields.String(required=True, description='Physical address of the customer',
                             default='Hgavish 2, R’annana'),
    'comments': fields.String(required=True, description='Comments about the customer', default='Just a comment')
})

item_model = nameSpace_payment.model('item', {
    'price': fields.Float(required=True, description='Price per unit of the product/service', default=1.0),
    'quantity': fields.Float(required=True, description='Quantity of the product/service', default=1.0),
    'vatIncluded': fields.Boolean(required=True, description='Whether the price includes VAT', default=False),
    'name': fields.String(required=True, description='Name of the product/service', default='Product Name'),
    'description': fields.String(required=True, description='Description of the product/service',
                                 default='Product Description')
})

payment_model = nameSpace_payment.model('payment', {
    'payments': fields.Integer(required=True, description='Number of payments', default=1),
    'chargeIdentifier': fields.String(required=True, description='Unique charge identifier', default='1234567'),
    'docType': fields.Integer(required=True, description='Type of document to generate', default=108),
    'mail': fields.Boolean(required=True, description='Whether to send email or not', default=True),
    'discount': fields.Float(required=True, description='Discount amount', default=2.0),
    'discountType': fields.String(required=True, description='Type of discount (percent or absolute)',
                                  enum=['percent', 'absolute'], default='percent'),
    'rounding': fields.Boolean(required=True, description='Whether to round the amount or not', default=False),
    'signDoc': fields.Boolean(required=True, description='Whether to sign the document or not', default=True),
    'details': fields.String(required=True, description='Additional details about the payment', default='Few Details'),
    'lang': fields.String(required=True, description='Language of the payment page', default='he'),
    'currency': fields.String(required=True, description='Currency of the transaction', default='ILS'),
    'contact': fields.Nested(contact_model, required=True, description='Contact details of the customer'),
    'items': fields.List(fields.Nested(item_model), required=True, description='List of items in the transaction'),
    'notifyUrl': fields.String(required=True, description='URL to notify upon transaction status change',
                               default='https://kostiner-tenders.onrender.com'),
    'successUrl': fields.String(required=True, description='URL to redirect to upon successful transaction',
                                default='https://kostiner-tenders.onrender.com'),
    'failureUrl': fields.String(required=True, description='URL to redirect to upon failed transaction',
                                default='https://kostiner-tenders.onrender.com')
})

methods = nameSpace_payment.model('method', {
    'type': fields.Integer(required=True, description='Type of payment method'),
    'total': fields.Float(required=True, description='Total payment amount'),
    'date': fields.Date(required=True, description='Date format is Y-m-d. Default is current date'),

})

document_model = nameSpace_payment.model('document', {
    'docType': fields.Integer(required=True, description='Type of document to generate', default=108),
    'mail': fields.Boolean(required=True, description='Whether to send email or not', default=True),
    'discount': fields.Float(required=True, description='Discount amount', default=2.0),
    'discountType': fields.String(required=True, description='Type of discount (percent or absolute)',
                                  enum=['percent', 'absolute'], default='percent'),
    'rounding': fields.Boolean(required=True, description='Whether to round the amount or not', default=False),
    'signDoc': fields.Boolean(required=True, description='Whether to sign the document or not', default=True),
    'details': fields.String(required=True, description='Additional details about the payment', default='Few Details'),
    'lang': fields.String(required=True, description='Language of the payment page', default='he'),
    'currency': fields.String(required=True, description='Currency of the transaction', default='ILS'),
    'contact': fields.Nested(contact_model, required=True, description='Contact details of the customer'),
    'items': fields.List(fields.Nested(item_model), required=True, description='List of items in the transaction'),
    'methods': fields.Nested(methods, required=True, description='method of document')
})
