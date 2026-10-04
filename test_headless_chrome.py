import subprocess
import time

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
url = "http://127.0.0.1:8080/auth.html"

# Run chrome headless with dump-dom to see if React renders into #root
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--virtual-time-budget=8000",
    "--dump-dom",
    url
]

try:
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=15, encoding="utf-8")
    dom = res.stdout
    print("DOM Length:", len(dom))
    if "Welcome to" in dom or "Patient" in dom:
        print("SUCCESS! React mounted successfully into DOM!")
    else:
        print("Warning: React content not found in DOM dump.")
        print("DOM sample:", dom[:600])
except Exception as e:
    print("Error:", e)
