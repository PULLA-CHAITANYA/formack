from telethon.sync import TelegramClient, events
import asyncio
import os
import random
import logging
from flask import Flask
import threading

API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_NAME = "918220747701"

app = Flask(__name__)

# ─────────────────────────────
# ✅ Logging Setup
# ─────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
seen_links = set()

# ─────────────────────────────
# ✅ Flask Endpoint
# ─────────────────────────────
@app.route('/')
def home():
    return "✅ SmashBot is alive!"

# ─────────────────────────────
# ✅ Telegram Handler
# ─────────────────────────────
@client.on(events.NewMessage(chats='mainet_community'))
async def handler(event):
    message = event.message
    text = message.message or ""

    try:
        buttons = await event.get_buttons()
        if not buttons:
            return
    except Exception as e:
        logger.warning(f"[x] Could not fetch buttons: {e}")
        return

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
# ✅ Telegram Background Task
# ─────────────────────────────
def start_telegram():
    async def main():
        await client.connect()
        if not await client.is_user_authorized():
            logger.error("❌ Not authorized. Please re-login.")
            return

        logger.info("🤖 SmashBot is live and monitoring 'mainet_community' for raid buttons...")
        await client.run_until_disconnected()

    asyncio.run(main())

# ─────────────────────────────
# ✅ Run Flask + Telegram Together
# ─────────────────────────────
if __name__ == '__main__':
    threading.Thread(target=start_telegram).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
