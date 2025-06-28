from telethon.sync import TelegramClient, events
import asyncio
import os
import random
import logging
from telethon.errors import SessionPasswordNeededError

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
SESSION_NAME = "918220747701"
TARGET_THREAD_ID = 67724  # Thread ID for RAIDSSS topic
TARGET_CHAT = 'mainet_community'

# ─────────────────────────────────────────────
# ✅ Session Validation
# ─────────────────────────────────────────────
if f"{SESSION_NAME}.session" not in os.listdir():
    logger.error("❌ Session file not found. Please upload it to the project root.")
    exit()

seen_links = set()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ─────────────────────────────────────────────
# ✅ Main SmashBot Handler
# ─────────────────────────────────────────────
@client.on(events.NewMessage(chats=TARGET_CHAT))
async def smash_handler(event):
    msg = event.message

    # Filter by thread_id
    if getattr(msg, "thread_id", None) != TARGET_THREAD_ID:
        return  # Ignore messages outside RAIDSSS topic

    logger.info(f"[✓] New message in RAIDSSS topic: {msg.message}")

    # Extract buttons
    try:
        buttons = await event.get_buttons()
    except Exception as e:
        buttons = None
        logger.warning(f"[x] Failed to get buttons: {e}")

    # Extract tweet URL
    tweet_url = None
    text = msg.message or ""
    if "https://" in text:
        start = text.find("https://")
        end = text.find(" ", start)
        tweet_url = text[start:] if end == -1 else text[start:end]

    if tweet_url and tweet_url in seen_links:
        logger.info(f"[i] Already smashed: {tweet_url}")
        return
    elif tweet_url:
        seen_links.add(tweet_url)

    # Click button
    if buttons:
        await asyncio.sleep(random.randint(6, 12))  # Anti-detection delay
        try:
            if len(buttons) >= 5:
                await msg.click(4)
                logger.info(f"[✓] Clicked 5th button for: {tweet_url or 'No link'}")
            else:
                await msg.click()
                logger.info(f"[✓] Clicked default button for: {tweet_url or 'No link'}")
        except Exception as e:
            logger.error(f"[x] Error clicking button: {e}")
    else:
        logger.info("[i] No buttons found in message.")

# ─────────────────────────────────────────────
# ✅ Async Start
# ─────────────────────────────────────────────
async def main():
    await client.connect()
    if not await client.is_user_authorized():
        logger.error("❌ Session not authorized. Please login again locally and re-upload the session.")
        return
    logger.info("🤖 SmashBot is now monitoring the RAIDSSS topic...")
    await client.run_until_disconnected()

# ─────────────────────────────────────────────
# ✅ Entrypoint
# ─────────────────────────────────────────────
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"🔥 Bot crashed: {e}")
