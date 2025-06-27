from telethon.sync import TelegramClient, events
import asyncio
import os
import random

# ENV variables from Railway
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']

# Your existing session file (must be in root directory of repo)
SESSION_NAME = "918220747701"  # Make sure you have 918220747701.session in your project root

# Debug: Check if the session file exists in the deployed environment
print("📁 Files in directory:", os.listdir())
if f"{SESSION_NAME}.session" not in os.listdir():
    print("❌ Session file not found. Please upload it to the project root.")
    exit()

seen_links = set()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats='mainet_community'))  # Change to your group if needed
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

        await asyncio.sleep(random.randint(6, 12))  # Anti-detection delay
        try:
            if len(buttons) >= 5:
                await message.click(4)  # 5th button
                print(f"[✓] Smashed 5th button: {tweet_url or 'No link'}")
            else:
                await message.click()  # Default to first button
                print(f"[✓] Smashed default button: {tweet_url or 'No link'}")
        except Exception as e:
            print(f"[x] Error smashing: {e}")
    else:
        print("[i] Message received — no buttons found.")

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ Session not authorized. Please login manually again.")
        return
    print("🤖 SmashBot is running and waiting for raid messages...")
    await client.run_until_disconnected()

asyncio.run(main())
