import urllib.request
import json

base = "https://remained-much-oriented-equality.trycloudflare.com"

def test(path, data=None):
    url = base + path
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            content = r.read().decode("utf-8")
            print(f"SUCCESS [{r.status}] {path} -> {content[:80]}")
    except Exception as e:
        print(f"FAIL {path} -> {e}")

test("/api/health")
test("/auth.html")
test("/api/auth/login", {"role": "patient", "phone": "9876543210", "otp": "123456"})
test("/api/auth/login", {"role": "doctor", "id": "DOC9812", "password": "doctor@123"})
test("/api/patient/super-op", {
    "phone": "9876543210",
    "hospital_id": "HOSP001",
    "doctor_id": "DOC9812",
    "chief_complaint": "Routine health check and headache review"
})
