from telethon.sync import TelegramClient, events
import asyncio
import os
import random
import logging
from telethon.errors import SessionPasswordNeededError, TypeNotFoundError

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API credentials from Railway or .env
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_NAME = "918220747701"

# Confirm session file exists
if f"{SESSION_NAME}.session" not in os.listdir():
    logger.error("❌ Session file not found. Please upload it to the project root.")
    exit()

seen_links = set()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats='testingbothu'))  # Replace with your group/channel
async def smash_handler(event):
    message = event.message
    text = message.message or ""
    try:
        buttons = await event.get_buttons()  # More reliable
    except Exception as e:
        buttons = None
        logger.warning(f"[x] Failed to get buttons: {e}")

    logger.debug(f"[DEBUG] Message: {text}")
    logger.debug(f"[DEBUG] Buttons: {buttons}")

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
        await asyncio.sleep(random.randint(6, 12))  # Anti-detection
        try:
            if len(buttons) >= 5:
                await message.click(4)
                logger.info(f"[✓] Smashed 5th button: {tweet_url or 'No link'}")
            else:
                await message.click()
                logger.info(f"[✓] Smashed default button: {tweet_url or 'No link'}")
        except Exception as e:
            logger.error(f"[x] Error clicking: {e}")
    else:
        logger.info("[i] Message received — no clickable buttons found.")

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        logger.error("❌ Session not authorized. Please login again locally and re-upload the session.")
        return
    logger.info("🤖 SmashBot is running and waiting for raid messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"🔥 Bot crashed: {e}")
