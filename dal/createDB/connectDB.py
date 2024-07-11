import os

from pymongo import MongoClient,errors
from dotenv import load_dotenv

load_dotenv()

def connect_to_mongodb(
        mongo_uri=f'mongodb+srv://{os.getenv("ATLAS_USER")}:{os.getenv("ATLAS_USER_PASSWORD")}@devcluster.tlutfgy.mongodb.net/?retryWrites=true&w=majority&appName=DevCluster'
):
    try:
        mongo_uri = mongo_uri
        client = MongoClient(mongo_uri)
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except errors.ConnectionError as ce:
        print(f"Connection Error: {ce}\n"
              f"Failed to connect using the provided URI: {mongo_uri}\n"
              f"Please check your username: {os.getenv('ATLAS_USER')} and password: {os.getenv('ATLAS_USER_PASSWORD')}")
        raise
    except errors.ConfigurationError as conf_err:
        print(f"Configuration Error: {conf_err}\n"
              f"Please ensure your MongoDB URI and configuration are correct.")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}\n"
              f"Please check your environment and configuration.")
        raise

