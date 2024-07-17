from flask import request
from flask_restx import Resource

from services import product_service
from models_swagger.product_model import nameSpace_product as namespace, product_model

product_service = product_service


@namespace.route('/get-all-products')
class GetAllProducts(Resource):
    @namespace.doc('list_products')
    @namespace.marshal_list_with(product_model)
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
    @namespace.marshal_with(product_model)
    def post(self):
        '''create a new product'''
        new_product = request.json
        result = product_service.create(new_product)
        print(result)
        return result, 201


@namespace.route('/put-product/<string:category>')
class UpdateProduct(Resource):
    @namespace.doc('update_product')
    @namespace.expect(product_model)
    @namespace.marshal_with(product_model)
    def put(self, category):
        '''update product by category'''
        update_product = request.json
        result = product_service.update(category, update_product)
        if result is not None and result.modified_count > 0:
            updated_product = product_service.get_by_category(category)
            return updated_product
        else:
            namespace.abort(404, f"product {category} doesn't exist")


@namespace.route('/delete-product/<string:category>')
class DeleteProductByCategory(Resource):
    @namespace.doc('delete_product')
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
