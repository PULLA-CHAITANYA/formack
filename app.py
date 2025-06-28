from telethon.sync import TelegramClient, events
import asyncio
import os
import random
import logging
from telethon.errors import SessionPasswordNeededError, TypeNotFoundError

# ─────────────────────────────────────────────
# ✅ Logging Setup
# ─────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# ✅ Environment Configs
# ─────────────────────────────────────────────
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_NAME = "918220747701"  # Replace with your number/session name

if f"{SESSION_NAME}.session" not in os.listdir():
    logger.error("❌ Session file not found. Please upload it to the project root.")
    exit()

seen_links = set()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ─────────────────────────────────────────────
# ✅ Debug Handler for All Messages
# ─────────────────────────────────────────────
@client.on(events.NewMessage)
async def debug_handler(event):
    try:
        chat = await event.get_chat()
        logger.warning(f"[DEBUG] New message from: {chat.title} ({event.chat_id})")
        logger.warning(f"[DEBUG] Text: {event.message.message}")
    except Exception as e:
        logger.warning(f"[DEBUG] Failed to fetch chat/message info: {e}")

# ─────────────────────────────────────────────
# ✅ Raidar SmashBot Handler
# ─────────────────────────────────────────────
@client.on(events.NewMessage(chats='testingbothu'))  # Replace with actual group name
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
        await asyncio.sleep(random.randint(6, 12))  # Anti-detection delay
        try:
            if len(buttons) >= 5:
                await message.click(4)
                logger.info(f"[✓] Smashed 5th button: {tweet_url or 'No link'}")
            else:
                await message.click()
                logger.info(f"[✓] Smashed default button: {tweet_url or 'No link'}")
        except Exception as e:
            logger.error(f"[x] Error clicking button: {e}")
    else:
        logger.info("[i] Message received — no clickable buttons found.")

# ─────────────────────────────────────────────
# ✅ Thread Checker Function
# ─────────────────────────────────────────────
async def get_last_message_topic_id():
    try:
        chat = 'mainet_community'  # Change this to any group/channel name or ID
        async for message in client.iter_messages(chat, limit=1):
            topic_id = getattr(message, 'topic_id', None)
            logger.info(f"🧵 Latest message in '{chat}': {message.text}")
            logger.info(f"🧵 Thread ID (topic_id): {topic_id}")
            logger.info(f"📨 Message ID: {message.id}")
            return
    except Exception as e:
        logger.error(f"Error fetching thread ID: {e}")

# ─────────────────────────────────────────────
# ✅ Main Async Start
# ─────────────────────────────────────────────
async def main():
    await client.connect()
    if not await client.is_user_authorized():
        logger.error("❌ Session not authorized. Please login again locally and re-upload the session.")
        return

    logger.info("🤖 SmashBot is running and waiting for raid messages...")
    await get_last_message_topic_id()
    await client.run_until_disconnected()

# ─────────────────────────────────────────────
# ✅ Entrypoint
# ─────────────────────────────────────────────
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"🔥 Bot crashed: {e}")
