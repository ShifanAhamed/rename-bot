import os
import time
from pyrogram import Client, filters

# ⚠️ Patch: Fix Telegram msg_id timing errors
original_time = time.time
time.time = lambda: int(original_time())

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("✅ Bot is running!")

app.run()
