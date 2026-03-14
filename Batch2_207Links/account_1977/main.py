import os

# Path setup
GROUPS_PATH = os.path.join(os.path.dirname(__file__), 'groups.txt')
API_PATH = os.path.join(os.path.dirname(__file__), 'api.py')

if not os.path.isfile(API_PATH):
    print(f"[ERROR] api.py not found at {API_PATH}")
    exit(1)
if not os.path.isfile(GROUPS_PATH):
    print(f"[ERROR] groups.txt not found at {GROUPS_PATH}")
    exit(1)

num_bots = 10

bot_code = '\nimport asyncio\nimport random\nimport sys\nimport os\nimport sqlite3\nimport shutil\naccount_dir = os.path.dirname(os.path.abspath(__file__))\nsys.path.append(os.path.dirname(account_dir))\nfrom telethon import TelegramClient, events\nfrom should_send_message import should_send_message\nfrom telethon.errors import FloodWaitError\nfrom common.common_functions import load_target_groups, next_format, contains_keyword, send_message_safe, file_exists\nparent = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))\ngroups_path = os.path.join(os.path.dirname(parent), "groups.txt")\ntry:\n    from api import apiId, apiHash, sessionName, KEYWORDS, formats\n    api_id = apiId()\n    api_hash = apiHash()\n    session_name = sessionName()\n    FORMATS = formats()\nexcept Exception as e:\n    print(f"[WARNING] Failed to import from api.py: {e}")\n    api_id = None\n    api_hash = None\n    session_name = None\n    KEYWORDS = None\n    FORMATS = []\nTARGET_GROUPS = load_target_groups(groups_path, bot_id="{BOT_ID}")\nlast_format_index = {}\nactive_groups = set()\nsession_base = session_name[:-8] if isinstance(session_name, str) and session_name.endswith(".session") else session_name\nsession_path = os.path.join(account_dir, session_base)\nclient = TelegramClient(session_path, api_id, api_hash)\n\nasync def start_client_with_lock_recovery():\n    global client\n    for _ in range(5):\n        try:\n            await client.start()\n            return\n        except sqlite3.OperationalError as e:\n            if "database is locked" not in str(e).lower():\n                raise\n            await asyncio.sleep(2)\n    fallback_session_path = f"{session_path}_fallback_{os.getpid()}"\n    src = f"{session_path}.session"\n    dst = f"{fallback_session_path}.session"\n    if os.path.isfile(src):\n        try:\n            shutil.copy2(src, dst)\n        except Exception:\n            pass\n    print("[WARNING] Session database is locked. Using fallback session file.")\n    client = TelegramClient(fallback_session_path, api_id, api_hash)\n    await client.start()\n\nasync def send_message_safe(chat_id, chat_title, group_link):\n    try:\n        last_msg = await client.get_messages(chat_id, limit=1)\n        if last_msg and last_msg[0].out:\n            print(f"⏭ Skipped (already last): {group_link}")\n            return\n        msg = next_format(chat_id, last_format_index, FORMATS)\n        await client.send_message(chat_id, msg)\n        print(f"[OK] Sent in: {group_link}")\n        await asyncio.sleep(random.randint(30, 45))\n    except FloodWaitError as e:\n        print(f"[WARNING] Skipped {group_link}: FloodWait {e.seconds}s - will retry on next trigger")\n    except Exception as e:\n        print(f"[ERROR] Error in {group_link}: {e}")\n    finally:\n        active_groups.discard(chat_id)\n\n@client.on(events.NewMessage)\nasync def handler(event):\n    if event.out:\n        return\n    if not event.is_group:\n        return\n    if not event.raw_text:\n        return\n    chat = await event.get_chat()\n    if not getattr(chat, "username", None):\n        return\n    group_link = f"https://t.me/{chat.username}"\n    if group_link not in TARGET_GROUPS:\n        return\n    text = event.raw_text.strip()\n    length = len(text)\n    has_keyword = contains_keyword(text, KEYWORDS)\n    if not should_send_message(text, length, has_keyword):\n        return\n    gid = event.chat_id\n    if gid in active_groups:\n        print(f"[INFO] Already queued: {group_link}")\n        return\n    last_msg = await client.get_messages(gid, limit=1)\n    if last_msg and last_msg[0].out:\n        print(f"[INFO] Skipped (our last msg): {chat.title}")\n        return\n    active_groups.add(gid)\n    asyncio.create_task(\n        send_message_safe(gid, chat.title, group_link)\n    )\n\nasync def main():\n    print("=== Starting Bot Setup ===")\n    if not TARGET_GROUPS or len(FORMATS) == 0:\n        print("[ERROR] Failed to load target groups or formats. Exiting.")\n        return\n    print(f"[OK] Setup complete. Starting bot...")\n    await start_client_with_lock_recovery()\n    me = await client.get_me()\n    print(f"[INFO] Bot Account: {me.first_name}, Running (Selected Groups Only)")\n    print("Loaded links:")\n    for idx, link in enumerate(TARGET_GROUPS, 1):\n        print(f"{idx}. {link}")\n    print("Started Sending_ _ _ ________________________________")\n    await client.run_until_disconnected()\n\nasyncio.run(main())\n'

for i in range(1, num_bots + 1):
    bot_dir = os.path.join(os.path.dirname(__file__), f'bot{i}')
    os.makedirs(bot_dir, exist_ok=True)
    start_path = os.path.join(bot_dir, 'start.py')
    code = bot_code.replace("{BOT_ID}", f'bot{i}')
    with open(start_path, 'w', encoding='utf-8') as sf:
        sf.write(code)
    print(f"[OK] Generated {bot_dir}/start.py")

print(f"\n[DONE] All {num_bots} bot files generated for this account.")
