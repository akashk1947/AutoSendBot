import os

workspace_root = os.path.dirname(os.path.abspath(__file__))
bot_dirs = [f'bot{i}' for i in range(1, 11)]

for bot_dir in bot_dirs:
    start_py = os.path.join(workspace_root, bot_dir, 'start.py')
    # Use 'start' to open a new Command Prompt window for each bot
    # /D sets the working directory, /K keeps the window open after execution
    cmd = f'start "{bot_dir}" cmd /K "cd /D {os.path.join(workspace_root, bot_dir)} && python start.py"'
    os.system(cmd)
    print(f"[START] {bot_dir} launched in new window.")

print("\nAll 10 bots launched in separate Command Prompt windows.\n")
