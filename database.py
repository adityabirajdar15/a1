from pymongo import MongoClient

# Connect to local MongoDB server
client = MongoClient("mongodb://localhost:27017")

# Select your database
db = client["appdev"]

# Collections
users_collection = db["users"]
workouts_collection = db["workouts"]
diet_collection = db["diet_logs"]