import os
import time
from pyrogram import Client, filters

# ⚠️ Patch: Fix Telegram msg_id timing errors on Railway/Render
original_time = time.time
time.time = lambda: int(original_time())  # Override time to integer

# 🔐 Environment variables (set in Railway/Render dashboard)
API_ID = int(os.environ.get("API_ID", 28906453))
API_HASH = os.environ.get("API_HASH", "f494712f1d11956c1954e2cbbd984370")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4")

# 📦 Pyrogram Client
app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# 🟢 /start Command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("✅ Bot is running!")

# 🚀 Run the bot
if __name__ == "__main__":
    app.run()
