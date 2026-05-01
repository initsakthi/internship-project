from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import shutil
import os
import asyncio
import traceback

# ==========================================
# SURGICAL PIPELINE IMPORTS
# ==========================================
# 1. Legacy Archive
from pipelines.pipeline_legacy import process_document as legacy_process

# 2. New Modular Orchestrator (Updated for Page Tracking)
from pipelines import unstructured_v2 

# 3. Background Automation Service
from file_watcher import watcher

from auth.routes import router as auth_router

app = FastAPI(title="Unified Data Extraction Pipeline (V2 Architecture)")
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Setup for Unstructured file storage
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==========================================
# CORS CONFIGURATION (UPDATED)
# ==========================================
# Using wildcard allow_origins temporarily to ensure frontend connectivity 
# and prevent data hiding in the browser dashboard.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# BACKGROUND SERVICE INITIALIZATION
# ==========================================
@app.on_event("startup")
async def startup_event():
    """Starts the Folder Watcher in the background when the server boots."""
    print(f"🚀 Initializing Background Watcher on: {UPLOAD_DIR}")
    asyncio.create_task(watcher.start_watching(UPLOAD_DIR))

class ExtractionRequest(BaseModel):
    sourceType: str
    tags: List[str]
    db_host: str
    db_port: int
    db_name: str

# ==========================================
# 1. CONNECTION TESTING (UNTOUCHED)
# ==========================================
@app.post("/test-connection")
async def test_connection(request: ExtractionRequest):
    if request.sourceType == "structured":
        try:
            conn = mysql.connector.connect(
                user='root', password='', host=request.db_host, 
                port=request.db_port, database=request.db_name, connection_timeout=5
            )
            conn.close()
            return {"status": "success", "message": "MySQL Connected"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    elif request.sourceType == "semi-structured":
        try:
            client = MongoClient(f"mongodb://{request.db_host}:{request.db_port}/", serverSelectionTimeoutMS=2000)
            client.admin.command('ping') 
            return {"status": "success", "message": f"MongoDB {request.db_name} Connected"}
        except Exception as e:
            return {"status": "error", "message": f"MongoDB Error: {str(e)}"}
            
    return {"status": "error", "message": "Invalid Source Type"}

# ==========================================
# 2. DB EXTRACTION (STRUCTURED & SEMI-STRUCTURED - UNTOUCHED)
# ==========================================
@app.post("/extract")
async def extract_data(request: ExtractionRequest):
    results = []
    
    if request.sourceType == "structured":
        try:
            conn = mysql.connector.connect(
                user='root', password='', host=request.db_host, 
                port=request.db_port, database=request.db_name
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SHOW TABLES")
            tables = [list(row.values())[0] for row in cursor.fetchall()]
            
            for tag in request.tags:
                found = False
                for table in tables:
                    cursor.execute(f"DESCRIBE {table}")
                    columns = [col['Field'].lower() for col in cursor.fetchall()]
                    
                    if tag.lower() in columns:
                        cursor.execute(f"SELECT {tag} FROM {table} WHERE {tag} IS NOT NULL")
                        data_list = cursor.fetchall()
                        for data in data_list:
                            results.append({
                                "tag": tag, 
                                "value": str(data[tag]), 
                                "sourceTable": table,
                                "confidence_score": 100
                            })
                            found = True
                if not found:
                    results.append({"tag": tag, "value": "N/A", "sourceTable": "N/A", "confidence_score": 0})
            
            cursor.close()
            conn.close()
            return {"status": "success", "records": results}
        except Exception as e:
            return {"status": "error", "message": f"SQL Error: {str(e)}"}

    elif request.sourceType == "semi-structured":
        try:
            mongo_client = MongoClient(f"mongodb://{request.db_host}:{request.db_port}/")
            db = mongo_client[request.db_name]
            es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

            for raw_tag in request.tags:
                tag = raw_tag.strip().lower()
                search_query = {"query": {"exists": {"field": tag}}}
                
                try:
                    es_result = es.search(index=request.db_name, body=search_query)
                    if es_result['hits']['total']['value'] > 0:
                        source_col = es_result['hits']['hits'][0]['_source'].get('collection_metadata')
                        if source_col:
                            cursor = db[source_col].find()
                            for doc in cursor:
                                if tag in doc and doc[tag] is not None:
                                    results.append({
                                        "tag": raw_tag,
                                        "value": str(doc[tag]),
                                        "sourceTable": f"{request.db_name}.{source_col}",
                                        "confidence_score": 100
                                    })
                    else:
                        results.append({"tag": raw_tag, "value": "N/A", "sourceTable": "N/A", "confidence_score": 0})
                except Exception:
                    results.append({"tag": raw_tag, "value": "Mapping Missing", "sourceTable": "N/A", "confidence_score": 0})

            return {"status": "success", "records": results}
        except Exception as e:
            return {"status": "error", "message": f"NoSQL Error: {str(e)}"}

    return {"status": "error", "message": "Invalid Source Type"}

# ==========================================
# 3. UNSTRUCTURED EXTRACTION (UPDATED PATH)
# ==========================================
@app.post("/extract-unstructured")
async def upload_document(
    file: UploadFile = File(...),
    tags: str = Form(...),
    use_v2: bool = Form(True) 
):
    try:
        # 1. Save uploaded file to the local directory
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Parse tags from comma-separated string
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        
        if use_v2:
            print(f" Calling Modular Local LLM Orchestrator for: {file.filename}")
            #  EXECUTE NEW PIPELINE (Supports Page Tracking)
            results = await unstructured_v2.run_pipeline(file_path, tag_list)
        else:
            print(f" Falling back to Legacy Pipeline for: {file.filename}")
            results = legacy_process(file_path, tag_list)
        
        # 3. RETURN RESULTS DIRECTLY TO FRONTEND
        # This ensuring the dictionary with "records" is sent back to Angular.
        return results
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)