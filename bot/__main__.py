import os
import asyncio
import datetime
import ntplib
from pyrogram import Client, filters
from pymongo import MongoClient

# ========== CONFIG ========== #
API_ID = 27944263
API_HASH = "f494712f1d11956c1954e2cbbd984370"
BOT_TOKEN = "7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4"
MONGO_URI = "MONGO_URI = "mongodb://shifanahamed007:shifan007@ac-xxxx.mongodb.net:27017/?authSource=admin"

# ========== TIME SYNC FIX FOR RENDER ========== #
def sync_time_with_ntp():
    try:
        ntp = ntplib.NTPClient()
        response = ntp.request("pool.ntp.org")
        corrected_time = datetime.datetime.utcfromtimestamp(response.tx_time)
        print("⏱ Synced time:", corrected_time.isoformat(), "UTC")
    except Exception as e:
        print("❌ NTP Sync Failed:", e)

sync_time_with_ntp()

# ========== MONGO SETUP ========== #
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["telegram_bot"]
    users_collection = db["users"]
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print("❌ MongoDB Error:", e)

# ========== TELEGRAM BOT SETUP ========== #
app = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ========== HANDLERS ========== #
@app.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    users_collection.update_one(
        {"_id": user_id},
        {"$set": {"name": name}},
        upsert=True
    )
    await message.reply(f"👋 Hello {name}! You are now registered in MongoDB.")

@app.on_message(filters.text & ~filters.command(["start"]))
async def echo_handler(client, message):
    await message.reply("✅ Message received!")

# ========== RUN ========== #
if __name__ == "__main__":
    print("🚀 Starting Telegram bot...")
    app.run()

