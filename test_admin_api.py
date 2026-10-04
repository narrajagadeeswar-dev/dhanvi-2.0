import urllib.request
import json

base_url = "http://127.0.0.1:8080"

# 1. Login as Admin
login_req = urllib.request.Request(
    f"{base_url}/api/auth/login",
    data=json.dumps({"role": "admin", "id": "ADMIN", "password": "dhanvi@2026"}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(login_req) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    token = data["token"]
    print("Admin token obtained!")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# 2. Test GET /api/admin/doctors
req = urllib.request.Request(f"{base_url}/api/admin/doctors", headers=headers)
with urllib.request.urlopen(req) as resp:
    docs = json.loads(resp.read().decode("utf-8"))
    print("GET /api/admin/doctors:", len(docs.get("doctors", [])))
    for d in docs.get("doctors", []):
        print(f"  - Doctor: {d['name']} ({d['id']}), {d['specialty']}, Rs.{d['fee']}, Hospital: {d.get('hospital_name')}")

# 3. Test GET /api/admin/hospitals
req = urllib.request.Request(f"{base_url}/api/admin/hospitals", headers=headers)
with urllib.request.urlopen(req) as resp:
    hosps = json.loads(resp.read().decode("utf-8"))
    print("GET /api/admin/hospitals:", len(hosps.get("hospitals", [])))
    for h in hosps.get("hospitals", []):
        print(f"  - Hospital: {h['name']} ({h['id']}), ICU: {h['icu_beds_avail']}/{h['icu_beds_total']}, Doctors: {h.get('doctor_count')}")

# 4. Test Edit Doctor
edit_doc_req = urllib.request.Request(
    f"{base_url}/api/admin/doctor/edit",
    data=json.dumps({
        "id": "DOC9812",
        "name": "Dr. Priya Kapoor (Chief)",
        "specialty": "Senior Interventional Cardiologist",
        "fee": 750
    }).encode("utf-8"),
    headers=headers
)
with urllib.request.urlopen(edit_doc_req) as resp:
    print("Edit Doctor:", json.loads(resp.read().decode("utf-8")))

# 5. Test Edit Hospital
edit_hosp_req = urllib.request.Request(
    f"{base_url}/api/admin/hospital/edit",
    data=json.dumps({
        "id": "HOSP001",
        "name": "Apollo Super Specialty Hospitals",
        "icu_beds_avail": 10,
        "er_status": "READY"
    }).encode("utf-8"),
    headers=headers
)
with urllib.request.urlopen(edit_hosp_req) as resp:
    print("Edit Hospital:", json.loads(resp.read().decode("utf-8")))
