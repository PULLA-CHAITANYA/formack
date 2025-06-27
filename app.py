from telethon.sync import TelegramClient, events
import asyncio
import os
import random

# Railway-provided environment vars
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
SESSION_NAME = "918220747701"  # Your existing session name (.session file must be present)

seen_links = set()
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats='mainet_community'))  # Replace with your group
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

        await asyncio.sleep(random.randint(6, 12))  # Random delay
        try:
            if len(buttons) >= 5:
                await message.click(4)  # 5th button
                print(f"[✓] Smashed 5th button: {tweet_url or 'No link'}")
            else:
                await message.click()  # Default to first
                print(f"[✓] Smashed first button: {tweet_url or 'No link'}")
        except Exception as e:
            print(f"[x] Error smashing: {e}")
    else:
        print("[i] No buttons.")

async def main():
    await client.connect()
    if not await client.is_user_authorized():
        print("❌ Session not authorized. Please log in manually again.")
        return
    print("🤖 SmashBot is running and waiting for raids...")
    await client.run_until_disconnected()

asyncio.run(main())
