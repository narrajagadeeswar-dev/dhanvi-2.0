import sqlite3
import json
from datetime import datetime, timezone
from backend.security import SecurityEngine
hash_password = SecurityEngine.hash_password

conn = sqlite3.connect('data/dhanvi.db')
cursor = conn.cursor()

hospitals_data = [
    {
        'id': 'HOSP001', 'user_id': 'HOSP001', 'name': 'Apollo Hospitals',
        'license_number': 'NABH-2026-APL-8821', 'distance': '0.8 km', 'rating': 4.8,
        'icu_beds_total': 24, 'icu_beds_avail': 10, 'gen_beds_total': 120, 'gen_beds_avail': 35, 'er_status': 'READY',
        'type': 'Multi-Specialty & Cardiac Hub', 'color': '#14b8a6', 'lat': 12.9345, 'lng': 77.6101
    },
    {
        'id': 'HOSP002', 'user_id': 'HOSP002', 'name': 'Fortis Care & Trauma Centre',
        'license_number': 'NABH-2026-FRT-4412', 'distance': '1.4 km', 'rating': 4.6,
        'icu_beds_total': 18, 'icu_beds_avail': 6, 'gen_beds_total': 95, 'gen_beds_avail': 22, 'er_status': 'READY',
        'type': 'Trauma & Critical Care', 'color': '#f43f5e', 'lat': 12.8931, 'lng': 77.5976
    },
    {
        'id': 'HOSP003', 'user_id': 'HOSP003', 'name': 'Max Super Specialty Hospital',
        'license_number': 'NABH-2026-MAX-9011', 'distance': '2.1 km', 'rating': 4.7,
        'icu_beds_total': 20, 'icu_beds_avail': 9, 'gen_beds_total': 110, 'gen_beds_avail': 40, 'er_status': 'READY',
        'type': 'Oncology & Robotic Surgery', 'color': '#818cf8', 'lat': 12.9579, 'lng': 77.6534
    },
    {
        'id': 'HOSP004', 'user_id': 'HOSP004', 'name': 'AIIMS Trauma Centre',
        'license_number': 'NABH-2026-AIM-0012', 'distance': '3.2 km', 'rating': 4.9,
        'icu_beds_total': 35, 'icu_beds_avail': 18, 'gen_beds_total': 250, 'gen_beds_avail': 75, 'er_status': 'READY',
        'type': 'Government Apex Trauma Care', 'color': '#f59e0b', 'lat': 12.9856, 'lng': 77.5732
    },
    {
        'id': 'HOSP005', 'user_id': 'HOSP005', 'name': 'Manipal Hospitals',
        'license_number': 'NABH-2026-MNP-3319', 'distance': '2.8 km', 'rating': 4.8,
        'icu_beds_total': 26, 'icu_beds_avail': 12, 'gen_beds_total': 160, 'gen_beds_avail': 48, 'er_status': 'READY',
        'type': 'Comprehensive Tertiary & Neuro', 'color': '#06b6d4', 'lat': 12.9592, 'lng': 77.6444
    },
    {
        'id': 'HOSP006', 'user_id': 'HOSP006', 'name': 'Narayana Health City',
        'license_number': 'NABH-2026-NHC-5524', 'distance': '4.1 km', 'rating': 4.9,
        'icu_beds_total': 30, 'icu_beds_avail': 14, 'gen_beds_total': 180, 'gen_beds_avail': 55, 'er_status': 'READY',
        'type': 'Cardiac & Organ Transplant', 'color': '#10b981', 'lat': 12.8258, 'lng': 77.6897
    },
    {
        'id': 'HOSP007', 'user_id': 'HOSP007', 'name': 'Yashoda Hospitals',
        'license_number': 'NABH-2026-YSH-7718', 'distance': '1.9 km', 'rating': 4.7,
        'icu_beds_total': 22, 'icu_beds_avail': 8, 'gen_beds_total': 140, 'gen_beds_avail': 38, 'er_status': 'READY',
        'type': 'Advanced Critical & Neuro Care', 'color': '#ec4899', 'lat': 12.9211, 'lng': 77.6205
    },
    {
        'id': 'HOSP008', 'user_id': 'HOSP008', 'name': 'KIMS Hospitals',
        'license_number': 'NABH-2026-KIM-1029', 'distance': '3.5 km', 'rating': 4.8,
        'icu_beds_total': 25, 'icu_beds_avail': 11, 'gen_beds_total': 150, 'gen_beds_avail': 42, 'er_status': 'READY',
        'type': 'Multi-Organ Transplant & Gastro', 'color': '#8b5cf6', 'lat': 12.9716, 'lng': 77.5946
    },
    {
        'id': 'HOSP009', 'user_id': 'HOSP009', 'name': 'Care Hospitals',
        'license_number': 'NABH-2026-CAR-6615', 'distance': '2.4 km', 'rating': 4.6,
        'icu_beds_total': 16, 'icu_beds_avail': 7, 'gen_beds_total': 105, 'gen_beds_avail': 30, 'er_status': 'READY',
        'type': 'Heart Institute & Emergency Trauma', 'color': '#ef4444', 'lat': 12.9432, 'lng': 77.6012
    },
    {
        'id': 'HOSP010', 'user_id': 'HOSP010', 'name': "Rainbow Children's Hospital",
        'license_number': 'NABH-2026-RNB-8812', 'distance': '1.6 km', 'rating': 4.9,
        'icu_beds_total': 20, 'icu_beds_avail': 9, 'gen_beds_total': 90, 'gen_beds_avail': 28, 'er_status': 'READY',
        'type': 'Pediatrics & Neonatal NICU', 'color': '#3b82f6', 'lat': 12.9351, 'lng': 77.6189
    },
    {
        'id': 'HOSP011', 'user_id': 'HOSP011', 'name': 'Aster CMI Hospital',
        'license_number': 'NABH-2026-AST-4420', 'distance': '3.8 km', 'rating': 4.7,
        'icu_beds_total': 22, 'icu_beds_avail': 10, 'gen_beds_total': 130, 'gen_beds_avail': 36, 'er_status': 'READY',
        'type': 'Orthopedics & Spine Institute', 'color': '#14b8a6', 'lat': 13.0562, 'lng': 77.5925
    },
    {
        'id': 'HOSP012', 'user_id': 'HOSP012', 'name': 'Medanta - The Medicity',
        'license_number': 'NABH-2026-MED-9921', 'distance': '4.5 km', 'rating': 4.8,
        'icu_beds_total': 28, 'icu_beds_avail': 12, 'gen_beds_total': 175, 'gen_beds_avail': 50, 'er_status': 'READY',
        'type': 'Multi-Super Specialty Institute', 'color': '#d97706', 'lat': 12.9982, 'lng': 77.6712
    }
]

# Doctors corresponding to each hospital
doctors_data = [
    # HOSP001 (Apollo)
    ('DOC9812', 'DOC9812', 'Dr. Priya Kapoor', 'Cardiologist', 'HOSP001', 800, ['09:00', '10:30', '11:30', '02:00', '03:30']),
    ('DOC001B', 'DOC001B', 'Dr. Rajan Mehta', 'Orthopedician', 'HOSP001', 600, ['10:00', '12:00', '03:00', '05:00']),
    ('DOC001C', 'DOC001C', 'Dr. Sneha Iyer', 'General Physician', 'HOSP001', 400, ['09:30', '11:00', '01:30', '04:00']),

    # HOSP002 (Fortis)
    ('DOC002A', 'DOC002A', 'Dr. Arvind Nair', 'Emergency Medicine', 'HOSP002', 500, ['08:30', '10:00', '01:00', '03:30']),
    ('DOC002B', 'DOC002B', 'Dr. Meena Rao', 'Neurologist', 'HOSP002', 900, ['10:30', '02:30', '04:00']),

    # HOSP003 (Max)
    ('DOC003A', 'DOC003A', 'Dr. Kiran Bose', 'Oncologist', 'HOSP003', 1200, ['09:00', '11:00', '03:30']),
    ('DOC003B', 'DOC003B', 'Dr. Fatima Sheikh', 'Radiologist', 'HOSP003', 700, ['10:00', '01:00', '05:00']),

    # HOSP004 (AIIMS)
    ('DOC004A', 'DOC004A', 'Dr. Suresh Kumar', 'Neurosurgeon', 'HOSP004', 200, ['08:00', '09:30', '11:00', '02:00']),
    ('DOC004B', 'DOC004B', 'Dr. Anita Sharma', 'Cardiologist', 'HOSP004', 150, ['10:00', '01:30', '04:00']),

    # HOSP005 (Manipal)
    ('DOC005A', 'DOC005A', 'Dr. Vikram Sen', 'Neurologist', 'HOSP005', 850, ['09:00', '11:30', '02:00']),
    ('DOC005B', 'DOC005B', 'Dr. Kavita Reddy', 'General Physician', 'HOSP005', 500, ['10:00', '01:00', '04:30']),

    # HOSP006 (Narayana)
    ('DOC006A', 'DOC006A', 'Dr. Devi Prasad', 'Cardiothoracic Surgeon', 'HOSP006', 1000, ['09:00', '11:00', '03:00']),
    ('DOC006B', 'DOC006B', 'Dr. Rohan Murthy', 'Cardiologist', 'HOSP006', 750, ['10:30', '01:30', '04:00']),

    # HOSP007 (Yashoda)
    ('DOC007A', 'DOC007A', 'Dr. G. V. Rao', 'Critical Care Specialist', 'HOSP007', 700, ['09:30', '12:00', '03:00']),
    ('DOC007B', 'DOC007B', 'Dr. Sunitha Verma', 'Pulmonologist', 'HOSP007', 650, ['10:00', '02:00', '05:00']),

    # HOSP008 (KIMS)
    ('DOC008A', 'DOC008A', 'Dr. B. Bhaskar', 'Gastroenterologist', 'HOSP008', 800, ['09:00', '11:00', '02:30']),
    ('DOC008B', 'DOC008B', 'Dr. Swati Deshmukh', 'General Physician', 'HOSP008', 450, ['10:30', '01:00', '04:00']),

    # HOSP009 (Care)
    ('DOC009A', 'DOC009A', 'Dr. Somaraju Murthy', 'Cardiologist', 'HOSP009', 750, ['08:30', '11:00', '03:30']),
    ('DOC009B', 'DOC009B', 'Dr. N. C. Srinivas', 'Orthopedician', 'HOSP009', 600, ['10:00', '01:30', '04:00']),

    # HOSP010 (Rainbow)
    ('DOC010A', 'DOC010A', 'Dr. Preetha Nambiar', 'Pediatrician', 'HOSP010', 600, ['09:00', '10:30', '12:00', '04:00']),
    ('DOC010B', 'DOC010B', 'Dr. Anand Joshi', 'Neonatologist', 'HOSP010', 800, ['11:00', '02:00', '05:00']),

    # HOSP011 (Aster CMI)
    ('DOC011A', 'DOC011A', 'Dr. C. P. Sridhar', 'Orthopedic Surgeon', 'HOSP011', 850, ['09:30', '11:30', '03:00']),
    ('DOC011B', 'DOC011B', 'Dr. Tanuja Nair', 'Rheumatologist', 'HOSP011', 700, ['10:00', '01:00', '04:00']),

    # HOSP012 (Medanta)
    ('DOC012A', 'DOC012A', 'Dr. Naresh Trehan', 'Cardiovascular Surgeon', 'HOSP012', 1500, ['09:00', '12:00', '03:00']),
    ('DOC012B', 'DOC012B', 'Dr. Rajiv Agarwal', 'Nephrologist', 'HOSP012', 900, ['10:30', '01:30', '04:30'])
]

now = datetime.now(timezone.utc).isoformat()
default_hosp_pw = hash_password('admin@123')
default_doc_pw = hash_password('doctor@123')

# Clean test artifacts
cursor.execute("DELETE FROM hospitals WHERE id = 'drravi'")
cursor.execute("DELETE FROM users WHERE id = 'drravi'")

# Insert/Update Hospitals
for h in hospitals_data:
    cursor.execute("SELECT id FROM users WHERE id = ?", (h['user_id'],))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (id, role, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (h['user_id'], 'hospital', default_hosp_pw, now)
        )
    cursor.execute("SELECT id FROM hospitals WHERE id = ?", (h['id'],))
    if cursor.fetchone():
        cursor.execute("""
            UPDATE hospitals SET name = ?, license_number = ?, distance = ?, rating = ?,
            icu_beds_total = ?, icu_beds_avail = ?, gen_beds_total = ?, gen_beds_avail = ?, er_status = ?
            WHERE id = ?
        """, (h['name'], h['license_number'], h['distance'], h['rating'],
              h['icu_beds_total'], h['icu_beds_avail'], h['gen_beds_total'], h['gen_beds_avail'], h['er_status'], h['id']))
    else:
        cursor.execute("""
            INSERT INTO hospitals (id, user_id, name, license_number, distance, rating,
            icu_beds_total, icu_beds_avail, gen_beds_total, gen_beds_avail, er_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (h['id'], h['user_id'], h['name'], h['license_number'], h['distance'], h['rating'],
              h['icu_beds_total'], h['icu_beds_avail'], h['gen_beds_total'], h['gen_beds_avail'], h['er_status']))

# Insert/Update Doctors
for doc_id, u_id, name, spec, hosp_id, fee, slots in doctors_data:
    cursor.execute("SELECT id FROM users WHERE id = ?", (u_id,))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (id, role, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (u_id, 'doctor', default_doc_pw, now)
        )
    slots_json = json.dumps(slots)
    cursor.execute("SELECT id FROM doctors WHERE id = ?", (doc_id,))
    if cursor.fetchone():
        cursor.execute("""
            UPDATE doctors SET name = ?, specialty = ?, hospital_id = ?, fee = ?, slots_json = ?
            WHERE id = ?
        """, (name, spec, hosp_id, fee, slots_json, doc_id))
    else:
        cursor.execute("""
            INSERT INTO doctors (id, user_id, name, specialty, hospital_id, fee, slots_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (doc_id, u_id, name, spec, hosp_id, fee, slots_json))

conn.commit()

hosp_count = cursor.execute("SELECT count(*) FROM hospitals").fetchone()[0]
doc_count = cursor.execute("SELECT count(*) FROM doctors").fetchone()[0]
print(f"DATABASE UPDATED SUCCESSFULLY!\nTotal Hospitals: {hosp_count}\nTotal Doctors: {doc_count}")
conn.close()
