import os
from pyrogram import Client, filters

API_ID = int(os.environ.get("28906453"))
API_HASH = os.environ.get("f494712f1d11956c1954e2cbbd984370")
BOT_TOKEN = os.environ.get("7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4")

app = Client("rename_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("✅ Bot is running!")

app.run()
