from telethon import TelegramClient
import sys
import os

# Adjust these paths as needed
account_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(account_dir)
from api import apiId, apiHash, sessionName

api_id = apiId()
api_hash = apiHash()
session_name = sessionName()

client = TelegramClient(session_name, api_id, api_hash)

async def main():
    await client.start()
    print("Session created and authorized!")

import asyncio
asyncio.run(main())