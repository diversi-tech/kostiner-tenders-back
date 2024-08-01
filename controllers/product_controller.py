from flask import request
from flask_restx import Resource
from pymongo.results import UpdateResult
from werkzeug.exceptions import BadRequest

from services import product_service
from models_swagger.product_model import nameSpace_product as namespace, product_model
from services.auth_service import policy_required


@namespace.route('/get-all-products')
class GetAllProducts(Resource):
    @namespace.doc('list_products')
    @namespace.marshal_list_with(product_model)
    @jwt_required()
    def get(self):
        '''get all product'''
        return product_service.get_all()


@namespace.route('/get-product-by-category/<string:category>')
@namespace.response(404, 'product not found')
class GetProductByCategory(Resource):
    @namespace.doc('get_product')
    @namespace.marshal_with(product_model)
    def get(self, category):
        '''get product by category'''
        product = product_service.get_by_category(category)
        if product:
            return product
        namespace.abort(404, f"product {category} doesn't exist")


@namespace.route('/post-product')
class PostProduct(Resource):
    @namespace.doc('create_product')
    @namespace.expect(product_model)
    @namespace.marshal_with(product_model, 201)
    @policy_required('admin')
    def post(self):
        '''create a new product'''
        new_product = request.json
        result = product_service.create(new_product)
        print('====in product controller in post=====')
        print(f'result', {result})
        print(f'type(result) {type(result)}')
        print(f'isinstance(result, BadRequest) {isinstance(result, BadRequest)}')
        if not isinstance(result, BadRequest):
            print('in if')
            return product_service.get_by_category(new_product['category'])
        namespace.abort(result.code, result.description)


@namespace.route('/put-product/<string:category>')
class UpdateProduct(Resource):
    @namespace.doc('update_product')
    @namespace.expect(product_model)
    @namespace.marshal_with(product_model)
    @policy_required('admin')
    def put(self, category):
        '''update product by category'''
        update_product = request.json
        result = product_service.update(category, update_product)
        print('====in product controller in put=====')
        print(f'type(result) {type(result)}')
        print(f'result {result}')
        if isinstance(result, UpdateResult) and result.matched_count > 0:
            updated_product = product_service.get_by_category(update_product['category'])
            print(f'updated_product {updated_product}')
            return updated_product
        elif isinstance(result, BadRequest):
            print(f'{type(result)}')
            print(f'result {result}')
            print(f'{result.code}')
            namespace.abort(result.code, result.description)
        namespace.abort(result.code, result.description)


@namespace.route('/delete-product/<string:category>')
class DeleteProductByCategory(Resource):
    @namespace.doc('delete_product')
    @policy_required('admin')
    def delete(self, category):
        '''delete product by category'''
        count_delete = product_service.delete(category)
        if count_delete is not None and count_delete > 0:
            return 'The product deleted successfully'
        namespace.abort(404, f"product {category} doesn't exist")


namespace.add_resource(GetAllProducts, '/get-all-products')
namespace.add_resource(PostProduct, '/post-product')
namespace.add_resource(GetProductByCategory, '/get-product-by-category/<string:category>')
namespace.add_resource(UpdateProduct, '/put-product/<string:category>')
namespace.add_resource(DeleteProductByCategory, '/delete-product/<string:category>')
