import threading
from functools import wraps
from typing import Callable
import pymongo
from pymongo import MongoClient


class CacheMongo:
    data: dict
    client: MongoClient
    db: pymongo.database.Database
    collection: pymongo.collection.Collection

    def new(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Cache, cls).new(cls)
        return cls.instance

    def __init__(self) -> None:
        self.data = {}
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["cachemongodb"]
        self.collection = self.db["cachedata"]

    def cache(self, func) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.__name__ not in self.data:
                self.data[func.__name__] = {}

            name = self.args_name(*args, **kwargs)
            if name not in self.data[func.__name__]:
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    raise e

                threading.Thread(
                    target=self.save_data_to_db, args=(func.__name__, name, result)
                ).start()
                self.data[func.__name__][name] = result
            else:
                result = self.data[func.__name__][name]

            return result

        return wrapper

    def args_name(self, *args, **kwargs) -> str:
        name = ""
        for arg in args:
            name += f"{hash(arg)}:{arg}-"

        for key, value in kwargs.items():
            name += f"{key}:{value}-"

        return name

    def save_data_to_db(self, func_name, key, value):
        data_to_save = {"func_name": func_name, "key": key, "value": value}
        self.collection.insert_one(data_to_save)