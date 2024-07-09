import json
import os

from pymongo import errors
from dotenv import load_dotenv

from dal.createDB.connectDB import connect_to_mongodb

load_dotenv()

mongo_uri = f'mongodb+srv://{os.getenv("ATLAS_USER")}:{os.getenv("ATLAS_USER_PASSWORD")}@devcluster.tlutfgy.mongodb.net/?retryWrites=true&w=majority&appName=DevCluster'
db_name = os.getenv("DATABASE_NAME")
collections = json.loads(os.getenv("COLLECTIONS"))
def create_database_and_collections(client, db_name, collections):
    try:
        db = client[db_name]
        for collection_name in collections:
            if collection_name in db.list_collection_names():
                print(f"Collection '{collection_name}' already exists.")
            else:
                try:
                    print(f"Creating collection '{collection_name}'...")
                    db.create_collection(collection_name)
                    print(f"Collection '{collection_name}' created successfully.")
                except errors.CollectionInvalid as ci:
                    print(f"Collection Error: {ci}")
                    raise
                except Exception as e:
                    print(f"An error occurred while creating collection '{collection_name}': {e}")
                    raise
        print(f"Database '{db_name}' and collections were created successfully.")
    except KeyError as ke:
        print(f"KeyError: One or more parameters are incorrect: {ke}")
        raise
    except Exception as ex:
        print(f"A general error occurred while creating database and collections: {ex}")
        raise



def main_create_db_collections():
    client = connect_to_mongodb(mongo_uri)
    db_name = os.getenv("DATABASE_NAME")
    collections = json.loads(os.getenv("COLLECTIONS"))
    try:
        if db_name in client.list_database_names():
            print(f"Database '{db_name}' already exists.")
            db = client[db_name]
            create_database_and_collections(client, db_name, collections)
        else:
            print(f"Creating database '{db_name}'...")
            create_database_and_collections(client, db_name, collections)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        client.close()

if __name__ == "__main__":
    main_create_db_collections()

