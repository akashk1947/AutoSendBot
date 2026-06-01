import asyncio
import os
import re
import unicodedata
import random
from pathlib import Path
from telethon import TelegramClient, errors

try:
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'python-dotenv'])
    from dotenv import load_dotenv

# --- CONFIGURATION & ENV LOADING ---
env_path = Path(__file__).parent / '.env'

def prompt_and_save_env(phone, api_id, api_hash):
    with open(env_path, 'w') as f:
        f.write(f"PHONE={phone}\nAPI_ID={api_id}\nAPI_HASH={api_hash}\n")

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

session_name = 'session'

# --- UTILITY FUNCTIONS ---

def normalize_text(text):
    """
    1. Converts stylized 'fancy' fonts to standard text.
    2. Removes all non-alphanumeric characters (removes underscores, spaces, dashes).
    3. Converts to lowercase.
    """
    if not text:
        return ""
    # Normalize unicode (converts 𝗗𝗠 to DM)
    text = unicodedata.normalize('NFKC', text)
    # Remove everything except digits and letters
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()

async def fetch_formats_from_saved_messages(client, num_formats=3):
    entity = await client.get_entity('me')
    messages = []
    async for msg in client.iter_messages(entity, limit=num_formats):
        if msg.text and msg.text.strip():
            messages.append(msg.text.strip())
    return list(reversed(messages))

async def fetch_group_links(client):
    print("[INFO] Fetching joined groups...")
    links = []
    async for dialog in client.iter_dialogs():
        if getattr(dialog.entity, 'megagroup', False) and dialog.is_group and getattr(dialog.entity, 'username', None):
            link = f"https://t.me/{dialog.entity.username}"
            links.append(link)
    print(f"[INFO] Found {len(links)} groups.")
    return links

# --- CONSTANTS ---
KEYWORDS = [
    "proxy support", "interview support", "interview help", 
    "support available", "proxy", "assessment", "exam", "test"
]

# Clean versions of the phone numbers/text you want to block
# DO NOT put underscores or spaces here.
BLOCK_LIST = [
    "6309729431", 
    "9244145979", 
    "8271737924", 
    "9133817162", 
    "9885074380", 
    "7093493173",
    "dmtoknowmore"
]

async def send_messages(client, group_links, formats):
    last_format = -1
    round_num = 1
    
    while True:
        print(f"\n--- Starting Round {round_num} ---")
        for idx, group in enumerate(group_links, 1):
            if group == 'https://t.me/SavedMessages' or group.lower() == 'me':
                continue

            last_format = (last_format + 1) % len(formats)
            message_to_send = formats[last_format]
            
            last_msg_raw = None
            try:
                async for msg in client.iter_messages(group, limit=1):
                    last_msg_raw = msg.text if msg.text else ""
                    break
            except Exception as e:
                print(f"{idx}. {group}: ERROR fetching last message: {e}")
                continue

            if last_msg_raw:
                # NORMALIZE the message for comparison
                cleaned_last_msg = normalize_text(last_msg_raw)
                
                # Check for Block List (Phone numbers/Specific phrases)
                is_blocked = any(target in cleaned_last_msg for target in BLOCK_LIST)
                
                # Check for Keywords
                has_keyword = any(kw in last_msg_raw.lower() for kw in KEYWORDS)
                
                # Check if we are double-posting the exact same format
                is_duplicate = last_msg_raw.strip() == message_to_send.strip()

                if is_blocked:
                    print(f"{idx}. SKIPPED (Blocked Content Found) -> {group}")
                    continue
                
                if is_duplicate:
                    print(f"{idx}. SKIPPED (Duplicate Post) -> {group}")
                    continue

                if len(last_msg_raw) <= 250 and not has_keyword:
                    print(f"{idx}. SKIPPED (Short/No Keyword) -> {group}")
                    continue

            try:
                await client.send_message(group, message_to_send)
                print(f"{idx}. SENT _/ -> {group}")
            except errors.FloodWaitError as e:
                print(f"X FloodWait: Sleeping for {e.seconds}s")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"{idx}. ERROR sending: {e}")

            await asyncio.sleep(random.randint(2, 6))

        wait_time = random.randint(600, 900)
        print(f"\n[INFO] Round {round_num} complete. Waiting {wait_time // 60} minutes...")
        round_num += 1
        await asyncio.sleep(wait_time)

async def main():
    client = TelegramClient(session_name, api_id, api_hash)
    await client.start(phone=phone)
    
    group_links = await fetch_group_links(client)
    unique_links = list(dict.fromkeys(group_links)) # Deduplicate
    
    if not unique_links:
        print("[WARN] No groups found.")
        return

    formats = await fetch_formats_from_saved_messages(client, num_formats=3)
    if not formats:
        print("[WARN] No formats found in Saved Messages.")
        return

    await send_messages(client, unique_links, formats)

if __name__ == '__main__':
    asyncio.run(main())