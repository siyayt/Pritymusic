from typing import Dict
from PritiMusic.core.mongo import mongodb

# MongoDB mein autoplay ka collection
autoplaydb = mongodb.autoplay

# Cache dictionary: Isse bot har baar database check nahi karega, balki memory se fast read karega
autoplay_cache: Dict[int, bool] = {}


async def is_autoplay_group(chat_id: int) -> bool:
    """
    Check karta hai ki group mein autoplay enable hai ya nahi.
    Pehle cache mein check karega, agar nahi mila toh database mein.
    """
    if chat_id in autoplay_cache:
        return autoplay_cache[chat_id]
    
    chat = await autoplaydb.find_one({"chat_id": chat_id})
    if not chat:
        autoplay_cache[chat_id] = False
        return False
        
    autoplay_cache[chat_id] = True
    return True


async def add_autoplay_group(chat_id: int):
    """
    Group mein autoplay ON karta hai aur database me save karta hai.
    """
    is_on = await is_autoplay_group(chat_id)
    if not is_on:
        # Cache aur Database dono update karein
        autoplay_cache[chat_id] = True
        await autoplaydb.insert_one({"chat_id": chat_id})


async def remove_autoplay_group(chat_id: int):
    """
    Group se autoplay OFF karta hai aur database se delete karta hai.
    """
    is_on = await is_autoplay_group(chat_id)
    if is_on:
        # Cache aur Database dono se remove karein
        autoplay_cache[chat_id] = False
        await autoplaydb.delete_one({"chat_id": chat_id})
