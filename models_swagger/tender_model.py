from flask_restx import Namespace, fields, namespace

namespace_tender = Namespace(name=str('tender'),
                      description='tenders',
                      path='/api',
                      ordered=True
                      )

# Define the main model
tender_model = namespace_tender.model('Tender', {
    'tender_id': fields.String(required=True, description='tender id'),
    'body_name': fields.String(required=True, description='body_names'),
    'tender_number': fields.String(required=True, description='tender_number'),
    'tender_name': fields.String(required=True, description='tender_name'),
    'published_date': fields.Date(required=True, description='published_date'),
    'submission_date': fields.Date(required=True, description='submission_date'),
    "category": fields.String(required=True, description='category'),
    'winner_name': fields.String(required=True, description='winner_name'),
    'details_winner': fields.String(required=True, description='details_winner'),
    'participants': fields.String(required=True, description='participants'),
    'amount_bid': fields.Float(required=True, description='amount_bid'),
    'estimate': fields.Float(required=True, description='estimate')
})