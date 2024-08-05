from datetime import datetime
import jwt
from flask_jwt_extended import verify_jwt_in_request, jwt_required
from flask_restx import Resource, fields
from flask import request, jsonify
from pymongo.results import InsertManyResult
from werkzeug.datastructures import FileStorage
# from flask_restx.errors import abort
from flask import abort
from werkzeug.exceptions import NotFound


from dal.tender_repo import DataAlreadyExistsError
from services import tender_service
from services import user_service
from models_swagger.tender_model import namespace_tender as namespace, tender_model


@namespace.route('/get-all-tenders')
class GetAllTenders(Resource):
    @namespace.doc(params={
        'search date': 'search date of the range (format: YYYY-MM-DD)'
    })
    @namespace.response(401, 'Invalid token')
    @namespace.response(400, 'Invalid date')
    @jwt_required()
    def get(self):
        '''get all tenders'''
        try:
            detail = verify_jwt_in_request()
            user_id = detail[1].get("user_id")
            user = user_service.get_by_id(user_id)
            search_date = request.args.get('search date')
            print(f'tender controller search date: {search_date}')
            list_obj_tenders = \
                tender_service.convert_datetime_to_str(
                    tender_service.convert_objectid_to_str(
                        tender_service.get_all(user, search_date)))
            return list_obj_tenders, 200
        except NotFound as e:
            error_message = {'message': str(e)}
            print(f'except NotFound as e: {error_message}')
            namespace.abort(404, message=f'{str(e)}')
        except (ValueError, TypeError) as e:
            print(f'except (ValueError, TypeError) as e: {e}')
            namespace.abort(400, message=f'{str(e)}')
        except jwt.ExpiredSignatureError:
            namespace.abort(401, "Token has expired")
        except jwt.InvalidTokenError:
            namespace.abort(401, "Invalid token")
        except Exception as e:
            print(f'tender controller Exception msg: {e}')
            namespace.abort(400, str(e))


@namespace.route('/get-id-tender/<string:tender_id>')
@namespace.response(404, 'tender not found')
class GetTenderById(Resource):
    @namespace.doc('get_tender')
    @namespace.marshal_with(tender_model)
    def get(self, tender_id):
        '''get tender by Id'''
        tender = tender_service.get_by_id(tender_id)
        if tender:
            return tender
        namespace.abort(404, f"tender {tender_id} doesn't exist")


@namespace.route('/post-upload-csv')
class CSVUpload(Resource):
    upload_parser = namespace.parser()
    upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='CSV or Excel file')

    @namespace.expect(upload_parser)
    def post(self):
        global result
        if 'file' not in request.files:
            abort(400, "No file part in the request")
        args = self.upload_parser.parse_args()
        file = args['file']
        print(f'tender controller args: {args}')
        print(f'tender controller file: {file}')

        if file.filename == '':
            abort(400, "No selected file")

        if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
            abort(400, "File is not a CSV or Excel")

        try:
            if file.filename.endswith('.csv'):
                result = tender_service.insert_from_csv(file)

            elif file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
                result = tender_service.insert_from_excel(file)

            if isinstance(result, InsertManyResult):
                return 'The documents were successfully entered', 201

        except ValueError as e:
            abort(400, str(e))
        except DataAlreadyExistsError as e:
            abort(e.code, e.details)
        except Exception as e:
            abort(500, str(e))
        return {"message": "Unexpected error occurred"}, 500


@namespace.route('/update-tender/<string:tender_id>')
class PutTenderById(Resource):
    @namespace.doc('update_tender')
    @namespace.expect(tender_model)
    @namespace.marshal_with(tender_model)
    def put(self, tender_id, namespace):
        '''update tender by id'''
        update_tender = request.json
        result = tender_service.update(tender_id, update_tender)
        if result.modified_count > 0:
            updated_tender = tender_service.get_by_id(tender_id)
            return updated_tender
        namespace.abort(404, f"tender {tender_id} doesn't exist")


@namespace.route('/delete-tender/<string:tender_id>')
@namespace.response(204, 'No Content')
class DeleteTenderById(Resource):
    @namespace.doc('delete_tender')
    def delete(self, tender_id):
        '''delete tender by Id'''
        count_delete = tender_service.delete(tender_id)
        if count_delete is not None and count_delete > 0:
            return 'The tender deleted successfully'
        namespace.abort(404, f"tender {tender_id} doesn't exist")


@namespace.route('/search')
class TenderSearch(Resource):
    @namespace.doc('search_tender')
    @namespace.expect(namespace.model('SearchCriteria', {
        'body_name': fields.String(required=False, description='body_names'),
        'tender_number_name': fields.String(required=False, description='tender_number'),
        'published_date': fields.Date(required=False, description='published_date'),
        'submission_date': fields.Date(required=False, description='submission_date'),
        "category": fields.List(fields.String, required=False, description='category'),
        'winner_name': fields.String(required=False, description='winner_name'),
        'details_winner': fields.String(required=False, description='details_winner'),
        'participants': fields.List(fields.String, required=False, description='participants'),
        'amount_bid': fields.Float(required=False, description='amount_bid'),
        'estimate': fields.Float(required=False, description='estimate')
    }))
    @namespace.marshal_list_with(tender_model)
    @namespace.response(401, 'Invalid token')
    @namespace.response(400, 'Invalid date')
    @jwt_required()
    def post(self):
        '''Search for tenders'''
        try:
            detail = verify_jwt_in_request()
            user_id = detail[1].get("user_id")
            user = user_service.get_by_id(user_id)
            print(f'tender controller search date: {user}')
            criteria = request.json
            if not criteria:
                namespace.abort(400, "Search criteria cannot be empty")

            # Convert string dates to datetime objects if provided
            if 'published_date' in criteria:
                try:
                    criteria['published_date'] = datetime.strptime(criteria['published_date'], '%Y-%m-%d')
                except ValueError:
                    namespace.abort(400, "Invalid published_date format")

            if 'submission_date' in criteria:
                try:
                    criteria['submission_date'] = datetime.strptime(criteria['submission_date'], '%Y-%m-%d')
                except ValueError:
                    namespace.abort(400, "Invalid submission_date format")

            results = tender_service.search(user, criteria)
            print(f'results in controller {results}')
            return results, 200

        except ValueError as e:
            abort(400, str(e))
        except jwt.ExpiredSignatureError:
            abort(401, "Token has expired")
        except jwt.InvalidTokenError:
            abort(401, "Invalid token")
        except Exception as e:
            print(f'tender controller Exception msg: {e}')
            abort(400, str(e))


namespace.add_resource(TenderSearch, '/search')
namespace.add_resource(GetAllTenders, '/get-all-tenders')
namespace.add_resource(GetTenderById, '/get-id-tender/<string:tender_id>')
namespace.add_resource(CSVUpload, '/post-upload-csv')
namespace.add_resource(PutTenderById, '/update-tender/<string:tender_id>')
namespace.add_resource(DeleteTenderById, '/delete-tender/<string:tender_id>')
