import datetime
import ntplib
import os
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import Message

# ========== Environment Variables ==========
API_ID = int(os.getenv("27944263"))
API_HASH = os.getenv("f494712f1d11956c1954e2cbbd984370")
BOT_TOKEN = os.getenv("7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4")
MONGO_URI = os.getenv("mongodb://shifanahamed007:shifan007@cluster0.mongodb.net:27017/?authSource=admin")  # e.g., "mongodb+srv://user:pass@cluster0.mongodb.net/dbname"

# ========== Time Sync Function ==========
def sync_time():
    try:
        client = ntplib.NTPClient()
        response = client.request("pool.ntp.org")
        corrected_time = datetime.datetime.fromtimestamp(response.tx_time, datetime.UTC)
        print(f"⏱ Synced time: {corrected_time.isoformat()}")
    except Exception as e:
        print(f"⚠️ Time sync failed: {e}")

sync_time()

# ========== MongoDB Setup ==========
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_database()
    collection = db["messages"]
    print("✅ Connected to MongoDB Atlas")
except Exception as e:
    print(f"❌ MongoDB Error: {e}")

# ========== Telegram Bot ==========
app = Client(
    session_name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ========== /start Command ==========
@app.on_message(filters.command("start"))
async def start_handler(client, message: Message):
    await message.reply_text(
        f"👋 Hello **{message.from_user.first_name}**!\n\n"
        "Use `/save your_message` to save a message to MongoDB."
    )

# ========== /save Command ==========
@app.on_message(filters.command("save") & filters.text)
async def save_handler(client, message: Message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "N/A"
        first_name = message.from_user.first_name or "N/A"
        full_text = message.text

        command, *content = full_text.split(maxsplit=1)
        message_content = content[0] if content else ""

        if not message_content:
            await message.reply_text("⚠️ Please provide a message to save after `/save`.")
            return

        data = {
            "_id": message.message_id,
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "message": message_content,
            "saved_at": datetime.datetime.utcnow()
        }

        collection.insert_one(data)
        await message.reply_text(f"✅ Saved your message with ID: `{message.message_id}`")
    except Exception as e:
        await message.reply_text(f"❌ Error saving message: {e}")

# ========== Run Bot ==========
if __name__ == "__main__":
    print("🚀 Starting Telegram bot...")
    app.run()
