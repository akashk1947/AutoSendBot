
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
TARGET_GROUPS = load_target_groups(groups_path, bot_id="bot7")
last_format_index = {}
active_groups = set()
session_base = session_name[:-8] if isinstance(session_name, str) and session_name.endswith(".session") else session_name
session_path = os.path.join(account_dir, session_base)
client = TelegramClient(session_path, api_id, api_hash)

async def start_client_with_lock_recovery():
    global client
    for _ in range(5):
        try:
            await try_login()
            return
        except sqlite3.OperationalError as e:
            if "database is locked" not in str(e).lower():
                raise
            await asyncio.sleep(2)
    fallback_session_path = f"{session_path}_fallback_{os.getpid()}"
    src = f"{session_path}.session"
    dst = f"{fallback_session_path}.session"
    if os.path.isfile(src):
        try:
            shutil.copy2(src, dst)
        except Exception:
            pass
    print("[WARNING] Session database is locked. Using fallback session file.")
    client = TelegramClient(fallback_session_path, api_id, api_hash)
    await try_login()

# --- Robust login with phone_code_hash recovery ---
async def try_login():
    from telethon.errors import SessionPasswordNeededError
    while True:
        try:
            await client.start()
            return
        except ValueError as ve:
            if 'phone_code_hash' in str(ve):
                print("[ERROR] Login failed: code expired or invalid. Restarting login flow.")
                phone = input("Please enter your phone (or bot token): ")
                sent = await client.send_code_request(phone)
                while True:
                    code = input("Please enter the code you received: ")
                    try:
                        await client.sign_in(phone, code, phone_code_hash=sent.phone_code_hash)
                        return
                    except ValueError as ve2:
                        if 'phone_code_hash' in str(ve2):
                            print("Invalid code. Please try again.")
                            sent = await client.send_code_request(phone)
                        else:
                            raise
                    except SessionPasswordNeededError:
                        pw = input("Two-step verification enabled. Please enter your password: ")
                        await client.sign_in(password=pw)
                        return
            else:
                raise
        except SessionPasswordNeededError:
            pw = input("Two-step verification enabled. Please enter your password: ")
            await client.sign_in(password=pw)
            return

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
    group_link = f"https://t.me/{chat.username}"
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
    print(f"[INFO] Bot Account: {me.first_name}, Running (Selected Groups Only)")
    print("Loaded links:")
    for idx, link in enumerate(TARGET_GROUPS, 1):
        print(f"{idx}. {link}")
    print("Started Sending_ _ _ ________________________________")
    await client.run_until_disconnected()

asyncio.run(main())
