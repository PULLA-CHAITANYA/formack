from telethon.sync import TelegramClient, events
import asyncio
import os
import random

# ---- Environment Variables ----
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_NAME = "918220747701"  # The same session name used in the login UI

# ---- Avoid Duplicate Smashes ----
seen_links = set()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats='mainet_community'))  # Replace with your target channel if needed
async def smash_handler(event):
    message = event.message
    text = message.message or ""
    buttons = message.buttons

    if buttons:
        tweet_url = None
        if "https://" in text:
            start = text.find("https://")
            end = text.find(" ", start)
            tweet_url = text[start:] if end == -1 else text[start:end]

        if tweet_url and tweet_url in seen_links:
            print(f"[i] Already smashed: {tweet_url}")
            return
        elif tweet_url:
            seen_links.add(tweet_url)

        await asyncio.sleep(random.randint(6, 11))

        try:
            if len(buttons) >= 5:
                await message.click(4)
                print(f"[✓] Smashed button 5: {tweet_url or 'No link'}")
            else:
                await message.click()
                print(f"[✓] Smashed default button: {tweet_url or 'No link'}")
        except Exception as e:
            print(f"[x] Failed to smash: {e}")
    else:
        print("[i] No buttons found.")

# ---- Start the Bot ----
client.start()
print("🤖 SmashBot is running. Waiting for raids...")
client.run_until_disconnected()
