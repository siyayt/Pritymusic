from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client

import config
from ..logging import LOGGER

TEMP_MONGODB = "mongodb+srv://SizzuMusicBot:Istkhar786@sizzumusicbot.5rymou1.mongodb.net/?appName=SizzuMusicBot"

MONGO_URI = config.MONGO_DB_URI or TEMP_MONGODB

try:
    _mongo_async_ = _mongo_client_(MONGO_URI)
    _mongo_sync_ = MongoClient(MONGO_URI)

    if config.MONGO_DB_URI:
        mongodb = _mongo_async_.Anon
        pymongodb = _mongo_sync_.Anon
    else:
        LOGGER(__name__).warning("MONGO_DB_URI not found, using TEMP_MONGODB")

        temp_client = Client(
            "Anon",
            bot_token=config.BOT_TOKEN,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
        )

        temp_client.start()
        info = temp_client.get_me()
        username = info.username
        temp_client.stop()

        mongodb = _mongo_async_[username]
        pymongodb = _mongo_sync_[username]

except Exception as e:
    LOGGER(__name__).error(f"MongoDB Connection Failed: {e}")
    raise e
