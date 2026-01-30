from pymongo import MongoClient
import os

mongo_client = None
db = None

def init_db():
    global mongo_client, db

    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DB")

    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[mongo_db]

    return db
