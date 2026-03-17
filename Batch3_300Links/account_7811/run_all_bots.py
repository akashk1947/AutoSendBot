import subprocess
import os

workspace_root = os.path.dirname(os.path.abspath(__file__))
bot_dirs = [f'bot{i}' for i in range(1, 31)]
processes = []

for bot_dir in bot_dirs:
    start_py = os.path.join(workspace_root, bot_dir, 'start.py')
    env = os.environ.copy()
    env['PYTHONPATH'] = workspace_root
    proc = subprocess.Popen(
        ['python', start_py],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=os.path.join(workspace_root, bot_dir),
        env=env
    )
    processes.append((bot_dir, proc))
    print(f"[START] {bot_dir} launched (PID {proc.pid})")

print("
All 30 bots launched. Waiting for completion...
")

for bot_dir, proc in processes:
    stdout, stderr = proc.communicate()
    print(f'
--- Output for {bot_dir} ---')
    print(stdout)
    if stderr:
        print(f'--- Errors for {bot_dir} ---')
        print(stderr)
