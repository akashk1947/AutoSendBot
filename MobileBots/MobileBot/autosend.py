import asyncio
from telethon import TelegramClient, errors
import os

# --- USER INPUT ---
phone = input('Enter your phone number (with country code): ')
api_id = int(input('Enter your API ID: '))
api_hash = input('Enter your API Hash: ')
session_name = 'user_session'


# --- FETCH FORMATS FROM SAVED MESSAGES ---
async def fetch_formats_from_saved_messages(client, num_formats=3):
    # 'me' is the special entity for Saved Messages
    entity = await client.get_entity('me')
    messages = []
    async for msg in client.iter_messages(entity, limit=num_formats):
        if msg.text and msg.text.strip():
            messages.append(msg.text.strip())
    # Return in chronological order (oldest first)
    return list(reversed(messages))


# --- GROUP LINKS: Will be dynamically fetched each run ---
async def fetch_group_links(client):
    print("[INFO] Fetching joined groups...")
    links = []
    async for dialog in client.iter_dialogs():
        # Only pure groups (not channels, contacts, private, or megagroups-as-channels)
        if getattr(dialog.entity, 'megagroup', False) and dialog.is_group and getattr(dialog.entity, 'username', None):
            link = f"https://t.me/{dialog.entity.username}"
            links.append(link)
    print(f"[INFO] Found {len(links)} groups.")
    return links

async def fetch_and_print_groups(client):
    print("[INFO] Fetching joined groups...")
    links = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group and getattr(dialog.entity, 'username', None):
            link = f"https://t.me/{dialog.entity.username}"
            links.append(link)
            print(link)
    print(f"[INFO] Found {len(links)} groups. Copy these into groupLinks for future runs.")
    return links


async def send_messages(client, group_links, formats, interval=600):
    last_format = -1
    round_num = 1
    while True:
        results = []
        for idx, group in enumerate(group_links, 1):
            # Skip sending to Saved Messages itself
            if group == 'https://t.me/SavedMessages' or group.lower() == 'me':
                continue
            last_format = (last_format + 1) % len(formats)
            try:
                await client.send_message(group, formats[last_format])
                status = "_/"
            except errors.FloodWaitError as e:
                status = "X"
                await asyncio.sleep(e.seconds)
            except Exception as e:
                status = "X"
            results.append((group, status))
            print(f"{idx}. {group}: {status}")
            await asyncio.sleep(2)  # Short delay between groups
        import random
        wait_time = random.randint(300, 600)
        print(f"[INFO] Waiting {wait_time} seconds before next round...\n")
        round_num += 1
        await asyncio.sleep(wait_time)


async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start(phone=phone)
    groupLinks = await fetch_group_links(client)
    if not groupLinks:
        print("[WARN] No groups found. Join some groups and try again.")
        return
    # Fetch formats from Saved Messages, fallback to default if none found
    formats = await fetch_formats_from_saved_messages(client, num_formats=3)
    if not formats:
        print("[WARN] No formats found in Saved Messages. Please add some messages there.")
        return
    await send_messages(client, groupLinks, formats)

if __name__ == '__main__':
    asyncio.run(main())
