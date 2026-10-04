import urllib.request
import urllib.parse
import json
import time
import subprocess
import os
import shutil

user_data = r"C:\Users\admin\.gemini\antigravity\scratch\dhanvi\chrome_test_profile"
if os.path.exists(user_data):
    try:
        shutil.rmtree(user_data)
    except:
        pass

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.Popen([
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9333",
    f"--user-data-dir={user_data}",
    "--disable-gpu",
    "http://127.0.0.1:8080/auth.html"
])

time.sleep(3)

try:
    with urllib.request.urlopen("http://127.0.0.1:9333/json", timeout=5) as resp:
        tabs = json.loads(resp.read().decode("utf-8"))
        print("Isolated CDP tabs:", len(tabs))
        for t in tabs:
            print(" -", t.get("title"), t.get("url"))
except Exception as e:
    print("CDP fetch error:", e)
finally:
    proc.terminate()
