from telethon.sync import TelegramClient, events
import asyncio
import os
import random
import logging
from telethon.errors import SessionPasswordNeededError

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
# ✅ Message Handler
# ─────────────────────────────
@client.on(events.NewMessage(chats='mainet_community'))
async def handler(event):
    message = event.message
    text = message.message or ""

    # Skip messages without buttons
    try:
        buttons = await event.get_buttons()
        if not buttons:
            return
    except Exception as e:
        logger.warning(f"[x] Could not fetch buttons: {e}")
        return

    # Extract tweet URL if available
    tweet_url = None
    if "https://" in text:
        start = text.find("https://")
        end = text.find(" ", start)
        tweet_url = text[start:] if end == -1 else text[start:end]

    if tweet_url and tweet_url in seen_links:
        logger.info(f"[i] Already processed: {tweet_url}")
        return
    elif tweet_url:
        seen_links.add(tweet_url)

    await asyncio.sleep(random.randint(6, 12))
    try:
        if len(buttons) >= 5:
            await message.click(4)
            logger.info(f"[✓] Clicked 5th button: {tweet_url or 'No link'}")
        else:
            await message.click()
            logger.info(f"[✓] Clicked default button: {tweet_url or 'No link'}")
    except Exception as e:
        logger.error(f"[x] Failed to click button: {e}")

# ─────────────────────────────
# ✅ Main Entrypoint
# ─────────────────────────────
async def main():
    await client.connect()
    if not await client.is_user_authorized():
        logger.error("❌ Not authorized. Please re-login.")
        return

    logger.info("🤖 SmashBot is live and monitoring 'mainet_community' for raid buttons...")
    await client.run_until_disconnected()

# ─────────────────────────────
# ✅ Run the Bot
# ─────────────────────────────
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"🔥 Bot crashed: {e}")
