from datetime import datetime

from bson import ObjectId
from pymongo import errors

from dal.base_repo import base_repo


class tender_repo(base_repo):
    def __init__(self):
        super().__init__('Kostiner', 'tenders')
        print('in __init__ in trender_repo')

    def get_obj_id(self):
        return 'tender_id'

    def get_name_string(self):
        return 'tender_name'

    def get_id_by_name(self, name):
        print(f'tender_repo get_id_by_name')
        try:
            result = self.collection.find_one({'body_name': name}, sort=[('published_date', -1)])
            if result is None:
                raise ValueError(f"לא קיים מכרז עם השם {name}")
            result['tender_id'] = str(result['tender_id'])
            tender_id = result['tender_id']
            return tender_id
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            raise ValueError(f"שגיאה בחיבור ל-MongoDB: {e}")

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

    def get_by_category(self, category, search_date, start_date, end_date):
        query = {
            '$and': [
                {'category': category},
                {'published_date': {'$gte': start_date}},
                {'published_date': {'$lte': end_date}}
            ]
        }
        if search_date > start_date:
            query['$and'].append({'published_date': {'$lte': search_date}})
            print(query['$and'][3])
        list_category = (self.collection
                         .find(query)
                         .sort('published_date', -1)
                         .limit(100))
        result_list = list(list_category)
        return result_list

    def search(self, criteria):
        print(f"Search criteria: {criteria}")
        mongo_query = self.build_mongo_query(criteria)
        print(f"MongoDB query: {mongo_query}")
        query = self.collection.find(mongo_query)
        results = list(query)
        print(f"Query results: {results}")
        return results

    def build_mongo_query(self, criteria):
        print(f"in build_mongo_query")
        query = {}

        if 'body_name' in criteria:
            query['body_name'] = criteria['body_name']
        if 'tender_number_name' in criteria:
            query['tender_number_name'] = criteria['tender_number_name']
        if 'published_date' in criteria:
            query['published_date'] = criteria['published_date']
        if 'submission_date' in criteria:
            query['submission_date'] = criteria['submission_date']
        if 'category' in criteria and criteria['category']:
            query['category'] = {"$in": criteria['category']}
        if 'winner_name' in criteria:
            query['winner_name'] = criteria['winner_name']
        if 'details_winner' in criteria:
            query['details_winner'] = criteria['details_winner']
        if 'participants' in criteria and criteria['participants']:
            query['participants'] = {"$in": criteria['participants']}
        if 'amount_bid' in criteria:
            query['amount_bid'] = criteria['amount_bid']
        if 'estimate' in criteria:
            query['estimate'] = criteria['estimate']

        return query


class DataAlreadyExistsError(Exception):
    """Exception raised when data already exists in the database."""

    def __init__(self, code=400, details="Data already exists in the database"):
        self.code = code
        self.details = details
        super().__init__(self.code, self.details)
