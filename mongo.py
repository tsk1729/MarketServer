import urllib
from datetime import datetime
from pymongo import MongoClient
from typing import Any
import certifi
from pymongo.collection import Collection  # <- corrected import

username = "sandeep"
password = "peedn@sT7"
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

MONGO_STRING = (
    f"mongodb+srv://{encoded_username}:{encoded_password}"
    "@owlit-cluster.s4cvt.mongodb.net/?retryWrites=true&w=majority&appName=owlit-cluster"
)
DATABASE_NAME = "owlit"


class MongoRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create(self, data: dict) -> Any:
        return self.collection.insert_one(data)

    def read(self, query: dict) -> Any:
        return self.collection.find_one(query)

    def read_all(self, query=None) -> iter:
        if query is None:
            query = {}
        return self.collection.find(query)

    def update(self, query: dict, update_data: dict) -> Any:
        return self.collection.update_one(query, {"$set": update_data})

    def delete(self, query: dict) -> Any:
        return self.collection.delete_one(query)

    def delete_all(self, query: dict) -> Any:
        return self.collection.delete_many(query)

    def upsert(self, query: dict, update_data: dict) -> Any:
        return self.collection.update_one(query, {"$set": update_data}, upsert=True)

    def update_with_ops(self, filter_query: dict, update_operations: dict) -> Any:
        return self.collection.update_many(filter_query, update_operations)

    def add_to_array_field(self, query: dict, array_field: str, item_data: dict) -> Any:
        update_data = {"$addToSet": {array_field: item_data}}
        return self.collection.update_one(query, update_data, upsert=True)

    def remove_from_array_field(self, query: dict, array_field: str, item_data: dict) -> Any:
        update_data = {"$pull": {array_field: item_data}}
        return self.collection.update_one(query, update_data)


class JobRepository:
    def __init__(self, collection: Collection):
        self.collection = collection

    def add_job(self, id: str, user_id: str, func_name: str, args: dict, target_time: datetime):
        job_data = {
            "_id": id,
            "user_id": user_id,
            "func_name": func_name,
            "args": args,
            "target_time": target_time,
        }
        return self.collection.insert_one(job_data)

    def get_job(self, job_id: str):
        return self.collection.find_one({"_id": job_id})

    def update_job(self, job_id: str, updates: dict):
        return self.collection.update_one({"_id": job_id}, {"$set": updates})

    def delete_job(self, job_id: str):
        return self.collection.delete_one({"_id": job_id})

    def get_all_jobs(self):
        return list(self.collection.find({}))

    def upsert_job(self, job_id: str, job_data: dict):
        return self.collection.update_one({"job_id": job_id}, {"$set": job_data}, upsert=True)


class RepositoryManager:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri, tlsCAFile=certifi.where())
        self.db = self.client[db_name]
        self.creators = MongoRepository(self.db["influencers"])
        self.companies = MongoRepository(self.db["brands"])
        self.company_posts = MongoRepository(self.db["brand_posts"])




repo_manager = RepositoryManager(uri=MONGO_STRING, db_name=DATABASE_NAME)
