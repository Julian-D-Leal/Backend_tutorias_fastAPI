from pymongo import MongoClient
from config.config import settings

client = MongoClient(settings.DATABASE_URL, settings.PORT, serverSelectionTimeoutMS=5000)

try:
    conn = client.server_info()
    print(f'Connected to MongoDB {conn.get("version")}')
except Exception:
    print('Connection to MongoDB failed')

db = client[settings.MONGO_INITDB_DATABASE]

