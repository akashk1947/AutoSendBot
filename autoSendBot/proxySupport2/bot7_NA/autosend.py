import asyncio
import random
from telethon import TelegramClient, errors
import os
from pathlib import Path

# --- CONFIGURATION VARIABLES ---
# Time to wait between the end of one round and the start of the next (in seconds)
WAIT_TIME_FROM = 1800  # 30 minutes
WAIT_TIME_TO = 3600    # 60 minutes
ROUND_DURATION = 3600  # Total time to finish one round (1 hour)

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

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    phone = os.getenv('PHONE')
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    # ... (rest of your env loading logic remains same)
    api_id = int(api_id) if api_id else None

# --- FETCH FORMATS & LINKS (Functions remain the same) ---
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

KEYWORDS = ["proxy support", "interview support", "interview", "interview help", "support available", "proxy", "assessment", "exam", "test", "8106368645"]

# --- CORE LOGIC ---
async def send_messages(client, group_links, formats):
    last_format = -1
    round_num = 1
    skip_numbers = ["92441_45979", "𝗗𝗠_𝗧𝗢_𝗞𝗡𝗢𝗪_𝗠𝗢𝗥𝗘","8271737924","82_717379_24", "9133817162", "9885074380", "7093493173", "919133817162", "919885074380", "917093493173", "9133_81_7162", "98850_74380", "7093_49_3173"]
    
    while True:
        num_groups = len(group_links)
        # Calculate dynamic gap: 1 hour / number of groups
        gap = ROUND_DURATION / num_groups if num_groups > 0 else 5
        
        print(f"\n--- Starting Round {round_num} ---")
        print(f"[INFO] Target: {num_groups} groups. Gap between sends: {gap:.2f}s")

        for idx, group in enumerate(group_links, 1):
            if group == 'https://t.me/SavedMessages' or group.lower() == 'me':
                continue
                
            last_format = (last_format + 1) % len(formats)
            message_to_send = formats[last_format]
            
            try:
                # Logic to check last message (Keywords/Skip numbers)
                last_msg = None
                async for msg in client.iter_messages(group, limit=1):
                    last_msg = msg.text.strip() if msg.text else None
                    break
                
                skip_reason = None
                if last_msg:
                    has_keyword = any(k in last_msg.lower() for k in KEYWORDS)
                    if any(num in last_msg for num in skip_numbers): skip_reason = "Skip Number"
                    elif last_msg == message_to_send: skip_reason = "Duplicate"
                    elif len(last_msg) <= 250 and not has_keyword: skip_reason = "Short/No Keyword"

                if skip_reason:
                    print(f"{idx}.__S_K_I_P__ {group}")
                else:
                    await client.send_message(group, message_to_send)
                    print(f"{idx}.__________/ {group}")

            except errors.FloodWaitError as e:
                print(f"[!] FloodWait: Must sleep for {e.seconds}s")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(f"{idx}.__X_X_X_X__ {group}")

            # Always wait the calculated gap to keep the 1-hour rhythm
            await asyncio.sleep(gap)

        # Round finished: Wait for random time between 30 and 60 minutes
        wait_time = random.randint(WAIT_TIME_FROM, WAIT_TIME_TO)
        print(f"Next round starts in {wait_time // 60} minutes ({wait_time}s)...\n")
        
        round_num += 1
        await asyncio.sleep(wait_time)

async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start(phone=phone)
    
    groupLinks = await fetch_group_links(client)
    unique_links = list(dict.fromkeys(groupLinks)) # Faster deduplication
    
    if not unique_links:
        print("[WARN] No groups found.")
        return

    formats = await fetch_formats_from_saved_messages(client)
    if not formats:
        print("[WARN] No formats in Saved Messages.")
        return

    await send_messages(client, unique_links, formats)

if __name__ == '__main__':
    asyncio.run(main())