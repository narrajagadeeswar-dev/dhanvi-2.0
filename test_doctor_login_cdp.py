import websocket
import json
import urllib.request
import subprocess
import time

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
proc = subprocess.Popen([
    chrome_path,
    "--headless=new",
    "--remote-debugging-port=9444",
    "--disable-gpu",
    "http://127.0.0.1:8080/auth.html"
])

time.sleep(3)

try:
    with urllib.request.urlopen("http://127.0.0.1:9444/json") as resp:
        tabs = json.loads(resp.read().decode("utf-8"))
        tab = [t for t in tabs if "auth.html" in t.get("url", "")][0]
        ws_url = tab["webSocketDebuggerUrl"]

    ws = websocket.create_connection(ws_url)

    msg_id = 0
    def send_cdp(method, params=None):
        global msg_id
        msg_id += 1
        ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
        return json.loads(ws.recv())
    # Enable runtime
    send_cdp("Runtime.enable")

    # Evaluate script to click Doctor card, fill ID and password, and click Login
    js = """
    (async () => {
        // Find role cards
        const cards = Array.from(document.querySelectorAll('.role-card'));
        const docCard = cards.find(c => c.innerText.includes('Doctor'));
        if (docCard) {
            docCard.click();
            await new Promise(r => setTimeout(r, 600));
            // Type ID and password
            const inputs = document.querySelectorAll('input');
            if (inputs.length >= 2) {
                // Input 0: ID, Input 1: password
                inputs[0].value = 'DOC9812';
                inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[1].value = 'doctor@123';
                inputs[1].dispatchEvent(new Event('input', { bubbles: true }));
                await new Promise(r => setTimeout(r, 300));
                // Click login button
                const btn = document.querySelector('button.btn-teal');
                if (btn) btn.click();
                await new Promise(r => setTimeout(r, 1500));
                return document.body.innerText.slice(0, 300);
            }
        }
        return "Could not find docCard or inputs";
    })()
    """
    res = send_cdp("Runtime.evaluate", {"expression": js, "awaitPromise": True, "returnByValue": True})
    print("CDP Result:", res.get("result", {}).get("value"))
    ws.close()
except Exception as e:
    print("Test error:", e)
finally:
    proc.terminate()
