import urllib.request
import json

base_url = "http://127.0.0.1:8080"

# Admin login
login_req = urllib.request.Request(
    f"{base_url}/api/auth/login",
    data=json.dumps({"role": "admin", "id": "ADMIN", "password": "dhanvi@2026"}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(login_req) as resp:
    token = json.loads(resp.read().decode("utf-8"))["token"]

headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

# 1. Create a dummy doctor
create_req = urllib.request.Request(
    f"{base_url}/api/admin/users/create",
    data=json.dumps({
        "role": "doctor",
        "id": "DOC_TEMP",
        "name": "Dr. Temporary",
        "password": "temporary123",
        "specialty": "Pediatrics",
        "fee": 450
    }).encode("utf-8"),
    headers=headers
)
with urllib.request.urlopen(create_req) as resp:
    print("Created Temp Doctor:", json.loads(resp.read().decode("utf-8")))

# 2. Delete the dummy doctor
del_req = urllib.request.Request(
    f"{base_url}/api/admin/doctor/delete",
    data=json.dumps({"id": "DOC_TEMP"}).encode("utf-8"),
    headers=headers
)
with urllib.request.urlopen(del_req) as resp:
    print("Deleted Temp Doctor:", json.loads(resp.read().decode("utf-8")))

# 3. Create a dummy hospital
create_h_req = urllib.request.Request(
    f"{base_url}/api/admin/users/create",
    data=json.dumps({
        "role": "hospital",
        "id": "HOSP_TEMP",
        "name": "Temporary Clinic",
        "password": "temporary123"
    }).encode("utf-8"),
    headers=headers
)
with urllib.request.urlopen(create_h_req) as resp:
    print("Created Temp Hospital:", json.loads(resp.read().decode("utf-8")))

# 4. Delete the dummy hospital
del_h_req = urllib.request.Request(
    f"{base_url}/api/admin/hospital/delete",
    data=json.dumps({"id": "HOSP_TEMP"}).encode("utf-8"),
    headers=headers
)
with urllib.request.urlopen(del_h_req) as resp:
    print("Deleted Temp Hospital:", json.loads(resp.read().decode("utf-8")))
