from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# PHASE 1: AUTHENTICATION MODELS
class UserAuth(BaseModel):
    """Model for receiving login and registration data from Angular."""
    username: str
    password: str
    role: Optional[str] = "user"  # Default to 'user', can be 'developer'

class UserInDB(BaseModel):
    """Model for storing user records in the app_db.users collection."""
    username: str
    password_hash: str
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# ==========================================
# PHASE 2: DATA EXTRACTION MODELS (NEW)
# ==========================================
class ExtractionRequest(BaseModel):
    """
    Standard model for extraction requests. 
    This is what the validator and main.py were looking for.
    """
    sourceType: str  # structured, semi-structured, or unstructured
    tags: List[str]
    db_host: str
    db_port: int
    db_name: str

class UnstructuredResult(BaseModel):
    """Model for a single extracted record from a PDF."""
    tag: str
    value: str
    confidence_score: float = 0.0

# PHASE 3: CONNECTION HISTORY MODELS
class SavedConnection(BaseModel):
    """Model for saving database credentials to the app_db.saved_connections collection."""
    username: str # To link the history to a specific user
    pipeline_type: str  # structured, semi-structured, or unstructured
    host: str
    port: str
    database_name: str
    db_username: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ExtractionHistory(BaseModel):
    """Model for logging every extraction attempt in app_db.extraction_history."""
    username: str
    pipeline_type: str
    host: str
    port: str
    status: str  # success or error