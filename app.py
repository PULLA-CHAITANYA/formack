from telethon import TelegramClient, events, Button
import asyncio
import os
import random
import logging
import threading
from flask import Flask
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
# ✅ Environment / Config
# ─────────────────────────────
API_ID = int(os.getenv('API_ID', 25749247))
API_HASH = os.getenv('API_HASH', '5c8f9cdbed12339f4d1d9414a0151bc7')
SESSION_NAME = "918220747701"  # Corresponds to 918220747701.session

# Check session
if not os.path.exists(f"{SESSION_NAME}.session"):
    logger.error("❌ Session file not found. Please upload '918220747701.session'.")
    exit()

# Telegram Client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
seen_links = set()

# ─────────────────────────────
# ✅ Message Handler for Raids
# ─────────────────────────────
@client.on(events.NewMessage(chats='mainet_community'))
async def handler(event):
    message = event.message
    text = message.message or ""

    # Extract buttons
    try:
        buttons = await event.get_buttons()
        if not buttons:
            return
    except Exception as e:
        logger.warning(f"[!] Could not fetch buttons: {e}")
        return

    # Extract tweet link
    tweet_url = None
    if "https://" in text:
        start = text.find("https://")
        end = text.find(" ", start)
        tweet_url = text[start:] if end == -1 else text[start:end]

    if tweet_url:
        if tweet_url in seen_links:
            logger.info(f"[i] Already clicked: {tweet_url}")
            return
        seen_links.add(tweet_url)

    # Wait before clicking (simulate human)
    await asyncio.sleep(random.randint(6, 12))

    try:
        if len(buttons) >= 5:
            await message.click(4)
            logger.info(f"[✓] Clicked 5th button for: {tweet_url or 'No Link'}")
        else:
            await message.click()
            logger.info(f"[✓] Clicked default button for: {tweet_url or 'No Link'}")
    except Exception as e:
        logger.error(f"[x] Failed to click button: {e}")

# ─────────────────────────────
# ✅ Flask Keep-Alive Server (Railway Ping)
# ─────────────────────────────
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 SmashBot is alive!", 200

def start_flask():
    app.run(host='0.0.0.0', port=8000)

# ─────────────────────────────
# ✅ Main Entrypoint
# ─────────────────────────────
async def start_bot():
    await client.connect()
    if not await client.is_user_authorized():
        logger.error("❌ Client not authorized. Please check session.")
        return
    logger.info("🤖 SmashBot is live and scanning 'mainet_community' for raid buttons...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=start_flask).start()

    while True:
        try:
            asyncio.run(start_bot())
        except Exception as e:
            logger.critical(f"🔥 Bot crashed: {e}")
            logger.info("⏳ Restarting in 5 seconds...")
            asyncio.sleep(5)
