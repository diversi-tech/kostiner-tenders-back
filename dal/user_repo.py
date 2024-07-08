from bson import ObjectId
from pymongo import MongoClient,errors
from dotenv import load_dotenv
import os
load_dotenv()


from dal.createDB.connectDB import connect_to_mongodb

client = connect_to_mongodb(f'mongodb+srv://{os.getenv("ATLAS_USER")}:{os.getenv("ATLAS_USER_PASSWORD")}@devcluster.tlutfgy.mongodb.net/')
user_collection = client['Kostiner']['users']

class user_repo:
    def get(self):
        # print("repo -get",list(user_collection.find()))
        try:
            return list(user_collection.find())
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return []

    def get_by_id(self, user_id):
        try:
            print(type(ObjectId(user_id)))
            print('user_repo get_by_id(self, user_id):')
            return user_collection.find_one({'user_id': ObjectId(user_id)})
        except errors.InvalidId as e:
            print(f"Invalid ID: {e}")
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None


    def insert(self, data):
        try:
            print('post in user_repo')
            data['user_id'] = ObjectId()
            result = user_collection.insert_one(data)
            return result
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None

    def update(self, user_id, data):
        try:
            print('user_repo // def update(self, user_id, data)')
            result = user_collection.update_one({'user_id': ObjectId(user_id)}, {'$set' : data})
            print(result)
            return result
        except errors.InvalidId as e:
            print(f'Imvakidid: {e}')
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None

    def delete(self, user_id):
        try:
            result = user_collection.delete_one({'user_id': ObjectId(user_id)})
            return result.deleted_count
        except errors.InvalidId as e:
            print(f"Invalid ID: {e}")
            return None
        except errors.PyMongoError as e:
            print(f"An error occurred: {e}")
            return None
