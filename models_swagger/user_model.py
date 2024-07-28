from flask_restx import Namespace, fields

nameSpace_user = Namespace(name=str('user'),
                           description='users',
                           path='/api',
                           ordered=True
                           )

purchase_model = nameSpace_user.model('purchase_history', {
    'plan_type': fields.String(required=True, description='Subscription name'),
    'purchase_start_date': fields.Date(required=True, description='Subscription start date'),
    'purchase_end_date': fields.Date(required=True, description='Subscription end date'),
    'categories': fields.List(fields.String, required=False, description='Subscription categories'),
    'amount': fields.Integer(required=True, description='purchase_amount')
})

subscription = nameSpace_user.model('subscription', {
    'plan_type': fields.String(required=True, description='plan', default='Subscription', choices=('Tender report', 'One-time category', 'Subscription')),
    'start_date': fields.Date(required=True, description='start_date'),
    'end_date': fields.Date(required=True, description='end_date'),
    'categories': fields.List(fields.String, required=False, description='category'),
    'amount': fields.Integer(required=True, description='purchase_amount')
}
                                    )

user_data_model = nameSpace_user.model('user', {
    'user_id': fields.String(readOnly=True, required=True,
                             description='The unique identifier of a user, User MongoDB Object ID'),
    'user_name': fields.String(required=True, description='user_name of the user'),
    'password': fields.String(required=True, description='password of user'),
    'email': fields.String(required=True, description='email of the user'),
    'role': fields.String(required=True, description='role of the user'),
    'first_name': fields.String(required=True, description='first_name of the user'),
    'last_name': fields.String(required=True, description='last_name of the user'),
    'business_name': fields.String(required=True, description='business_name of the user'),
    'purchase_history': fields.List(fields.Nested(purchase_model, required=True, description='purchase_history'), required=True, description='purchase_history'),
    'subscriptions': fields.Nested(subscription, required=True, description='subscriptions')
})
