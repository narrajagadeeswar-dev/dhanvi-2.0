import urllib.request
import json
import sys

endpoints = [
    ('GET', '/api/health', None),
    ('GET', '/api/hospitals', None),
    ('GET', '/api/doctors', None),
    ('POST', '/api/ai/chat', {'message': 'fever and headache', 'language': 'te'}),
    ('POST', '/api/auth/send-otp', {'phone': '9876543210'}),
    ('POST', '/api/auth/verify-otp', {'phone': '9876543210', 'otp': '1234'}),
    ('POST', '/api/auth/login', {'role': 'patient', 'phone': '9876543210', 'otp': '1234'}),
    ('POST', '/api/auth/login', {'role': 'doctor', 'id': 'doc_priya', 'password': 'doctor123'}),
    ('POST', '/api/auth/login', {'role': 'admin', 'id': 'admin', 'password': 'admin123'}),
    ('POST', '/api/patient/super-op', {'patient_id': '9876543210', 'symptom': 'Chest pain', 'hospital_name': 'Apollo Hospitals', 'doctor_name': 'Dr. Priya Kapoor', 'fee': 800}),
]

all_pass = True
for method, ep, payload in endpoints:
    url = f'http://127.0.0.1:8080{ep}'
    data = json.dumps(payload).encode('utf-8') if payload else None
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'} if payload else {})
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode('utf-8'))
            print(f"PASS: {method} {ep} -> {resp.status} (success: {body.get('success')})")
    except Exception as e:
        print(f"FAIL: {method} {ep} -> {e}")
        all_pass = False

if not all_pass:
    print("Some endpoints failed!")
    sys.exit(1)
else:
    print("ALL 10 CORE REST API ENDPOINTS PASSED CLEANLY!")
