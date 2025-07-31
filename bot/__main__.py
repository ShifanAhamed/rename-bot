import os
import asyncio
from pyrogram import Client, filters
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import ntplib

# Load environment variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# Sync time to avoid msg_id error
try:
    c = ntplib.NTPClient()
    response = c.request("pool.ntp.org")
    corrected_time = datetime.datetime.fromtimestamp(response.tx_time, datetime.UTC)
    print(f"⏱ Synced time: {corrected_time}")
except Exception as e:
    print(f"⚠️ Failed to sync time: {e}")

# MongoDB Setup
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["telegram_bot"]
    users_collection = db["users"]
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print(f"❌ MongoDB Error: {e}")

# Bot Client
app = Client(
    session_name="my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# /start command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"name": name, "joined": datetime.datetime.utcnow()}},
        upsert=True
    )

    await message.reply_text(f"👋 Hello {name}, you’ve been registered!")

# /users command
@app.on_message(filters.command("users"))
async def user_count(client, message):
    count = users_collection.count_documents({})
    await message.reply_text(f"📊 Total registered users: {count}")

print("🚀 Starting Telegram bot...")
app.run()

