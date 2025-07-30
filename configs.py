# (c) @AbirHasan2005

import os
import logging

class Config(object):
    # Required
    API_ID = int(os.environ.get("API_ID", "28906453"))  # Replace default if needed
    API_HASH = os.environ.get("API_HASH", "f494712f1d11956c1954e2cbbd984370")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7746953136:AAER6ehls2fS2ny4zO3wWcvBEcxg_YB_UD4")

    # Owner & Pro Users
    OWNER_ID = int(os.environ.get("OWNER_ID", "1869440885"))  # Replace with your Telegram ID
    PRO_USERS = list(set(int(x) for x in os.environ.get("PRO_USERS", "1869440885").split()))
    if OWNER_ID not in PRO_USERS:
        PRO_USERS.append(OWNER_ID)

    # MongoDB
    MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://shifanahamed007:Shifan007@cluster0.xvznbpo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # Log Channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001234567890"))  # Replace with your log channel ID

    # Misc
    DOWNLOAD_DIR = os.environ.get("DOWNLOAD_DIR", "./downloads")
    BROADCAST_AS_COPY = os.environ.get("BROADCAST_AS_COPY", "False").lower() == "true"

    # Logging
    LOGGER = logging
