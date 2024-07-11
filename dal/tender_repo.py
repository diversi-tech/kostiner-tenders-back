from bson import ObjectId

from dal.base_repo import base_repo

class tender_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner', 'tenders')
        print('in __init__ in trender_repo')

    def get_obj_id(self):
        return 'tender_id'

    def insert(self, data):
        print(f'in tender_repo\nin insert: len(data):{len(data)}')
        result = []
        try:
            for item in data:
                tender_id = None
                try:
                    tender_id = ObjectId(item['tender_id'])
                except Exception as e:
                    print(f"Invalid ObjectId format for tender_id: {item['tender_id']}. Error: {e}")
                    tender_id = item['tender_id']
                    continue
                if not self.collection.find_one({'tender_id': tender_id}):
                    result.append(item)
            if not result:
                print(f'if not exist new object {result}')
                raise DataAlreadyExistsError(400, "all the tenders already exists.")
            return self.collection.insert_many(result)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise e

    # def search(self, criteria):
    #     print(f"Search criteria: {criteria}")  # נדפיס את הקריטריונים כדי לוודא שהם נכונים
    #     query = self.collection.find(criteria)
    #     return list(query)

    def search(self, criteria):
        print(f"Search criteria: {criteria}")
        mongo_query = self.build_mongo_query(criteria)
        query = self.collection.find(mongo_query)
        return list(query)

    def build_mongo_query(self, criteria):
        query = {}
        if 'category' in criteria:
            query['category'] = criteria['category']
        if 'tender_name' in criteria:
            query['tender_name'] = criteria['tender_name']
        if 'date' in criteria:
            query['date'] = criteria['date']
        if 'participant_name' in criteria:
            query['details.participants.name'] = criteria['participant_name']
        return query





class DataAlreadyExistsError(Exception):
    """Exception raised when data already exists in the database."""

    def __init__(self, code=400, details="Data already exists in the database"):
        self.code = code
        self.details = details
        super().__init__(self.code, self.details)
