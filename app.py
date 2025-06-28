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
# ✅ Raid Handler (Only Button Messages)
# ─────────────────────────────
@client.on(events.NewMessage(chats='mainet_community'))
async def raid_filter(event):
    message = event.message
    text = message.message or ""

    try:
        buttons = await event.get_buttons()
    except Exception:
        buttons = None

    if not buttons:
        return  # ⛔ Ignore messages with no buttons

    logger.info(f"[🚀] Button message detected in 'mainet_community'")
    logger.info(f"     → Text: {text}")
    logger.info(f"     → Buttons: {buttons}")

    # Find tweet URL if present
    tweet_url = None
    if "https://" in text:
        start = text.find("https://")
        end = text.find(" ", start)
        tweet_url = text[start:] if end == -1 else text[start:end]

    if tweet_url and tweet_url in seen_links:
        logger.info(f"[SKIP] Already handled: {tweet_url}")
        return
    elif tweet_url:
        seen_links.add(tweet_url)

    await asyncio.sleep(random.randint(6, 12))  # Anti-bot delay

    try:
        if len(buttons) >= 5:
            await message.click(4)
            logger.info(f"[✓] Clicked 5th button: {tweet_url or 'No link'}")
        else:
            await message.click()
            logger.info(f"[✓] Clicked first button: {tweet_url or 'No link'}")
    except Exception as e:
        logger.error(f"[x] Error clicking button: {e}")

# ─────────────────────────────
# ✅ Topic Scanner (Optional Logging)
# ─────────────────────────────
async def get_last_message_topic_id():
    try:
        chat = 'mainet_community'
        async for message in client.iter_messages(chat, limit=50):
            topic_id = getattr(message, 'topic_id', None)
            logger.info(f"🧾 Message ID: {message.id} | Topic ID: {topic_id}")
            if topic_id:
                logger.info(f"🧵 Found topic in '{chat}': {message.text}")
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

    logger.info("🤖 SmashBot is live and monitoring 'mainet_community' for raid buttons...")
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
