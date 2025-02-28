from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["referral_bot"]
users = db["users"]

def add_user(user_id, referrer=None):
    if not users.find_one({"user_id": user_id}):
        users.insert_one({"user_id": user_id, "referrer": referrer, "referrals": 0})

def add_referral(referrer_id):
    users.update_one({"user_id": referrer_id}, {"$inc": {"referrals": 1}})

def get_referrals(user_id):
    user = users.find_one({"user_id": user_id})
    return user["referrals"] if user else 0
