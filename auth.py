from pymongo import MongoClient
from flask_login import UserMixin
import bcrypt
from config import MONGODB_URI

# MongoDB connection
try:
    if MONGODB_URI and MONGODB_URI != "your_mongodb_atlas_connection_string_here":
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Test connection
        client.server_info()
        db = client['legal_ai_db']
        users_collection = db['users']
        # Create unique index on email
        users_collection.create_index('email', unique=True)
        print("✓ MongoDB connected successfully!")
    else:
        print("⚠ MongoDB URI not configured. Please update MONGODB_URI in .env file")
        print("  Get your connection string from: https://cloud.mongodb.com/")
        users_collection = None
except Exception as e:
    print(f"⚠ MongoDB connection failed: {e}")
    print("  Please check your MONGODB_URI in .env file")
    users_collection = None


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.email = user_data['email']
        self.name = user_data['name']

    @staticmethod
    def get_by_id(user_id):
        if users_collection is None:
            return None
        from bson.objectid import ObjectId
        user_data = users_collection.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def get_by_email(email):
        if users_collection is None:
            return None
        user_data = users_collection.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def create_user(name, email, password):
        if users_collection is None:
            print("Error: MongoDB not connected")
            return None
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        user_data = {
            'name': name,
            'email': email,
            'password': hashed_password
        }
        
        try:
            result = users_collection.insert_one(user_data)
            user_data['_id'] = result.inserted_id
            print(f"✓ User created: {email}")
            return User(user_data)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def verify_password(email, password):
        if users_collection is None:
            return None
        user_data = users_collection.find_one({'email': email})
        if user_data:
            if bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
                return User(user_data)
        return None
