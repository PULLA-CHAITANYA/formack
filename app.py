from telethon.sync import TelegramClient, events
import asyncio
import os
import random
import logging
from telethon.errors import SessionPasswordNeededError, TypeNotFoundError

# ─────────────────────────────
# ✅ Logging Setup
# ─────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─────────────────────────────
# ✅ Config
# ─────────────────────────────
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_NAME = "918220747701"

if f"{SESSION_NAME}.session" not in os.listdir():
    logger.error("❌ Session file not found. Please upload it.")
    exit()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
seen_links = set()

# ─────────────────────────────
# ✅ Debug Logger (Global)
# ─────────────────────────────
@client.on(events.NewMessage)
async def debug_handler(event):
    try:
        chat = await event.get_chat()
        logger.warning(f"[DEBUG] New message from: {chat.title} ({event.chat_id})")
        logger.warning(f"[DEBUG] Text: {event.message.message}")
    except Exception as e:
        logger.warning(f"[DEBUG] Failed to fetch chat/message info: {e}")

# ─────────────────────────────
# ✅ Smash Handler (Raidar Bot)
# ─────────────────────────────
@client.on(events.NewMessage(chats='testingbothu'))  # replace with your real group
async def smash_handler(event):
    message = event.message
    text = message.message or ""

    try:
        buttons = await event.get_buttons()
    except Exception as e:
        buttons = None
        logger.warning(f"[x] Failed to get buttons: {e}")

    logger.info(f"[✓] Message received in 'testingbothu'")
    logger.info(f"    → Text: {text}")
    logger.info(f"    → Buttons: {buttons}")

    tweet_url = None
    if "https://" in text:
        start = text.find("https://")
        end = text.find(" ", start)
        tweet_url = text[start:] if end == -1 else text[start:end]

    if tweet_url and tweet_url in seen_links:
        logger.info(f"[i] Already smashed: {tweet_url}")
        return
    elif tweet_url:
        seen_links.add(tweet_url)

    if buttons:
        await asyncio.sleep(random.randint(6, 12))
        try:
            if len(buttons) >= 5:
                await message.click(4)
                logger.info(f"[✓] Clicked 5th button: {tweet_url or 'No link'}")
            else:
                await message.click()
                logger.info(f"[✓] Clicked default button: {tweet_url or 'No link'}")
        except Exception as e:
            logger.error(f"[x] Error clicking button: {e}")
    else:
        logger.info("[i] No clickable buttons found.")

# ─────────────────────────────
# ✅ Topic Scanner
# ─────────────────────────────
async def get_last_message_topic_id():
    try:
        chat = 'mainet_community'
        async for message in client.iter_messages(chat, limit=50):  # scan more
            topic_id = getattr(message, 'topic_id', None)
            logger.info(f"🧾 Message ID: {message.id} | Topic ID: {topic_id}")
            if topic_id:
                logger.info(f"🧵 Found topic message in '{chat}':")
                logger.info(f"    → Text: {message.text}")
                logger.info(f"    → Thread ID (topic_id): {topic_id}")
                return
        logger.warning("⚠️ No thread messages found in last 50 messages.")
    except Exception as e:
        logger.error(f"❌ Error fetching topic: {e}")

# ─────────────────────────────
# ✅ Main Async Entrypoint
# ─────────────────────────────
async def main():
    await client.connect()
    if not await client.is_user_authorized():
        logger.error("❌ Not authorized. Please re-login.")
        return

    logger.info("🤖 SmashBot is running...")
    await get_last_message_topic_id()
    await client.run_until_disconnected()

# ─────────────────────────────
# ✅ Entrypoint
# ─────────────────────────────
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"🔥 Bot crashed: {e}")
