from pymongo import MongoClient
from elasticsearch import Elasticsearch

# 1. Connect to services
mongo_client = MongoClient("mongodb://127.0.0.1:27017/")
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def seed_complete_database(db_name, emp_id, dept, proj, skills, date, score):
    # --- MongoDB Setup ---
    db = mongo_client[db_name]
    collection = db["employees_collection"]
    collection.delete_many({}) 
    
    # Insert a document with ALL the fields you want to extract
    full_data = {
        "employee_id": emp_id,
        "department": dept,
        "project": proj,
        "skill_set": skills,
        "joining_date": date,
        "performance_score": score
    }
    collection.insert_one(full_data)
    print(f" MongoDB: '{db_name}' fully seeded with all fields.")

    # --- Elasticsearch Metadata Mapping ---
    # This MUST list every field you want the backend to recognize
    metadata = {
        "employee_id": "exists",
        "department": "exists",
        "project": "exists",
        "skill_set": "exists",
        "joining_date": "exists",
        "performance_score": "exists",
        "collection_metadata": "employees_collection" 
    }
    
    # Overwrite the index in ES
    es.index(index=db_name, document=metadata)
    print(f"✅ Elasticsearch: Index '{db_name}' now supports ALL 6 tags.")

# Seed the Primary Database
seed_complete_database(
    "nosql_db", 
    "EMP_PRI_101", "Engineering", "Alpha", "Angular, Python", "2026-01-01", "9.5"
)

# Seed the Secondary Database (with different data for demo)
seed_complete_database(
    "secondary_nosql", 
    "EMP_SEC_999", "R&D", "Gamma", "MongoDB, ES", "2026-02-15", "8.8"
)

print("\n All 6 fields are now active on both hosts!")