from pymongo import MongoClient
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    db = client["nosql_db"]
    # List collections to prove connection
    print("Collections found:", db.list_collection_names())
except Exception as e:
    print("MongoDB Connection Failed:", e)