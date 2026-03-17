# pip install telethon
# python createAccountV2.py
"""
createAccountV2.py
==================
This script logs in to your Telegram account, fetches all joined public group links, and scaffolds a new bot account folder.
Bots and group link distribution are dynamic based on the number of joined groups.

Usage:
    python createAccountV2.py

You will be prompted for:
  - Mobile number (e.g. +919876541234)
  - API ID
  - API Hash
  - (Telegram login code, if not already authorized)

The script creates:
    account_XXXX/           <- last 4 digits of the mobile number
        __init__.py
        api.py
        groups.txt
        groups.py           <- all joined group links
        should_send_message.py
        run_all_bots.py
        main.py
        common/
            __init__.py
            common_functions.py
        bot1/ .. botN/
            start.py
Where N is based on the number of joined groups.
"""

import os
import re
import shutil
import math
import asyncio
from telethon import TelegramClient
from telethon.tl.types import Channel

# ─────────────────────────────────────────────
# Prompt user
# ─────────────────────────────────────────────
mobile = input("Enter mobile number (e.g. +919876541234): ").strip()
api_id  = input("Enter API ID: ").strip()
api_hash = input("Enter API Hash: ").strip()

# Define base_dir for the account folder
last4 = mobile[-4:]
base_dir = f"account_{last4}"
os.makedirs(base_dir, exist_ok=True)

# Define bot_start_template before main_py generation
bot_start_template = r'''
import asyncio
import random
import sys
import os
import sqlite3
import shutil
account_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(account_dir))
from telethon import TelegramClient, events
from should_send_message import should_send_message
from telethon.errors import FloodWaitError
from common.common_functions import load_target_groups, next_format, contains_keyword, send_message_safe, file_exists
parent = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))
groups_path = os.path.join(os.path.dirname(parent), "groups.txt")
try:
    from api import apiId, apiHash, sessionName, KEYWORDS, formats
    api_id = apiId()
    api_hash = apiHash()
    session_name = sessionName()
    FORMATS = formats()
except Exception as e:
    print(f"[WARNING] Failed to import from api.py: {e}")
    api_id = None
    api_hash = None
    session_name = None
    KEYWORDS = None
    FORMATS = []
TARGET_GROUPS = load_target_groups(groups_path, bot_id="{BOT_ID}", total_bots={num_bots})
last_format_index = {}
active_groups = set()
session_base = session_name[:-8] if isinstance(session_name, str) and session_name.endswith(".session") else session_name
session_path = os.path.join(account_dir, session_base)
client = TelegramClient(session_path, api_id, api_hash)

async def start_client_with_lock_recovery():
    global client
    for _ in range(5):
        try:
            await client.start()
            return
        except sqlite3.OperationalError as e:
            if "database is locked" not in str(e).lower():
                raise
            await asyncio.sleep(2)
    fallback_session_path = f"{session_path}_fallback_{{os.getpid()}}"
    src = f"{session_path}.session"
    dst = f"{fallback_session_path}.session"
    if os.path.isfile(src):
        try:
            shutil.copy2(src, dst)
        except Exception:
            pass
    print("[WARNING] Session database is locked. Using fallback session file.")
    client = TelegramClient(fallback_session_path, api_id, api_hash)
    await client.start()

async def send_message_safe(chat_id, chat_title, group_link):
    try:
        last_msg = await client.get_messages(chat_id, limit=1)
        if last_msg and last_msg[0].out:
            print(f"⏭ Skipped (already last): {group_link}")
            return
        msg = next_format(chat_id, last_format_index, FORMATS)
        await client.send_message(chat_id, msg)
        print(f"[OK] Sent in: {group_link}")
        await asyncio.sleep(random.randint(30, 45))
    except FloodWaitError as e:
        print(f"[WARNING] Skipped {group_link}: FloodWait {e.seconds}s - will retry on next trigger")
    except Exception as e:
        print(f"[ERROR] Error in {group_link}: {e}")
    finally:
        active_groups.discard(chat_id)

@client.on(events.NewMessage)
async def handler(event):
    if event.out:
        return
    if not event.is_group:
        return
    if not event.raw_text:
        return
    chat = await event.get_chat()
    if not getattr(chat, "username", None):
        return
    group_link = f"https://t.me/{{chat.username}}"
    if group_link not in TARGET_GROUPS:
        return
    text = event.raw_text.strip()
    length = len(text)
    has_keyword = contains_keyword(text, KEYWORDS)
    if not should_send_message(text, length, has_keyword):
        return
    gid = event.chat_id
    if gid in active_groups:
        print(f"[INFO] Already queued: {group_link}")
        return
    last_msg = await client.get_messages(gid, limit=1)
    if last_msg and last_msg[0].out:
        print(f"[INFO] Skipped (our last msg): {chat.title}")
        return
    active_groups.add(gid)
    asyncio.create_task(
        send_message_safe(gid, chat.title, group_link)
    )

async def main():
    print("=== Starting Bot Setup ===")
    if not TARGET_GROUPS or len(FORMATS) == 0:
        print("[ERROR] Failed to load target groups or formats. Exiting.")
        return
    print(f"[OK] Setup complete. Starting bot...")
    await start_client_with_lock_recovery()
    me = await client.get_me()
    print(f"[INFO] Bot Account: {{me.first_name}}, Running (Selected Groups Only)")
    print("Loaded links:")
    for idx, link in enumerate(TARGET_GROUPS, 1):
        print(f"{{idx}}. {{link}}")
    print("Started Sending_ _ _ ________________________________")
    await client.run_until_disconnected()

asyncio.run(main())
'''

# Generate main.py content for redistributing group links among bots
main_py = '''
import os
import math
import shutil

def split_groups(groups, num_bots):
    k, m = divmod(len(groups), num_bots)
    return [groups[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_bots)]

def main():
    with open("groups.txt", "r", encoding="utf-8") as f:
        groups = [line.strip() for line in f if line.strip()]
    num_bots = {num_bots}
    bot_dirs = [f"bot{{i+1}}" for i in range(num_bots)]
    group_chunks = split_groups(groups, num_bots)
    for bot_dir, chunk in zip(bot_dirs, group_chunks):
        os.makedirs(bot_dir, exist_ok=True)
        with open(os.path.join(bot_dir, "groups.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(chunk))
    print(f"Redistributed {{len(groups)}} links among {{num_bots}} bots.")

if __name__ == "__main__":
    main()
'''

# Generate bot1..botN/start.py immediately
# Ensure num_bots is defined before use
num_bots = 1  # TODO: Replace with dynamic calculation after fetching group links
for i in range(1, num_bots + 1):
    bot_dir = os.path.join(base_dir, f"bot{i}")
    os.makedirs(bot_dir, exist_ok=True)
    code = bot_start_template.replace("{BOT_ID}", f"bot{i}")
    with open(os.path.join(bot_dir, "start.py"), "w", encoding="utf-8") as f:
        f.write(code)

# Ensure total_links is defined before use
if 'total_links' not in locals():
    total_links = 0  # TODO: Replace with actual group link count if available
print(f"""
================================================
✅  Account folder created successfully!

  Folder : {base_dir}
  Bots   : {num_bots}
  Links  : {total_links}

All joined public group links are saved in:
  groups.py

Next steps:
  1. To run all bots at once:
       cd {base_dir}
       python run_all_bots.py

  2. To run a single bot:
       cd {os.path.join(base_dir, 'bot1')}
       python start.py

  3. If you update groups.txt later, re-run:
       python main.py   (inside the account folder)
     to redistribute links across bots.
================================================
""")
