import os
import time
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, filters

# ✅ System Time Only (No NTP)
get_time = lambda: int(time.time())
print("⏱ Using system time:", datetime.datetime.utcnow().isoformat(), "UTC")

# 🔐 Environment Variables
API_ID = int(os.environ.get("API_ID", "28906453"))
API_HASH = os.environ.get("API_HASH", "f494712f1d11956c1954e2cbbd984370")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://shifanahamed007:sShifan007@cluster0.xvznbpo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# 🌐 MongoDB Setup
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["Cluster0"]  # ✅ Correct DB name from URI
users_collection = db["users"]  # ✅ Use a clear collection name

# 🤖 Pyrogram Client
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🟢 /start command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"

    # Insert user if new
    if not await users_collection.find_one({"user_id": user_id}):
        await users_collection.insert_one({
            "user_id": user_id,
            "username": username,
            "joined_at": get_time()
        })
        print(f"👤 New user added: {username} ({user_id})")

    await message.reply_text("✅ Bot is running and connected to MongoDB!")

# 🚀 Start Bot
if __name__ == "__main__":
    print("🚀 Starting Telegram bot...")
    app.run()



