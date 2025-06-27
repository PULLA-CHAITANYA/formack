from telethon.sync import TelegramClient, events
import asyncio
import os
import random

# -------------------------------
# Telegram Setup
# -------------------------------

API_ID = int(os.environ['API_ID'])         # Railway Secret
API_HASH = os.environ['API_HASH']          # Railway Secret
SESSION_PATH = os.path.join("sessions", "918220747701")  # Path to saved .session

seen_links = set()  # To avoid duplicate smash actions

client = TelegramClient(SESSION_PATH, API_ID, API_HASH)

@client.on(events.NewMessage(chats='mainet_community'))  # <-- Update if needed
async def handler(event):
    message = event.message
    text = message.message or ""
    buttons = message.buttons

    if buttons:
        # Try to extract tweet link from the message
        tweet_url = None
        if "https://" in text:
            start = text.find("https://")
            end = text.find(" ", start)
            tweet_url = text[start:] if end == -1 else text[start:end]

        # Avoid duplicate smash
        if tweet_url and tweet_url in seen_links:
            print(f"[i] Already smashed: {tweet_url}")
            return
        elif tweet_url:
            seen_links.add(tweet_url)

        # Anti-detection wait (randomized)
        await asyncio.sleep(random.randint(6, 12))

        try:
            if len(buttons) >= 5:
                await message.click(4)  # 0-based index → 5th button
                print(f"[✓] SMASHED 5th button: {tweet_url or 'no link'}")
            else:
                await message.click()
                print(f"[✓] SMASHED fallback button: {tweet_url or 'no link'}")
        except Exception as e:
            print(f"[x] Error smashing: {e}")
    else:
        print("[i] New message received – no buttons found.")

# -------------------------------
# Start the SmashBot
# -------------------------------

client.start()
print("🤖 SmashBot is live. Waiting for messages in #mainet_community...")
client.run_until_disconnected()
