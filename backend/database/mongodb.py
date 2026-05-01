from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB Port 27017
client = AsyncIOMotorClient("mongodb://localhost:27017")

# This creates 'app_db' if it doesn't exist
db = client.app_db