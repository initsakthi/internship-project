from fastapi import APIRouter, HTTPException
from database.mongodb import db
from database.models import UserAuth
from .utils import hash_password, verify_password
from datetime import datetime

router = APIRouter()

@router.post("/register")
async def register(user: UserAuth):
    # 1. Check if user already exists
    existing_user = await db.users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # 2. Prepare data with hashed password and initial login count
    user_dict = {
        "username": user.username,
        "password_hash": hash_password(user.password),
        "role": user.role, 
        "login_count": 0,
        "created_at": datetime.utcnow()
    }
    
    await db.users.insert_one(user_dict)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserAuth):
    # 1. Find user by username
    db_user = await db.users.find_one({"username": user.username})
    
    # 2. Verify password
    if not db_user or not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # 3. Role validation
    if db_user["role"] != user.role:
        raise HTTPException(
            status_code=403, 
            detail=f"Access Denied: Your account is registered as a {db_user['role']}."
        )
    
    # 4. Increment login count in MongoDB
    new_count = db_user.get("login_count", 0) + 1
    await db.users.update_one(
        {"username": user.username},
        {"$set": {"login_count": new_count}}
    )
    
    return {
        "username": db_user["username"],
        "role": db_user["role"],
        "login_count": new_count
    }

# --- NEW ENDPOINT FOR DEVELOPER DASHBOARD ---
@router.get("/user-stats")
async def get_user_stats():
    try:
        # Queries the users collection we see in your MongoDB Compass
        total_users = await db.users.count_documents({})
        developer_count = await db.users.count_documents({"role": "developer"})
        standard_users = await db.users.count_documents({"role": "user"})

        return {
            "total": total_users,
            "developers": developer_count,
            "users": standard_users
        }
    except Exception as e:
        # Fallback to prevent frontend errors
        return {"total": 0, "developers": 0, "users": 0, "error": str(e)}