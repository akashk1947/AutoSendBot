import os
import asyncio
import random
import importlib.util
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError

# --- DYNAMIC IMPORT ---
common_functions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Batch1_147Links', 'account_4139', 'common', 'common_functions.py'))
spec = importlib.util.spec_from_file_location('common_functions', common_functions_path)
common_functions = importlib.util.module_from_spec(spec)
spec.loader.exec_module(common_functions)
contains_keyword = common_functions.contains_keyword

# --- CONFIGURATION ---
accounts = {
    # 'Batch1_147Links/account_7741': [f'bot{i}' for i in range(1, 2)],
    # 'Batch1_147Links/account_4139': [f'bot{i}' for i in range(1, 2)],
    # 'Batch2_207Links/account_1518': [f'bot{i}' for i in range(1, 2)],
    # 'Batch2_207Links/account_1977': [f'bot{i}' for i in range(1, 2)],
    # 'Batch2_207Links/account_4254': [f'bot{i}' for i in range(1, 2)],
    # 'Batch2_207Links/account_49952': [f'bot{i}' for i in range(1, 2)], #will run next
    'Batch2_207Links/account_64944': [f'bot{i}' for i in range(1, 2)],
}

GROUPS = [
    "https://t.me/ForceCertified",
    "https://t.me/SalesforceUSA",
    "https://t.me/Salesforcea",
    # Groups are added dynamically from clients, this is just a placeholder list. The actual groups will be fetched from the clients' dialogs.
]

FORMAT_1 = """
\/\/#atp ➕9️⃣1️⃣ 9️⃣1️⃣3️⃣3️⃣ 8️⃣1️⃣ 7️⃣1️⃣6️⃣2️⃣
──────────────────────
𝗢𝗡𝗘  𝗣 𝗔 𝗬  𝗨𝗡𝗟𝗜𝗠𝗜𝗧𝗘𝗗
⚡️ 𝗜 𝗡 𝗧 𝗘 𝗩 𝗜 𝗘 𝗪  𝗦 𝗨 𝗣 𝗣 𝗢  𝗧

𝗪𝗲 𝗖𝗼𝘃𝗲𝗿 𝗔𝗹𝗹 𝘁𝗲𝗰𝗵𝗻𝗼𝗹𝗼𝗴𝗶𝗲𝘀 𝗲𝘅𝗮𝗺𝗽𝗹𝗲:
Java | Python | Node.js | React.js | Angular .NET | Salesforce | DevOps | AWS | Azure GCP | Data Science | ML | AI | BA | Manual Testing Automation (Selenium, Cypress) ,SAP | ServiceNow SQL | Oracle | Power BI | Tableau and all technologies

𝗣  𝟬 𝘅 𝘆  𝘄𝗶𝘁𝗵 𝗮𝗱𝘃𝗮𝗻𝗰𝗲 𝘄𝗵𝗶𝗰𝗵  𝗴𝗼𝗻𝗻𝗮 𝗯𝗲 :
👉 𝟭𝟬𝟬  ℅ 𝗶 𝗻 𝘃 𝗶 𝘀 𝗶 𝗯 𝗹 𝗲 on screen share
👉 𝟭𝟬𝟬 ℅ 𝗶 𝗻 𝘃 𝗶 𝘀 𝗶 𝗯 𝗹 𝗲 in task Manager
👉 𝟭𝟬𝟬  % 𝗼𝗻 𝘀 𝗽 𝗼 𝘁 𝗮𝗻𝘀𝘄𝗲𝗿𝘀
👉 𝟭𝟬𝟬 ℅ 𝘀 𝗮 𝗳 𝗲 and secured

𝘀 𝘂 𝗽 𝗽 𝗼 𝘁 𝗲 𝗱 🇺🇸 🇬🇧 🇮🇳 🇨🇦 🇦🇺, All
──────────────────────
\/\/#atp ➕9️⃣1️⃣ 9️⃣1️⃣3️⃣3️⃣ 8️⃣1️⃣ 7️⃣1️⃣6️⃣2️⃣"""

FORMAT_2 = """🚩 𝗜 𝗡 𝗧 𝗘 𝗩 𝗜 𝗘 𝗪  𝗦 𝗨 𝗣 𝗣 𝗢  𝗧 ‼️

* Python (Full Stack, Front end, Backend)
* Java ( Fullstack, Front end, Backend,)
📍AWS , AZURE
📍React ,js
📍Data Engineer
📍Data Analyst 
📍SQL/Power BI/ selenium 
📍Data science
📍Tableau
📍Service Now, Salesforce
📍ETL Testing, QA manual, QA Automation
📍And All Tech Stach we cover


For INDIA,USA,UK,Canada,Australia
*(IST/CST/PST/EST time zones)*

\/\/#atp ➕9️⃣1️⃣ 9️⃣8️⃣8️⃣ 5️⃣0️⃣ 7️⃣4️⃣ 3️⃣8️⃣0️⃣"""

FORMAT_3 = """Hi everyone 👋 

I n t e v i e w  s u p p o t  a v a i l a b l e for all technologies 

For:
👉 Salesforce 
👉Java
👉Java full stack  
👉 C , C ++
👉Spring Boot Microservices 
👉spring Hibernate 
👉Dot Net
👉SAP
👉Data science 
👉Aws admin
👉Aws Devops
👉Azure admin
👉Azure Data Engineer 
👉Data Engineering 
👉Azure devops
👉Selenium
👉Manuel Testing
👉Automation testing 
👉Python
👉Python full stack 
👉SQL
👉Power Bi
👉Restapi
👉Django
👉Bigdata
👉React js & node js
👉Mango DB
👉Oracle 

O n l n e  t e s t   s u p p o t  &  E x a m s u p p o t also available 

\/\/#atp  ➕9️⃣1️⃣ 9️⃣1️⃣3️⃣3️⃣ 8️⃣1️⃣ 7️⃣1️⃣6️⃣2️⃣"""


# (FORMAT_1, FORMAT_2, etc. remain the same as your input)
FORMATS = [
    FORMAT_1,
    FORMAT_2,
    FORMAT_3
]

# --- HELPERS ---
def next_format(chat_id, last_format_index, FORMATS):
    i = last_format_index.get(chat_id, -1)
    i = (i + 1) % len(FORMATS)
    last_format_index[chat_id] = i
    return FORMATS[i]

def load_api_config(account):
    api_path = os.path.join(account, "api.py")
    if not os.path.exists(api_path):
        raise FileNotFoundError(f"api.py not found for {account}")
    spec = importlib.util.spec_from_file_location("api", api_path)
    api = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(api)
    return api

async def send_message_with_client(client, group, message, account_name, bot_name, formats_list, last_format_index, active_groups, chat_id=None):
    try:
        gid = chat_id if chat_id else group
        
        entity = await client.get_entity(group)
        last_msg = await client.get_messages(entity, limit=1)
        if last_msg and last_msg[0].out:
            print(f"X__Skipped__ {group}")
            return

        active_groups.add(gid)
        await asyncio.sleep(random.uniform(5, 15))  # 5-15 seconds between each group

        msg = next_format(gid, last_format_index, formats_list)
        await client.send_message(gid, msg)
        
        if not hasattr(send_message_with_client, 'sent_count'):
            send_message_with_client.sent_count = 0
        send_message_with_client.sent_count += 1
        
        now_str = datetime.now().strftime('%H:%M:%S')
        print(f"_/ __SENT___{account_name.split('/')[-1]}__ {group}")
    
    except FloodWaitError as e:
        total_seconds = e.seconds
        minutes = total_seconds // 60
        hours = minutes // 60
        seconds = total_seconds % 60
        minutes = minutes % 60
        if hours > 0:
            wait_str = f"{hours}:{minutes:02d}:{seconds:02d}"
        elif minutes > 0:
            wait_str = f"00:{minutes:02d}:{seconds:02d}"
        else:
            wait_str = f"00:00:{seconds:02d}"
        print(f"X__FloodWait__{account_name.split('/')[-1]}__ {group} ___{wait_str}")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        error_msg = 'Banned.' if 'banned' in str(e).lower() else str(e)
        print(f"X__[ERROR]__{account_name.split('/')[-1]}__ {group} ___{error_msg}")
    finally:
        active_groups.discard(gid)

# --- MAIN LOGIC ---

async def main():
    clients = []
    last_format_index = {}
    last_account_index = {}
    active_groups = set()
    all_our_user_ids = set()

    # 1. Initialize Clients
    print('[INFO] Starting clients...')
    for account, bots in accounts.items():
        try:
            api_mod = load_api_config(account)
            api_id = api_mod.apiId()
            api_hash = api_mod.apiHash()
            keywords = getattr(api_mod, 'KEYWORDS', [])

            for bot in bots:
                session_path = os.path.join(account, bot, api_mod.sessionName())
                client = TelegramClient(session_path, api_id, api_hash)
                await client.start()
                # Get our user id for this client
                try:
                    me = await client.get_me()
                    all_our_user_ids.add(me.id)
                except Exception as e:
                    print(f"[WARN] Could not get user id for {account}/{bot}: {e}")
                clients.append({
                    'client': client,
                    'account': account,
                    'bot': bot,
                    'keywords': keywords
                })
        except Exception as e:
            print(f"[CRITICAL] Failed to load {account}: {e}")

    # 2. Dynamic Group Fetching
    print('[INFO] Fetching joined groups...')
    joined_groups = set()
    for entry in clients:
        async for dialog in entry['client'].iter_dialogs():
            if dialog.is_group and getattr(dialog.entity, 'username', None):
                joined_groups.add(f"https://t.me/{dialog.entity.username}")
    
    if joined_groups:
        GROUPS.clear()
        GROUPS.extend(list(joined_groups))
        print(f'[INFO] Found {len(GROUPS)} groups.')


    # 3. Define the Strict 10-Minute Periodic Sending Loop
    async def run_strict_10min_send():
        while True:
            print("[INFO] Starting scheduled round...")
            for group_link in GROUPS:
                idx_acc = last_account_index.get(group_link, 0)
                idx_fmt = last_format_index.get(group_link, 0)

                selected = clients[idx_acc % len(clients)]

                try:
                    entity = await selected['client'].get_entity(group_link)
                    last_msg = await selected['client'].get_messages(entity, limit=1)
                    # Check if last message was sent by any of our accounts
                    if last_msg and last_msg[0].sender_id in all_our_user_ids:
                        print(f"[SKIP], (last msg is from any of our accounts) {group_link}")
                    else:
                        # Logic to send if last msg wasn't ours
                        await send_message_with_client(
                            selected['client'], group_link, "", 
                            selected['account'], selected['bot'], 
                            FORMATS, last_format_index, active_groups
                        )
                except Exception as e:
                    print(f"[ERROR] Periodic task failed for {group_link}: {e}")

                # Update indices
                last_account_index[group_link] = (idx_acc + 1) % len(clients)
                await asyncio.sleep(1) # Small delay between groups

            print("[INFO] Round completed. Waiting 10 minutes before next round...")
            await asyncio.sleep(600)  # Wait exactly 10 minutes

    # Only run the strict timer-based loop and keep clients alive
    await asyncio.gather(run_strict_10min_send(), *[c['client'].run_until_disconnected() for c in clients])

if __name__ == '__main__':
    asyncio.run(main())