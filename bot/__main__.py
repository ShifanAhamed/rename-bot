import os
import time

# ⚠️ Patch to prevent Pyrogram "msg_id too low" error on Railway/Render
original_time = time.time
time.time = lambda: int(original_time())  # Force integer-based time

from pyrogram import Client, filters

# 🔐 Hardcoded Telegram API credentials (only use hardcoded values for local/dev use)
API_ID = 28906453
API_HASH = "f494712f1d11956c1954e2cbbd984370"
BOT_TOKEN = "7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4"

# 📦 Initialize Pyrogram Client
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🟢 /start Command
@app.on_message(filters.command("start"))
async def start_handler(client, message):
    await message.reply_text("✅ Bot is running successfully!")

# 🚀 Run the bot
if __name__ == "__main__":
    print("🚀 Starting Telegram bot...")
    app.run()
