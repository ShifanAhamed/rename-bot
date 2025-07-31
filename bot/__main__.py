import os
import time
import ntplib
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client, filters

# ⏱ Time Sync Patch using NTP (Fixes Telegram msg_id errors)
try:
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')
    synced_time = int(response.tx_time)
    get_time = lambda: synced_time
    print("✅ Time synchronized with NTP")
except Exception as e:
    print(f"[⚠️] Time sync failed: {e}")
    get_time = lambda: int(time.time())  # fallback to local system time

# 🔐 Environment Variables (Railway/Render/Atlas Safe)
API_ID = int(os.environ.get("API_ID", "28906453"))
API_HASH = os.environ.get("API_HASH", "f494712f1d11956c1954e2cbbd984370")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4")

# ⚠️ FIXED: MongoDB URI with proper escape or raw string
MONGO_URI = os.environ.get(
    "MONGO_URI",
    r"mongodb+srv://shifanahamed007:s\\Shifan007@cluster0.xvznbpo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)

# 🌐 MongoDB Client (Motor)
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["Cluster0"]  # ✅ Corrected spelling
users_collection = db["users"]  # Use a simple collection name

# 🤖 Initialize Pyrogram Client
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🟢 /start command
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"

    # Store user in MongoDB if not already present
    if not await users_collection.find_one({"user_id": user_id}):
        await users_collection.insert_one({
            "user_id": user_id,
            "username": username,
            "joined_at": get_time()
        })
        print(f"👤 New user added: {username} ({user_id})")

    await message.reply_text("✅ Bot is running and connected to MongoDB!")

# 🚀 Run the bot
if __name__ == "__main__":
    print("🚀 Starting Telegram bot...")
    app.run()


