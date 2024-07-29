from dal.product_repo import  product_repo
from services.base_service import base_service


class product_service(base_service):
        def __init__(self):
            self.repo = product_repo()
            print(f'in __init__ in product_service')
            super().__init__(product_repo())

    # def get_all_products(self):
    #     return self.repo.get_all_product()

        def get_by_category(self, category):
            return self.repo.get_by_category(category)


        def delete(self, category):
            return self.repo.delete_by_category(category)

        def create(self, data):
            # ולידציה לשדות המחיר
            if not isinstance(data.get('price_subscription'), (int, float)) or not isinstance(data.get('price_monthly'), (int, float)):
                abort(400, 'price_subscription ו-price_monthly חייבים להיות מספרים תקינים.')

            return self.repo.insert(data)

        def update(self, category, data):
            # ולידציה לשדות המחיר
            if not isinstance(data.get('price_subscription'), (int, float)) or not isinstance(data.get('price_monthly'),(int, float)):
                abort(400, 'price_subscription ו-price_monthly חייבים להיות מספרים תקינים.')

            return self.repo.update_by_category(category, data)
