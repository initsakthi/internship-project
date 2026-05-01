from elasticsearch import Elasticsearch
from pymongo import MongoClient

# 1. Connect to Services
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])
mongo_client = MongoClient("mongodb://localhost:27017/")

# Configuration
db_name = "nosql_db"
mongo_db = mongo_client[db_name]

def sync_all_tags():
    # 2. Reset the Elasticsearch Index for a fresh start
    if es.indices.exists(index=db_name):
        es.indices.delete(index=db_name)
    es.indices.create(index=db_name)
    print(f"Index '{db_name}' recreated.")

    # 3. Iterate through every collection in your MongoDB
    for collection_name in mongo_db.list_collection_names():
        if collection_name in ['admin', 'local', 'config']: continue
        
        collection = mongo_db[collection_name]
        # Get one sample document to identify all available fields
        sample_doc = collection.find_one()
        
        if sample_doc:
            # Prepare a mapping of every key found in the document
            tags_to_index = {}
            for key in sample_doc.keys():
                if key == '_id': continue # Skip MongoDB internal ID
                
                # Store the key in lowercase to make search case-insensitive
                tags_to_index[key.lower()] = "exists"
            
            # Add the source metadata so the backend knows the table/collection name
            tags_to_index["collection_metadata"] = collection_name
            
            # 4. Push this map to Elasticsearch
            es.index(index=db_name, document=tags_to_index)
            print(f"Synced tags for collection: {collection_name}")

if __name__ == "__main__":
    sync_all_tags()
    print("\nUniversal indexing complete. All tags from all collections are now searchable.")