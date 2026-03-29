import os
import asyncio
import random
import threading
import time
from telethon.errors import FloodWaitError


def file_exists(path):
    return os.path.isfile(path)

def load_formats(formats_path):
    FORMATS = []
    if os.path.isfile(formats_path):
        with open(formats_path, "r", encoding="utf-8") as f:
            content = f.read()
        namespace = {}
        exec(content, namespace)
        FORMATS = [namespace.get(f'FORMAT_{i}') for i in range(1, 5) if f'FORMAT_{i}' in namespace]
        return FORMATS
    else:
        print(f"\u26a0\ufe0f formats file not found at {formats_path}")
        return []

def load_target_groups(groups_path, bot_id=None, total_bots=10, fromItem=0, toItem=3):
    if not os.path.isfile(groups_path):
        print(f"[WARNING] groups.txt not found at {groups_path}")
        return []

    with open(groups_path, "r", encoding="utf-8") as gf:
        all_lines = [line.strip() for line in gf if line.strip() and not line.strip().startswith("#")]

    if bot_id is not None:
        try:
            if isinstance(bot_id, str):
                digits = "".join(ch for ch in bot_id if ch.isdigit())
                if not digits:
                    print(f"[WARNING] Invalid bot_id: {bot_id}")
                    return []
                bot_number = int(digits)
            else:
                bot_number = int(bot_id)
        except Exception:
            print(f"[WARNING] Invalid bot_id: {bot_id}")
            return []

        if bot_number < 1 or bot_number > total_bots:
            print(f"[WARNING] bot_id out of range 1..{total_bots}: {bot_id}")
            return []

        total_links = len(all_lines)
        base_size = total_links // total_bots
        remainder = total_links % total_bots
        start_index = (bot_number - 1) * base_size + min(bot_number - 1, remainder)
        end_index = start_index + base_size + (1 if bot_number <= remainder else 0)
        return all_lines[start_index:end_index]

    return all_lines[fromItem:toItem]

def next_format(chat_id, last_format_index, FORMATS):
    i = last_format_index.get(chat_id, -1)
    i = (i + 1) % len(FORMATS)
    last_format_index[chat_id] = i
    return FORMATS[i]

def contains_keyword(text, KEYWORDS):
    t = text.lower()
    return any(k.lower() in t for k in KEYWORDS)

async def send_message_safe(client, chat_id, chat_title, group_link, FORMATS, last_format_index, active_groups):
    try:
        await asyncio.sleep(random.randint(5, 15))
        last_msg = await client.get_messages(chat_id, limit=1)
        if last_msg and last_msg[0].out:
            print(f"\u23ed Skipped (already last): {group_link}")
            return
        msg = next_format(chat_id, last_format_index, FORMATS)
        await client.send_message(chat_id, msg)
        print(f"\u2705 Sent in: {group_link}")
    except FloodWaitError as e:
        print(f" Skipped {group_link}: FloodWait {e.seconds}s - will retry on next trigger")
    except Exception as e:
        print(f" Error in {group_link}: {e}")
    finally:
        active_groups.discard(chat_id)

def handler_factory(client, TARGET_GROUPS, KEYWORDS, should_send_message, FORMATS, last_format_index, active_groups):
    from telethon import events
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
            print(f"\u23f3 Already queued: {group_link}")
            return
        last_msg = await client.get_messages(gid, limit=1)
        if last_msg and last_msg[0].out:
            print(f"\u23ed Skipped (our last msg): {chat.title}")
            return
        active_groups.add(gid)
        asyncio.create_task(
            send_message_safe(client, gid, chat.title, group_link, FORMATS, last_format_index, active_groups)
        )
    return handler
