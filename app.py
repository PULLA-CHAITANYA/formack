from telethon.sync import TelegramClient, events
import asyncio
import os
import random
import logging

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
SESSION_NAME = "918220747701"  # Replace with your phone number or custom session name

# ─────────────────────────────────────────────
# ✅ Session Validation
# ─────────────────────────────────────────────
if f"{SESSION_NAME}.session" not in os.listdir():
    logger.error("❌ Session file not found. Please upload it to the project root.")
    exit()

seen_links = set()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# ─────────────────────────────────────────────
# ✅ Smash Handler for Specific Channel Only
# ─────────────────────────────────────────────
@client.on(events.NewMessage(chats='testingbothu'))  # Replace with actual channel username or ID
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
# ✅ Async Entrypoint
# ─────────────────────────────────────────────
async def main():
    await client.connect()
    if not await client.is_user_authorized():
        logger.error("❌ Session not authorized. Please login again locally and re-upload the session.")
        return
    logger.info("🤖 SmashBot is running and waiting for raid messages...")
    await client.run_until_disconnected()

# ─────────────────────────────────────────────
# ✅ Start the Bot
# ─────────────────────────────────────────────
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"🔥 Bot crashed: {e}")
