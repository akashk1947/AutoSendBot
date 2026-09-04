import asyncio
import os
from pathlib import Path
from telethon import TelegramClient

# ========= DEPENDENCY CHECK =========
try:
    from dotenv import load_dotenv
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', 'python-dotenv'])
    from dotenv import load_dotenv

# ========= CREDENTIALS SETUP =========
env_path = Path(__file__).parent / '.env'

def prompt_and_save_env(phone, api_id, api_hash):
    with open(env_path, 'w') as f:
        f.write(f"PHONE={phone}\nAPI_ID={api_id}\nAPI_HASH={api_hash}\n")

# Load existing environment variables or prompt for new ones
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    phone = os.getenv('PHONE')
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    missing = False
    if not phone:
        phone = input('Enter your phone number (with country code): ')
        missing = True
    if not api_id:
        api_id = input('Enter your API ID: ')
        missing = True
    if not api_hash:
        api_hash = input('Enter your API Hash: ')
        missing = True
    if missing:
        prompt_and_save_env(phone, api_id, api_hash)
    api_id = int(api_id)
else:
    phone = input('Enter your phone number (with country code): ')
    api_id = input('Enter your API ID: ')
    api_hash = input('Enter your API Hash: ')
    prompt_and_save_env(phone, api_id, api_hash)
    api_id = int(api_id)

# Exactly matches your previous session name
session_name = "session"

# ========= MAIN LOGIN PROCESS =========
async def main():
    print(f"🔑 Initializing connection for {phone}...")
    
    # Initialize the client (this sets up 'session.session')
    client = TelegramClient(session_name, api_id, api_hash)
    
    # .start() will prompt you in the terminal for the SMS/Telegram code and 2FA password (if enabled)
    await client.start(phone)
    
    # Verify everything worked
    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"Logged in as: {me.first_name} {me.last_name or ''} (@{me.username or 'No Username'})")
    else:
        print("❌ Authorization failed.")
        
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())