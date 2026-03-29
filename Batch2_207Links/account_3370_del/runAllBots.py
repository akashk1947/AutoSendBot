import subprocess
import os
import threading

workspace_root = os.path.dirname(os.path.abspath(__file__))
bot_dirs = [f'bot{i}' for i in range(1, 11)]
processes = []

def stream_output(bot_dir, proc):
    def print_stream(stream, prefix):
        for line in iter(stream.readline, ''):
            if line:
                print(f'[{bot_dir}][{prefix}] {line}', end='')
        stream.close()
    threads = []
    threads.append(threading.Thread(target=print_stream, args=(proc.stdout, 'OUT')))
    threads.append(threading.Thread(target=print_stream, args=(proc.stderr, 'ERR')))
    for t in threads:
        t.start()
    for t in threads:
        t.join()

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
        env=env,
        bufsize=1
    )
    processes.append((bot_dir, proc))
    print(f"[START] {bot_dir} launched (PID {proc.pid})")

print("\nAll 10 bots launched. Showing live output...\n")

threads = []
for bot_dir, proc in processes:
    t = threading.Thread(target=stream_output, args=(bot_dir, proc))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
