import asyncio
import os
import re
import random
import subprocess
import sys
from pathlib import Path

from telethon import TelegramClient, errors

# --- CORRECTED TELETHON IMORTS ---
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import GetUserPhotosRequest

# Attempt to import dotenv, install if missing
try:
    from dotenv import dotenv_values
except ImportError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'python-dotenv'])
    from dotenv import dotenv_values

# --- CONFIGURATION ---
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

Formats = [
    """━━━━━━━━━━━━━━━━━━━━━━━
⚡️ INTERVIEW SUPPORT ⚡️ 
━━━━━━━━━━━━━━━━━━━━━━━

Struggling with interviews? Online tests? Aptitude rounds?
We’ve got your back 💯

🔥 OUR SERVICES:
✔ Aptitude Round Support
✔ Technical Interview Support
✔ Online Test / Exam Support
✔ Real-Time Job Support

🚀 TECHNOLOGIES COVERED:
Java | Python | Node.js | React.js | Angular
.NET | Salesforce | DevOps
AWS | Azure | GCP
Data Science | ML | AI
Business Analyst (BA)
Manual & Automation Testing (Selenium, Cypress)
SAP | ServiceNow | SQL | Oracle
Power BI | Tableau & Many More

━━━━━━━━━━━━━━━━━━━━━━━

💎 WHY CHOOSE US?
👉 100% Invisible Screen Sharing
👉 Undetectable in Task Manager
👉 Instant On-Spot Answers
👉 100% Safe & Secure Support
👉 Trusted Globally 🌍 (🇺🇸 🇬🇧 🇮🇳 🇨🇦 🇦🇺)

━━━━━━━━━━━━━━━━━━━━━━━

No_DMs
📲Only_WhatsAp: 91 92441_45979""",

"""🎯 Struggling with Interviews? Let Experts Handle It!

🚀 Crack Any Tech Interview with Expert Proxy Support!
✅ Guaranteed satisfaction
✅ Master Any Skill — Java to DevOps
✅ Safe, Secure & Instant Assistance

No_DMs
📲Only_WhatsAp: 91 92441_45979


🛠️ Technologies We Cover:
💻 Java (Fullstack / Backend)
💻 Python | React | Node.js
💻 Salesforce | ServiceNow | Workday | SAP
💻 DevOps (AWS / Azure / GCP)
💻 QA (Manual / Automation)
💻 Data Engineer | BI | .NET | More…


🌟 Why Choose Us?
💡 Confidential Yet Powerfull software
⚡ real-time coaching and guidance
🛡️ 100% Safe & Secure — protect your system & data
🏆 Experts Across Every Tech Domain — Java to Salesforce
🚀 Guaranteed Success — confidence & performance boost
🌍 Global Support — USA 🇺🇸 | UK 🇬🇧 | India 🇮🇳 | Canada 🇨🇦 | Australia 🇦🇺

No_DMs
📲Only_WhatsAp: 91 92441_45979"""
]

ROOT_DIR = Path(__file__).parent
MIN_BREAK = 5 * 60   
MAX_BREAK = 5 * 60   
ROUND_DELAY = 5 * 60 

# --- HELPER FUNCTIONS ---

def load_bot_env(bot_dir):
    env_path = bot_dir / '.env'
    global_env_path = ROOT_DIR / '.env'
    
    values = dotenv_values(env_path) if env_path.exists() else {}
    phone = values.get('PHONE') or os.getenv('PHONE')
    
    global_values = dotenv_values(global_env_path) if global_env_path.exists() else {}
    api_id = global_values.get('API_ID') or os.getenv('API_ID')
    api_hash = global_values.get('API_HASH') or os.getenv('API_HASH')

    if not phone:
        phone = input(f"Enter phone number for {bot_dir.name}: ")
    if not api_id:
        api_id = input(f"Enter API ID (global): ")
    if not api_hash:
        api_hash = input(f"Enter API Hash (global): ")
        
    return phone, int(api_id), api_hash

def get_bot_dirs(root_dir):
    bot_dirs = [p for p in root_dir.iterdir() if p.is_dir() and p.name.lower().startswith('bot')]
    
    def sort_key(path):
        match = re.search(r'\d+', path.name)
        if match:
            return (0, int(match.group()))
        else:
            return (1, path.name.lower())

    return sorted(bot_dirs, key=sort_key)

async def fetch_group_links(client):
    links = []
    async for dialog in client.iter_dialogs():
        if getattr(dialog.entity, 'megagroup', False) and dialog.is_group and getattr(dialog.entity, 'username', None):
            links.append(f"https://t.me/{dialog.entity.username}")
    print(f"Fetched {len(links)} groups.")
    return links

# --- PROFILE ENFORCEMENT ---

async def ensure_profile_name(client):
    """Checks the bot account name and updates it to 'Interview Support' if it doesn't match."""
    try:
        me = await client.get_me()
        current_first_name = me.first_name or ""
        
        # Checking if it matches target name (ignoring trailing/leading spaces)
        if current_first_name.strip().lower() != "interview support":
            print(f"[PROFILE] Changing name from '{current_first_name}' to 'Interview Support'...")
            # We set first_name to 'Interview Support' and clear last_name to prevent double-naming issues
            await client(UpdateProfileRequest(first_name="Interview Support", last_name=""))
            print("[PROFILE] Name updated successfully.")
        else:
            print("[PROFILE] Account name is already 'Interview Support'.")
    except Exception as e:
        print(f"[WARNING] Could not update profile name: {e}")

# --- CORE SEND LOGIC ---

async def send_round(client, group_links):
    skip_numbers = ["92441_45979", "78148_37019", "8271737924", "9133817162", "9885074380", "7093493173"] 
    all_failed = True 

    for idx, group in enumerate(group_links, 1):
        if group == 'https://t.me/SavedMessages' or group.lower() == 'me':
            continue

        message_to_send = random.choice(Formats)

        try:
            last_msg = None
            async for msg in client.iter_messages(group, limit=1):
                last_msg = msg.text.strip() if msg.text else None
                break
            
            if last_msg:
                has_keyword = any(k in last_msg.lower() for k in KEYWORDS)
                if any(num in last_msg for num in skip_numbers) or last_msg == message_to_send or (len(last_msg) <= 250 and not has_keyword):
                    print(f"{idx}._S_K_I_P_P_E_D_ {group}")
                    continue

            await client.send_message(group, message_to_send)
            all_failed = False
            print(f"{idx}.____________ _/ {group}")
            await asyncio.sleep(random.randint(1, 5))
            
        except errors.FloodWaitError as e:
            print(f"{idx}._____________X_ (Flood) {group}. Waiting {e.seconds}s")
            await asyncio.sleep(e.seconds)
        except Exception:
            print(f"{idx}._____________X_ {group}")

    return all_failed

async def run_bot_round(bot_dir):
    phone, api_id, api_hash = load_bot_env(bot_dir)
    is_na = False
    session_path = str(bot_dir / 'session')
    client = TelegramClient(session_path, api_id, api_hash)

    try:
        await client.start(phone=phone)
    except (errors.PhoneNumberBannedError, errors.UserDeactivatedBanError):
        print(f"[CRITICAL] {phone} is Banned. Marking as NA.")
        return True 
    except Exception as e:
        print(f"______S_K_I_P_P_E_D_ {phone} Error: {e}")
        return False

    try:
        # Run the profile name enforcement before handling groups or sending messages
        await ensure_profile_name(client)
        
        group_links = list(dict.fromkeys(await fetch_group_links(client)))
        if not group_links:
            return False

        all_failed = await send_round(client, group_links)
        if all_failed:
            is_na = True
            
        return is_na
    finally:
        await client.disconnect()

# --- MAIN LOOP ---

async def main():
    while True:
        all_dirs = get_bot_dirs(ROOT_DIR)
        active_bots = [d for d in all_dirs if "_NA" not in d.name.upper()]
        
        if not active_bots:
            print("\n" + "!" * 50)
            print("all Bots are failed to send | Script Ended")
            print("!" * 50)
            break

        print(f"\n[INFO] Starting Round. Active Bots: {len(active_bots)}")

        for bot_dir in active_bots:
            print(f"\n[RUNNING] {bot_dir.name}")
            is_na = await run_bot_round(bot_dir)

            if is_na:
                new_path = bot_dir.parent / f"{bot_dir.name}_NA"
                try:
                    bot_dir.rename(new_path)
                    print(f"✅ Folder marked as dead: {new_path.name}")
                except Exception as e:
                    print(f"❌ Rename failed: {e}")
                
                print(f"[INFO] {bot_dir.name} is NA. Moving to next bot immediately...")
                continue 

            gap = random.randint(MIN_BREAK, MAX_BREAK)
            print(f"[INFO] Waiting {gap}s before next bot...")
            await asyncio.sleep(gap)

        print(f"\n[ROUND COMPLETE] All active bots finished. Sleeping {ROUND_DELAY//60} mins...")
        await asyncio.sleep(ROUND_DELAY)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n__[_S_T_O_P_P_E_D_]__ Script terminated by user.")