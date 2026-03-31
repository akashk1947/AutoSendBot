
import asyncio
from telethon import TelegramClient, errors
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'python-dotenv'])
    from dotenv import load_dotenv


env_path = Path(__file__).parent / '.env'
def prompt_and_save_env(phone, api_id, api_hash):
    with open(env_path, 'w') as f:
        f.write(f"PHONE={phone}\nAPI_ID={api_id}\nAPI_HASH={api_hash}\n")

def get_env_value(var, prompt_text):
    val = os.getenv(var)
    if not val:
        val = input(prompt_text)
    return val

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    phone = os.getenv('PHONE')
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    missing = False
    if not phone:
        phone = input('Enter your phone number (with country code): ')
        missing = True
    if not api_id:
        api_id = input('Enter your API ID: ')
        missing = True
    if not api_hash:
        api_hash = input('Enter your API Hash: ')
        missing = True
    if missing:
        prompt_and_save_env(phone, api_id, api_hash)
    api_id = int(api_id)
else:
    phone = input('Enter your phone number (with country code): ')
    api_id = input('Enter your API ID: ')
    api_hash = input('Enter your API Hash: ')
    prompt_and_save_env(phone, api_id, api_hash)
    api_id = int(api_id)
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
    skip_numbers = ["9133817162", "9885074380", "7093493173"]
    while True:
        results = []
        for idx, group in enumerate(group_links, 1):
            # Skip sending to Saved Messages itself
            if group == 'https://t.me/SavedMessages' or group.lower() == 'me':
                continue
            last_format = (last_format + 1) % len(formats)
            message_to_send = formats[last_format]
            # Fetch last message in the group
            last_msg = None
            try:
                async for msg in client.iter_messages(group, limit=1):
                    last_msg = msg.text.strip() if msg.text else None
                    break
            except Exception as e:
                print(f"{idx}. {group}: ERROR fetching last message: {e}")
                continue
            # Skip if last message contains any of the skip_numbers
            if last_msg and any(num in last_msg for num in skip_numbers):
                print(f"{idx}. SKIPPED {group}:")
                continue
            if last_msg and last_msg == message_to_send:
                print(f"{idx}. SKIPPED {group}:")
                continue
            try:
                await client.send_message(group, message_to_send)
                status = "_/"
            except errors.FloodWaitError as e:
                status = "X"
                await asyncio.sleep(e.seconds)
            except Exception as e:
                status = "X"
            results.append((group, status))
            print(f"{idx}. {status}       {group}")
            import random
            gap = random.randint(1, 5)
            # print(f"[INFO] Waiting {gap} seconds before next message...")
            await asyncio.sleep(gap)  # Random delay between 1 and 5 seconds
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
