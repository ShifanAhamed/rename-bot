import os
import time  # ✅ Add this
from pyrogram import Client, filters

# 🕒 Add a small delay to let system time sync
time.sleep(5)

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("✅ Bot is running!")

app.run()
