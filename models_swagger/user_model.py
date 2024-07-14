from flask_restx import Namespace, fields

nameSpace_user = Namespace(name=str('user'),
                           description='users',
                           path='/api',
                           ordered=True
                           )

purchase_model = nameSpace_user.model('purchase_history', {
    'purchase_id': fields.String(required=True, description='purchase_id'),
    'product_name': fields.String(required=True, description='product_name'),
    'purchase_date': fields.Date(required=True, description='purchase_date'),
    'amount': fields.Integer(required=True, description='purchase_amount')
})

#subscription_one_time = nameSpace_user.model('one_time', {
 #   'subscription_id': fields.String(required=True, description='subscription_id'),
  #  'type': "one_time",
   # 'tender_id': fields.String(required=True, description='tender_id'),
    #'purchase_date': fields.Date(required=True, description='purchase_date')

#})


subscription = nameSpace_user.model('subscription', {
    'subscription_id': fields.String(required=True, description='subscription_id'),
    'type': "recurring",
    'plan': fields.String(required=True, description='plan'),
    'start_date': fields.Date(required=True, description='start_date'),
    'end_date': fields.Date(required=True, description='end_date'),
    'categories': fields.List(fields.String(required=True, description='category'))
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
    'purchase_history': fields.List(fields.Nested(purchase_model), required=True, description='purchase_history'),
    #'subscriptions': fields.List(fields.Nested(subscription_one_time), required=True, description='subscriptions')
    #'subscriptions': fields.Nested(subscription, required=True, description='subscriptions')

})

# or fields.Nested(subscription)