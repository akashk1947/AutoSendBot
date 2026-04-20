KEYWORDS = [
    "proxy support",
    "interview support",
    "interview",
    "interview help",
    "support available",
    "proxy",
    "assessment",
    "exam",
    "test",
    "8106368645",
]

import asyncio
import os
import re
from pathlib import Path

from telethon import TelegramClient, errors

try:
    from dotenv import dotenv_values
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'python-dotenv'])
    from dotenv import dotenv_values

ROOT_DIR = Path(__file__).parent


def prompt_and_save_env(env_path, phone, api_id, api_hash):
    env_path.parent.mkdir(parents=True, exist_ok=True)
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(f"PHONE={phone}\nAPI_ID={api_id}\nAPI_HASH={api_hash}\n")


def load_bot_env(bot_dir):
    env_path = bot_dir / '.env'
    global_env_path = ROOT_DIR / '.env'
    # Load phone from bot's .env
    values = dotenv_values(env_path) if env_path.exists() else {}
    phone = values.get('PHONE') or os.getenv('PHONE')
    # Load API_ID and API_HASH from global .env
    global_values = dotenv_values(global_env_path) if global_env_path.exists() else {}
    api_id = global_values.get('API_ID') or os.getenv('API_ID')
    api_hash = global_values.get('API_HASH') or os.getenv('API_HASH')

    missing = False
    if not phone:
        phone = input(f"Enter phone number for {bot_dir.name} (with country code): ")
        missing = True
    if not api_id:
        api_id = input(f"Enter API ID (global): ")
        missing = True
    if not api_hash:
        api_hash = input(f"Enter API Hash (global): ")
        missing = True
    if missing and env_path:
        # Only save phone to bot's .env, API_ID and API_HASH to global .env
        if not phone:
            prompt_and_save_env(env_path, phone, '', '')
        if (not api_id or not api_hash) and global_env_path:
            with open(global_env_path, 'a', encoding='utf-8') as f:
                if api_id:
                    f.write(f"API_ID={api_id}\n")
                if api_hash:
                    f.write(f"API_HASH={api_hash}\n")

    return phone, int(api_id), api_hash


def get_bot_dirs(root_dir):
    bot_dirs = [p for p in root_dir.iterdir() if p.is_dir() and p.name.lower().startswith('bot')]

    def sort_key(path):
        match = re.search(r'\d+', path.name)
        return int(match.group()) if match else path.name.lower()

    return sorted(bot_dirs, key=sort_key)


def get_session_name(bot_dir):
    session_base = bot_dir / 'session'
    return str(session_base)


# --- FETCH FORMATS FROM SAVED MESSAGES ---
async def fetch_formats_from_saved_messages(client, num_formats=3):
    entity = await client.get_entity('me')
    messages = []
    async for msg in client.iter_messages(entity, limit=num_formats):
        if msg.text and msg.text.strip():
            messages.append(msg.text.strip())
    return list(reversed(messages))


# --- GROUP LINKS: Will be dynamically fetched each bot run ---
async def fetch_group_links(client):
    links = []
    async for dialog in client.iter_dialogs():
        if getattr(dialog.entity, 'megagroup', False) and dialog.is_group and getattr(dialog.entity, 'username', None):
            link = f"https://t.me/{dialog.entity.username}"
            links.append(link)
    print(f"Fetched {len(links)} groups.")
    return links


async def send_round(client, group_links, formats, last_format):
    skip_numbers = [
        "92441_45979",
        "78148_37019",
        "𝗗𝗠_𝗧𝗢_𝗞𝗡𝗢𝗪_𝗠𝗢𝗥𝗘",
        "8271737924",
        "82_717379_24",
        "9133817162",
        "9885074380",
        "7093493173",
        "919133817162",
        "919885074380",
        "917093493173",
        "9133_81_7162",
        "98850_74380",
        "7093_49_3173",
    ]

    all_failed = True
    for idx, group in enumerate(group_links, 1):
        if group == 'https://t.me/SavedMessages' or group.lower() == 'me':
            continue

        last_format = (last_format + 1) % len(formats)
        message_to_send = formats[last_format]

        last_msg = None
        try:
            async for msg in client.iter_messages(group, limit=1):
                last_msg = msg.text.strip() if msg.text else None
                break
        except Exception as e:
            print(f"{idx}. {group}: ERROR fetching last message: {e}")
            continue

        if last_msg:
            has_keyword = any(keyword in last_msg.lower() for keyword in KEYWORDS)
            msg_length = len(last_msg)
        else:
            has_keyword = False
            msg_length = 0

        if last_msg and any(num in last_msg for num in skip_numbers):
            print(f"{idx}. SKIPPED  {group}")
            continue
        if last_msg and last_msg == message_to_send:
            print(f"{idx}. SKIPPED  {group}")
            continue
        if msg_length <= 250 and not has_keyword:
            print(f"{idx}. SKIPPED  {group}")
            continue

        try:
            await client.send_message(group, message_to_send)
            status = "_/"
            all_failed = False
            print(f"{idx}. {status}       {group}")
            import random
            gap = random.randint(1, 5)
            await asyncio.sleep(gap)
        except errors.FloodWaitError as e:
            status = "X"
            print(f"{idx}. {status}       {group}")
            await asyncio.sleep(e.seconds)
        except Exception:
            status = "X"
            print(f"{idx}. {status}       {group}")

    return last_format, all_failed


async def run_bot_round(bot_dir, last_format):
    phone, api_id, api_hash = load_bot_env(bot_dir)
    session_name = get_session_name(bot_dir)

    client = TelegramClient(session_name, api_id, api_hash)
    try:
        await client.start(phone=phone)
    except errors.PhoneNumberBannedError:
        print(f"[SKIP] Account: {phone} is Banned. Skipping this bot.")
        return last_format
    except errors.PhoneNumberFloodError:
        print(f"[SKIP] Account: {phone} is Restricted (Flood). Skipping this bot.")
        return last_format
    except errors.PhoneNumberInvalidError:
        print(f"[SKIP] Account: {phone} is Invalid. Skipping this bot.")
        return last_format
    except errors.UserDeactivatedBanError:
        print(f"[SKIP] Account: {phone} is Deactivated/Banned. Skipping this bot.")
        return last_format
    except Exception as e:
        if 'banned' in str(e).lower() or 'restricted' in str(e).lower():
            print(f"[SKIP] {phone} is Banned/Restricted")
            return last_format
        else:
            print(f"[SKIP] Account: {phone} error: {e}. Skipping this bot.")
            return last_format

    try:
        group_links = await fetch_group_links(client)
        seen = set()
        unique_group_links = []
        for link in group_links:
            if link not in seen:
                unique_group_links.append(link)
                seen.add(link)

        if not unique_group_links:
            print(f"[WARN] No groups found for {bot_dir.name}. Skipping this bot.")
            return last_format

        formats = await fetch_formats_from_saved_messages(client, num_formats=3)
        if not formats:
            print(f"[WARN] No formats found in Saved Messages for {bot_dir.name}. Skipping this bot.")
            return last_format

        last_format, all_failed = await send_round(client, unique_group_links, formats, last_format)
        if all_failed:
            print(f"[SKIP] Account: {phone} is likely Banned/Restricted (all sends failed). Skipping this bot.")
        return last_format
    finally:
        await client.disconnect()



MIN_BREAK = 5*60   # 5 minutes in seconds
MAX_BREAK = 10*60  # 10 minutes in seconds


async def main():
    bot_dirs = get_bot_dirs(ROOT_DIR)
    if not bot_dirs:
        print("[ERROR] No bot directories found in proxySupport. Create bot1, bot2, etc.")
        return

    print(f"[INFO] Total bots found: {len(bot_dirs)}")
    
    import random
    last_format = -1
    
    while True:
        
        for bot_dir in bot_dirs:
            # Skip bots with _NA suffix
            parts = bot_dir.name.split('_', 1)
            if len(parts) == 2 and parts[1].upper() == 'NA':
                print(f"[SKIP] Bot {bot_dir.name} is marked as NA.")
                continue
                
            print(f"[INFO] Running bot: {bot_dir.name}")
            last_format = await run_bot_round(bot_dir, last_format)
            
            # Short gap between different bots (0-10 seconds)
            break_gap = random.randint(MIN_BREAK, MAX_BREAK)
            print(f"[COMPLETED] {bot_dir.name}.")
            print(f"[INFO] Waiting {break_gap}s before next bot.")
            await asyncio.sleep(break_gap)

        # --- NEW LOGIC START ---
        round_delay = 15 * 60  # 15 minutes in seconds
        print(f"\n[ROUND COMPLETE FOR ALL BOTS], Sleeping 15 mins")
        await asyncio.sleep(round_delay)
        # --- NEW LOGIC END ---

if __name__ == '__main__':
    asyncio.run(main())
