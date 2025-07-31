import time
import datetime
import os
from pyrogram import Client, filters
from pymongo import MongoClient
import asyncio

# ========== CONFIG ========== #
API_ID = 27944263
API_HASH = "f494712f1d11956c1954e2cbbd984370"
BOT_TOKEN = "7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4"
MONGO_URL = "mongodb+srv://shifanahamed007:shifan007@cluster0.mongodb.net/?retryWrites=true&w=majority"

# ========== TIME FIX FOR RENDER ========== #
class FixedTime:
    def time(self):
        return time.time() + 5  # try +10 or -5 if error persists

time = FixedTime()
print("⏱ Using system time:", datetime.datetime.utcnow().isoformat(), "UTC")

# ========== MONGO SETUP ========== #
try:
    mongo_client = MongoClient(MONGO_URL)
    db = mongo_client["telegram_bot"]
    users_collection = db["users"]
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print("❌ MongoDB Error:", e)

# ========== TELEGRAM BOT ========== #
app = Client(
    name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start command
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    users_collection.update_one(
        {"_id": user_id},
        {"$set": {"name": name}},
        upsert=True
    )
    await message.reply(f"👋 Hello {name}! You are now registered.")

# Run the bot
if __name__ == "__main__":
    print("🚀 Starting Telegram bot...")
    app.run()


