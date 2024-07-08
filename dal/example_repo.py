# from config import db
#
# data_collection = db['<nameCollection>']
from config import db


class dataDAL:
    def __init__(self):
        # Initialize the connection to MongoDB or any other data source
        self.collection = db['users']

    def get_all_datas(self):
        data_list = list(self.collection.find({}, {'_id': 0}))
        return data_list

    def create_data(self, data):
        self.collection.insert_one(data)
        return data

    def get_data_by_id(self, data_id):
        return self.collection.find_one({'id': data_id}, {'_id': 0})

    def update_data(self, data_id, data):
        result = self.collection.update_one({'id': data_id}, {'$set': data})
        if result.modified_count:
            return self.get_data_by_id(data_id)
        return None

    def delete_data(self, data_id):
        result = self.collection.delete_one({'id': data_id})
        return result.deleted_count > 0




    # Other DAL methods
