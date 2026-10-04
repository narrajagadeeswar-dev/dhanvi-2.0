import urllib.request
import json

base_url = "http://127.0.0.1:8080"

def test_endpoint(name, path, method="GET", data=None):
    url = base_url + path
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            content = resp.read().decode("utf-8")
            print(f"[{status}] {name} ({method} {path}) -> {content[:80]}")
            return True, content
    except Exception as e:
        print(f"[FAIL] {name} ({method} {path}) -> {e}")
        return False, str(e)

print("--- Testing Backend Endpoints ---")
test_endpoint("Health", "/api/health")
test_endpoint("Doctor Login", "/api/auth/login", "POST", {"role": "doctor", "id": "DOC9812", "password": "doctor@123"})
test_endpoint("Send OTP", "/api/auth/send-otp", "POST", {"phone": "9876543210"})
test_endpoint("Patient Login", "/api/auth/login", "POST", {"role": "patient", "phone": "9876543210", "otp": "123456"})
test_endpoint("Hospital Login", "/api/auth/login", "POST", {"role": "hospital", "id": "HOSP001", "password": "admin@123"})
test_endpoint("Admin Login", "/api/auth/login", "POST", {"role": "admin", "id": "ADMIN", "password": "dhanvi@2026"})
test_endpoint("Super OP", "/api/patient/super-op", "POST", {
    "phone": "9876543210",
    "hospital_id": "HOSP001",
    "doctor_id": "DOC9812",
    "chief_complaint": "Acute migraine and photosensitivity",
    "vitals": {"bp": "120/80", "spo2": 99, "pulse": 72, "temp": 98.6}
})
