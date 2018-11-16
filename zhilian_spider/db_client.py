from config import config
from pymongo import MongoClient


class MongoDbClient():
    def __init__(self):
        self.db_client = MongoClient("mongodb://{user}:{pwd}@{host}:{port}/{db}".format(**config.mongo_server))
        self.db = config.mongo_server["db"]
        pass

    def insert_job(self, dict_item):
        return self.db_client[self.db]["jobs"].insert_one(dict_item)

    def insert_company(self, dict_item):
        return self.db_client[self.db]["company"].insert_one(dict_item)

    def insert_relation(self, dict_item):
        return self.db_client[self.db]["relation"].insert_one(dict_item)

    def find_company_by_url(self, url_str):
        return self.db_client[self.db]["company"].find_one({"url": url_str})

    def find_job_by_url(self, url_str):
        return self.db_client[self.db]["jobs"].find_one({"url": url_str})

    def find_relation_by_urls(self, job_url, company_url):
        return self.db_client[self.db]["relation"].find_one({"job_url": job_url, "company_url": company_url})


mongo_client = MongoDbClient()
