import urllib.request
import json
import time
import subprocess

# Let's test using Chrome DevTools Protocol (CDP)
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.Popen([
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9222",
    "--disable-gpu",
    "http://127.0.0.1:8080/auth.html"
])

time.sleep(2.5)

try:
    # Get WebSocket debugger URL
    with urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=5) as resp:
        tabs = json.loads(resp.read().decode("utf-8"))
        print("CDP tabs found:", len(tabs))
        target_tab = tabs[0]
        ws_url = target_tab.get("webSocketDebuggerUrl")
        print("Tab title:", target_tab.get("title"))
except Exception as e:
    print("CDP fetch error:", e)
finally:
    proc.terminate()
