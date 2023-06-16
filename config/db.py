from pymongo import MongoClient
from config.settings import mongodb_uri, port

conn = MongoClient(mongodb_uri, port)