from telethon.sync import TelegramClient, events
import asyncio
import os
import random

# Load credentials from Railway Environment Variables
API_ID = int(os.environ['API_ID'])        # e.g., 25749247
API_HASH = os.environ['API_HASH']         # e.g., '5c8f9cdbed12339f4d1d9414a0151bc7'
SESSION_NAME = "918220747701"             # This should match your saved session file

# Track links to prevent duplicate smashes
seen_links = set()

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats='mainet_community'))  # Replace with actual group username
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

        await asyncio.sleep(random.randint(6, 12))  # Random delay for anti-detection
        try:
            if len(buttons) >= 5:
                await message.click(4)  # Click 5th button
                print(f"[✓] Smashed 5th button: {tweet_url or 'No link'}")
            else:
                await message.click()  # Default to first button
                print(f"[✓] Smashed first button: {tweet_url or 'No link'}")
        except Exception as e:
            print(f"[x] Smash failed: {e}")
    else:
        print("[i] Message received – no buttons.")

client.start()
print("🤖 SmashBot is running and waiting for raid messages...")
client.run_until_disconnected()
