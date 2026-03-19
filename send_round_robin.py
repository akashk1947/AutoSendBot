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
    'Batch2_207Links/account_1518': [f'bot{i}' for i in range(1, 2)],
    # 'Batch2_207Links/account_8237': [f'bot{i}' for i in range(1, 2)],
    'Batch2_207Links/account_1977': [f'bot{i}' for i in range(1, 2)],
}

GROUPS = [
    "https://t.me/ForceCertified",
    "https://t.me/SalesforceUSA",
    "https://t.me/Salesforcea",
]

FORMAT_1 = """+91 91338_17162 whatsapp only

📢 Interview support
         Apttitude round support
             Online Test/Exam support 

We Cover All technologies example:
    Java | Python | Node.js | React.js | Angular .NET | Salesforce | DevOps | AWS | Azure GCP | Data Science | ML | AI | BA | Manual Testing Automation (Selenium, Cypress) ,SAP | ServiceNow SQL | Oracle | Power BI | Tableau n all

🎤 Proxy with advance software
Which gonna be invisible 
🔹 100℅ invisible on screen share
🔹 100℅ invisible in task Manager
🔹 100% on spot answers
🔹 100℅ safe and secured 

🌍 supported 🇺🇸 🇬🇧 🇮🇳 🇨🇦 🇦🇺 & All

+91 91338_17162 whatsapp only"""

FORMAT_2 = """🚩interview support-‼️

We are providing  interview support  for below technologies

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

and all IT certification and online Test Support.

For INDIA,USA,UK,Canada,Australia
*(IST/CST/PST/EST time zones)*
WhatsApp Only : +91 98850_74380"""

FORMAT_3 = """Hi everyone 👋 We providing 

Interview support available for all technologies 

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

Online test support & Exam support also available 

WhatsApp me for more details....
+91 91338_17162"""

FORMAT_4 = """_._._._._._._._._._._._
Interview Support 
°°°°°°°°°°°°°°°°°°°°

📍Data Science📍Data Analyst📍BA📍ETL📍Devops 📍Salesforce 📍Java📍Python 📍Power bi📍 React Angular📍QA📍Azure 📍Dot Net📍PL/SQL📍Networking 📍SAP📍Service Now📍AI/ML and many more

By using advance tool which is
🔹 100℅ invisible in task Manager
🔹 100℅ invisible on screen share
🔹 100℅ guaranteed support
🔹 100℅ on spot answers
🔹 100℅ safe and secured 

For INDIA,USA,UK,Canada,Australia
*(IST/CST/PST/EST time zones)

Whatsapp: +91 91338_17162"""


# (FORMAT_1, FORMAT_2, etc. remain the same as your input)
FORMATS = [
    FORMAT_1,
    FORMAT_2,
    FORMAT_3,
    FORMAT_4,
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

    # 3. Define the Periodic Sending Loop
    async def run_periodic_send():
        while True:
            print("[INFO] Starting scheduled round...")
            for group_link in GROUPS:
                idx_acc = last_account_index.get(group_link, 0)
                idx_fmt = last_format_index.get(group_link, 0)

                selected = clients[idx_acc % len(clients)]
                
                try:
                    entity = await selected['client'].get_entity(group_link)
                    last_msg = await selected['client'].get_messages(entity, limit=1)
                    if last_msg and last_msg[0].out:
                        print(f"[SKIP], (last msg is our msg) {group_link}")
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

            print("[INFO] Round completed. Sleeping for 1 hour...")
            await asyncio.sleep(3600)

    # 4. Set up Event Handlers
    for entry in clients:
        @entry['client'].on(events.NewMessage)
        async def handler(event, current_entry=entry):
            if event.out or not event.is_group or not event.raw_text:
                return
            
            chat = await event.get_chat()
            username = getattr(chat, "username", None)
            if not username:
                return
                
            group_link = f"https://t.me/{username}"
            text = event.raw_text.strip()
            
            if len(text) >= 250 or contains_keyword(text, current_entry['keywords']):
                idx_fmt = last_format_index.get(group_link, 0)
                await send_message_with_client(
                    current_entry['client'],
                    group_link,
                    FORMATS[idx_fmt % len(FORMATS)],
                    current_entry['account'],
                    current_entry['bot'],
                    FORMATS,
                    last_format_index,
                    active_groups
                )

    # Run both the periodic loop and the event listening
    await asyncio.gather(run_periodic_send(), *[c['client'].run_until_disconnected() for c in clients])

if __name__ == '__main__':
    asyncio.run(main())