from telethon.sync import TelegramClient, events
import asyncio
import os
import random
import logging
import threading
from flask import Flask

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
# ✅ Flask Setup (for uptime pings)
# ─────────────────────────────
app = Flask(__name__)

@app.route("/", methods=["GET", "HEAD"])
def home():
    logger.info("✅ UptimeRobot ping received on /")
    return "SmashBot is alive!", 200

@app.route("/<path:path>", methods=["GET", "HEAD"])
def catch_all(path):
    logger.info(f"⚠️ Ping received on unknown path: /{path}")
    return "Alive (unknown path)", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# ─────────────────────────────
# ✅ Message Handler
# ─────────────────────────────
@client.on(events.NewMessage(chats='testingbothu'))
async def handler(event):
    message = event.message
    text = message.message or ""

    try:
        buttons = await event.get_buttons()
        if not buttons:
            return

        # Flatten buttons from 2D list to 1D
        flat_buttons = [btn for row in buttons for btn in row]

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
        # ✅ Corrected positional argument (no keyword)
        await message.click(len(flat_buttons) - 1)
        logger.info(f"[✓] Clicked last button: {tweet_url or 'No link'}")
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

    logger.info("🤖 SmashBot is live and monitoring 'testingbothu' for raid buttons...")
    await client.run_until_disconnected()

# ─────────────────────────────
# ✅ Run Both Flask and Bot
# ─────────────────────────────
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"🔥 Bot crashed: {e}")
