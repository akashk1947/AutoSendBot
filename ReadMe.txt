# Telegram Multi-Bot Automation

## Prerequisites

- Python 3.8+ installed
- All required Python packages (see below)
- API credentials in `api.py`
- Group links in `groups.txt`

## Setup

1. **Install dependencies**  
   Open a terminal in the project directory and run:
   ```
   pip install telethon
   ```

2. **Prepare configuration**  
   - Edit `api.py` with your Telegram API credentials.
   - Add your group links (one per line) in `groups.txt`.

3. **Generate bot scripts**  
   In the `account6_4254` directory, run:
   ```
   python main.py
   ```
   This will create `bot1` to `bot10` folders, each with its own `start.py`.

## Running the Bots

4. **Start a bot**  
   In a new terminal, navigate to a bot folder (e.g., `bot1`) and run:
   ```
   python start.py
   ```

   Repeat for other bots as needed (each in a separate terminal).

## Notes

- Each bot will print the list of group links it is monitoring.
- Session files are preserved; running `main.py` again will not delete them.
- To update group links or credentials, edit `groups.txt` or `api.py` and rerun `main.py`.

##########################################################################
Account of Bot creation
C:\Users\theak\telegram\Running!!!>python createBot.py

Enter your Telegram phone number (Format: +91XXXXXXXXXX)
: +919324418152
Enter your Telegram api_id (Find it at https://my.telegram.org/apps)
: 39071336
Enter your Telegram api_hash
: 8b443e141f560f4eb2f60083f7bd4703
Copied 'account6_4139_Ban' to 'account6_8152'.
Updated api.py in 'account6_8152'.

--- Next Steps ---
To run each bot, open a terminal and execute:
python account6_8152/bot1/start.py
python account6_8152/bot2/start.py
python account6_8152/bot3/start.py
python account6_8152/bot4/start.py
python account6_8152/bot5/start.py
python account6_8152/bot6/start.py
python account6_8152/bot7/start.py
python account6_8152/bot8/start.py
python account6_8152/bot9/start.py
python account6_8152/bot10/start.py

Run each bot one by one. Your new Telegram account is ready for autoSendBot.


###########################################################################
Step 1:
____ Add phoneNumber, api_Id and api_hash in api.py file 

Step 2:
____ python main.py // To generate 10 bots having links/10bots

Step 3:
____ cd bot1
____cmd\bot1> python start.py