
import asyncio
import random
import sys
import os
workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) )
sys.path.append(workspace_root)
from telethon import TelegramClient, events
from account6_4254.should_send_message import should_send_message
from telethon.errors import FloodWaitError

from account6_4254.common.common_functions import load_formats, load_target_groups, next_format, contains_keyword, send_message_safe, file_exists

parent = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", ".."))
workspace_root = os.path.dirname(parent)
formats_path = os.path.join(parent, "formats.py")
groups_path = os.path.join(parent, "groups.py")
api_path = os.path.join(parent, "api.py")

# Load API credentials
if file_exists(api_path):
    with open(api_path, "r", encoding="utf-8") as f:
        content = f.read()
    namespace = {}
    exec(content, namespace)
    api_id = namespace.get('api_id')
    api_hash = namespace.get('api_hash')
    session_name = namespace.get('session_name')
    KEYWORDS = namespace.get('KEYWORDS')
    SHARED_FORMATS_FILE = namespace.get('SHARED_FORMATS_FILE', 'formats/formats.py')
    if SHARED_FORMATS_FILE and not os.path.isabs(SHARED_FORMATS_FILE):
        formats_path = os.path.normpath(os.path.join(workspace_root, SHARED_FORMATS_FILE))
    elif SHARED_FORMATS_FILE:
        formats_path = SHARED_FORMATS_FILE
    print("✅ Loaded API credentials from api.py")
else:
    print(f"⚠️ api.py not found at {api_path}")
    api_id = None
    api_hash = None
    session_name = None
    KEYWORDS = None
    SHARED_FORMATS_FILE = 'formats/formats.py'

TARGET_GROUPS = load_target_groups(groups_path, fromItem=0, toItem=10)
FORMATS = load_formats(formats_path)
last_format_index = {}
active_groups = set()

 # ...existing code...

client = TelegramClient(session_name, api_id, api_hash)

async def send_message_safe(chat_id, chat_title, group_link):
    try:
        last_msg = await client.get_messages(chat_id, limit=1)
        if last_msg and last_msg[0].out:
            # If our last message is the most recent, wait 30-45s before sending again
            last_sent_time = last_msg[0].date.timestamp()
            now = time.time()
            wait_time = max(0, 30 - (now - last_sent_time))
            if wait_time > 0:
                print(f"Waiting {int(wait_time)}s before sending again in {group_link}")
                await asyncio.sleep(wait_time)
            print(f"⏭ Skipped (already last): {group_link}")
            return
        msg = next_format(chat_id)
        await client.send_message(chat_id, msg)
        print(f"✅ Sent in: {group_link}")
        # After sending, wait 30-45s before next possible send
        await asyncio.sleep(random.randint(30, 45))
    except FloodWaitError as e:
        print(f" Skipped {group_link}: FloodWait {e.seconds}s - will retry on next trigger")
    except Exception as e:
        print(f" Error in {group_link}: {e}")
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
    has_keyword = contains_keyword(text)
    if not should_send_message(text, length, has_keyword):
        return
    gid = event.chat_id
    if gid in active_groups:
        print(f"⏳ Already queued: {group_link}")
        return
    last_msg = await client.get_messages(gid, limit=1)
    if last_msg and last_msg[0].out:
        print(f"⏭ Skipped (our last msg): {chat.title}")
        return
    active_groups.add(gid)
    asyncio.create_task(
        send_message_safe(gid, chat.title, group_link)
    )

async def main():
    print("\n=== Starting Bot Setup ===")
    if not TARGET_GROUPS or len(FORMATS) == 0:
        print("❌ Failed to load target groups or formats. Exiting.")
        return
    print(f"\n✅ Setup complete. Starting bot...\n")
    await client.start()
    me = await client.get_me()
    print(f"🚀 Bot Account: {me.first_name}, Running (Selected Groups Only)")
    await client.run_until_disconnected()

asyncio.run(main())