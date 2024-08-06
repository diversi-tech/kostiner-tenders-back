from bson import ObjectId
from pymongo import MongoClient, errors
from dotenv import load_dotenv
import os

load_dotenv()

from dal.createDB.connectDB import connect_to_mongodb

client = connect_to_mongodb(
    f'mongodb+srv://{os.getenv("ATLAS_USER")}:{os.getenv("ATLAS_USER_PASSWORD")}@devcluster.tlutfgy.mongodb.net/')


class base_repo:
    def __init__(self, db_name, collection_name):
        self.collection = client[db_name][collection_name]
        print(f'in __init__ base_repo')

    def get_obj_id(self):
        raise NotImplementedError("Subclasses should implement this method.")
    def get_name_string(self):
            raise NotImplementedError("Subclasses should implement this method.")

    # @requird_policy('user')
    def get(self):
        try:
            print(f'base_repo get')
            return list(self.collection.find())
        except errors.PyMongoError as e:
            return []

    def get_by_id(self, object_id):
        try:
            obj_id = self.get_obj_id()
            result = self.collection.find_one({obj_id: ObjectId(object_id)})
            return result

        except errors.InvalidId as e:
            print(f"Invalid ID: {e}")
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None

    def get_by_string(self, object_id):
        try:
            search = self.get_name_string()
            return self.collection.find_one({search: object_id})
        except errors.InvalidId as e:
            print(f"Invalid ID: {e}")
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None

    def insert(self, data):
        try:
            data[self.get_obj_id()] = ObjectId()
            result = self.collection.insert_one(data)
            return self.get_by_id(data[self.get_obj_id()])
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None

    def update(self, object_id, data):
        try:
            obj_id = self.get_obj_id()
            data.pop(obj_id, None)
            result = self.collection.update_one({obj_id: ObjectId(object_id)}, {'$set': data})
            return result
        except errors.InvalidId as e:
            print(f"Invalid ID: {e}")
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def delete(self, object_id):
        try:
            obj_id = self.get_obj_id()
            result = self.collection.delete_one({obj_id: ObjectId(object_id)})
            return result.deleted_count
        except errors.InvalidId as e:
            print(f"Invalid ID: {e}")
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None
