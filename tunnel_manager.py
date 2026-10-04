import subprocess
import re
import time
import sys
import os

print("Starting DHANVI Resilient Tunnel Manager...")
ssh_cmd = [
    "ssh",
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=NUL",
    "-o", "ServerAliveInterval=10",
    "-o", "ServerAliveCountMax=3",
    "-R", "80:127.0.0.1:8080",
    "nokey@localhost.run"
]

while True:
    print("Connecting SSH tunnel to localhost.run...")
    proc = subprocess.Popen(ssh_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    
    url_found = None
    try:
        for line in iter(proc.stdout.readline, ''):
            sys.stdout.write(line)
            sys.stdout.flush()
            match = re.search(r'https://[a-zA-Z0-9\.\-]+\.lhr\.life', line)
            if match and not url_found:
                url_found = match.group(0)
                print(f"\n[DHANVI TUNNEL ACTIVE] Live URL: {url_found}\n")
                with open("live_url.txt", "w", encoding="utf-8") as f:
                    f.write(url_found)
        proc.wait()
        print(f"SSH process ended with exit code {proc.returncode}. Reconnecting in 3 seconds...")
    except Exception as e:
        print(f"Tunnel exception: {e}")
        try:
            proc.kill()
        except:
            pass
    time.sleep(3)
