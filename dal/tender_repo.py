from bson import ObjectId

from dal.base_repo import base_repo

class tender_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner', 'tenders')
        print('in __init__ in trender_repo')

    def get_obj_id(self):
        return 'tender_id'
    def get_name_string(self):
            return 'tender_name'

    def insert_csv(self, data):
        print(f'tender_repo insert: len(data):{len(data)}')
        result = []
        try:
            for item in data:
                print(f'tender repo item: {item}')
                print(f'tender repo item: {item["tender_number_name"]}')
                if not self.collection.find_one({'tender_number_name': item['tender_number_name']}):
                    print(f'tender repo if not self.collection.find_one')
                    result.append(item)
            if not result:
                print(f'if not exist new object {result}')
                raise DataAlreadyExistsError(400, "all the tenders already exists.")
            return self.collection.insert_many(result)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise e

class DataAlreadyExistsError(Exception):
    """Exception raised when data already exists in the database."""
    def __init__(self, code=400, details="Data already exists in the database"):
        self.code = code
        self.details = details
        super().__init__(self.code, self.details)