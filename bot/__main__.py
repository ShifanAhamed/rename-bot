import os
import time
import ntplib
from pyrogram import Client, filters


# 🔧 Fix Telegram msg_id timing errors on Railway/Render
def sync_time():
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('pool.ntp.org')
        offset = response.tx_time - time.time()
        print(f"[🕒] Time sync offset: {offset:.2f} seconds")
        time.time = lambda: int(response.tx_time)
    except Exception as e:
        print(f"[⚠️] Time sync failed: {e}")

sync_time()

# 🔐 Telegram API credentials
API_ID = int(os.environ.get("API_ID", "28906453"))
API_HASH = os.environ.get("API_HASH", "f494712f1d11956c1954e2cbbd984370")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4")


# 📦 Pyrogram Bot Client
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ✅ /start command — stores user in MongoDB
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    user = users_collection.find_one({"_id": user_id})
    if not user:
        users_collection.insert_one({
            "_id": user_id,
            "first_name": message.from_user.first_name,
            "username": message.from_user.username,
            "joined_at": time.strftime("%Y-%m-%d %H:%M:%S")
        })
        await message.reply_text("👋 Hello! You've been added to the database.")
    else:
        await message.reply_text("✅ You're already in the database.")

# 🚀 Start the bot
if __name__ == "__main__":
    print("🚀 Starting Telegram bot...")
    app.run()

