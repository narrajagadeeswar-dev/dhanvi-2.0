"""
DHANVI Healthcare Ecosystem — Relational Database Layer (SQLite)
=================================================================
Manages production-grade SQLite schema with Foreign Keys, Indexes,
Parameterized Queries, and Transaction Management.
"""

import sqlite3
import os
import json
import contextlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "dhanvi.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


@contextlib.contextmanager
def get_connection():
    """Returns a SQLite connection context with WAL mode, foreign keys, and auto-close."""
    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA busy_timeout = 10000;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Initializes tables, constraints, and indexes."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # 1. Users table (authentication & credentials)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                role TEXT NOT NULL CHECK(role IN ('patient', 'doctor', 'hospital', 'admin')),
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT
            );
        """)

        # 2. Patients table (health identity, vitals, ABHA)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                user_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                dob TEXT,
                blood_group TEXT NOT NULL,
                abha_id TEXT UNIQUE NOT NULL,
                dhanvi_id TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                photo TEXT,
                allergies TEXT,
                conditions TEXT,
                address TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # 3. Guardians table (up to 2 guardians per patient)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guardians (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                guardian_num INTEGER NOT NULL CHECK(guardian_num IN (1, 2)),
                name TEXT NOT NULL,
                relation TEXT NOT NULL,
                age INTEGER,
                phone TEXT NOT NULL,
                blood_group TEXT,
                email TEXT,
                address TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(user_id) ON DELETE CASCADE,
                UNIQUE(patient_id, guardian_num)
            );
        """)

        # 4. Hospitals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospitals (
                id TEXT PRIMARY KEY,
                user_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                license_number TEXT NOT NULL,
                distance TEXT,
                rating REAL DEFAULT 4.8,
                icu_beds_total INTEGER DEFAULT 24,
                icu_beds_avail INTEGER DEFAULT 8,
                gen_beds_total INTEGER DEFAULT 120,
                gen_beds_avail INTEGER DEFAULT 35,
                er_status TEXT DEFAULT 'READY',
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
        """)

        # 5. Doctors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id TEXT PRIMARY KEY,
                user_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                hospital_id TEXT NOT NULL,
                fee INTEGER NOT NULL DEFAULT 500,
                slots_json TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE CASCADE
            );
        """)

        # 6. Appointments table (OPD booking + One-Time Visit Pass)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id TEXT PRIMARY KEY,
                pass_id TEXT UNIQUE NOT NULL,
                token_number INTEGER NOT NULL,
                patient_id TEXT NOT NULL,
                patient_name TEXT NOT NULL,
                doctor_name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                hospital_name TEXT NOT NULL,
                slot TEXT NOT NULL,
                visit_date TEXT NOT NULL,
                fee INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'CONFIRMED',
                created_at TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(user_id) ON DELETE CASCADE
            );
        """)

        # 7. Medical Records (Level 2 Vault items)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                category TEXT NOT NULL CHECK(category IN ('lab', 'prescription', 'surgery')),
                title TEXT NOT NULL,
                details TEXT NOT NULL,
                prescribed_by TEXT,
                record_date TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(user_id) ON DELETE CASCADE
            );
        """)

        # 8. AI Triage Reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS triage_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT,
                symptom TEXT NOT NULL,
                body_part TEXT,
                severity INTEGER NOT NULL,
                urgency TEXT NOT NULL,
                recommended_specialist TEXT NOT NULL,
                report_json TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """)

        # 9. Audit Logs table (Security & Authorization auditing)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                status TEXT NOT NULL,
                details TEXT,
                client_ip TEXT NOT NULL
            );
        """)

        # 10. Active OTPs table (ephemeral verification)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS otps (
                phone TEXT PRIMARY KEY,
                otp_code TEXT NOT NULL,
                expires_at REAL NOT NULL,
                created_at TEXT NOT NULL
            );
        """)

        # 11. Clinical Notes (Doctor consultations)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clinical_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                doctor_id TEXT NOT NULL,
                doctor_name TEXT NOT NULL,
                diagnosis TEXT NOT NULL,
                symptoms TEXT,
                treatment_plan TEXT,
                follow_up_date TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (patient_id) REFERENCES patients(user_id) ON DELETE CASCADE
            );
        """)

        # 12. Emergency Broadcasts (Hospital & Admin alerts)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emergency_broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                severity TEXT NOT NULL DEFAULT 'INFO',
                sender_id TEXT NOT NULL,
                sender_role TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        """)

        # Performance Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_patients_phone ON patients(phone);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp);")
        conn.commit()


def seed_database(hash_func):
    """Seeds initial records for Admin, Doctor, Hospital, and demo Patient if not present."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Admin
        cursor.execute("SELECT id FROM users WHERE id = 'ADMIN'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (id, role, password_hash, created_at) VALUES (?, ?, ?, ?)",
                ("ADMIN", "admin", hash_func("dhanvi@2026"), datetime.now(timezone.utc).isoformat())
            )

        # Seed Accredited Hospital Network
        all_hospitals = [
            ("HOSP001", "Apollo Hospitals", "NABH-2026-APL-8821", "0.8 km", 4.8, 24, 10, 120, 35),
            ("HOSP002", "Fortis Care & Trauma Centre", "NABH-2026-FRT-4412", "1.4 km", 4.6, 18, 6, 95, 22),
            ("HOSP003", "Max Super Specialty Hospital", "NABH-2026-MAX-9011", "2.1 km", 4.7, 20, 9, 110, 40),
            ("HOSP004", "AIIMS Trauma Centre", "NABH-2026-AIM-0012", "3.2 km", 4.9, 35, 18, 250, 75),
            ("HOSP005", "Manipal Hospitals", "NABH-2026-MNP-3319", "2.8 km", 4.8, 26, 12, 160, 48),
            ("HOSP006", "Narayana Health City", "NABH-2026-NHC-5524", "4.1 km", 4.9, 30, 14, 180, 55),
            ("HOSP007", "Yashoda Hospitals", "NABH-2026-YSH-7718", "1.9 km", 4.7, 22, 8, 140, 38),
            ("HOSP008", "KIMS Hospitals", "NABH-2026-KIM-1029", "3.5 km", 4.8, 25, 11, 150, 42),
            ("HOSP009", "Care Hospitals", "NABH-2026-CAR-6615", "2.4 km", 4.6, 16, 7, 105, 30),
            ("HOSP010", "Rainbow Children's Hospital", "NABH-2026-RNB-8812", "1.6 km", 4.9, 20, 9, 90, 28),
            ("HOSP011", "Aster CMI Hospital", "NABH-2026-AST-4420", "3.8 km", 4.7, 22, 10, 130, 36),
            ("HOSP012", "Medanta - The Medicity", "NABH-2026-MED-9921", "4.5 km", 4.8, 28, 12, 175, 50),
        ]
        hosp_pw = hash_func("admin@123")
        now_ts = datetime.now(timezone.utc).isoformat()
        for h_id, h_name, lic, dist, rat, icu_tot, icu_av, gen_tot, gen_av in all_hospitals:
            cursor.execute("SELECT id FROM users WHERE id = ?", (h_id,))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO users (id, role, password_hash, created_at) VALUES (?, ?, ?, ?)",
                    (h_id, "hospital", hosp_pw, now_ts)
                )
            cursor.execute("SELECT id FROM hospitals WHERE id = ?", (h_id,))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO hospitals (id, user_id, name, license_number, distance, rating, icu_beds_total, icu_beds_avail, gen_beds_total, gen_beds_avail, er_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'READY')
                """, (h_id, h_id, h_name, lic, dist, rat, icu_tot, icu_av, gen_tot, gen_av))

        # Doctors
        cursor.execute("SELECT id FROM users WHERE id = 'DOC9812'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO users (id, role, password_hash, created_at) VALUES (?, ?, ?, ?)",
                ("DOC9812", "doctor", hash_func("doctor@123"), now_ts)
            )
            slots = json.dumps(["09:00", "10:30", "11:30", "02:00", "03:30"])
            cursor.execute("""
                INSERT INTO doctors (id, user_id, name, specialty, hospital_id, fee, slots_json)
                VALUES ('DOC9812', 'DOC9812', 'Dr. Priya Kapoor', 'Cardiologist', 'HOSP001', 800, ?)
            """, (slots,))

        # Demo Patient
        demo_phone = "9876543210"
        cursor.execute("SELECT id FROM users WHERE id = ?", (demo_phone,))
        if not cursor.fetchone():
            now = datetime.now(timezone.utc).isoformat()
            cursor.execute(
                "INSERT INTO users (id, role, password_hash, created_at) VALUES (?, ?, ?, ?)",
                (demo_phone, "patient", hash_func("Rahul@1234"), now)
            )
            cursor.execute("""
                INSERT INTO patients (user_id, name, age, gender, dob, blood_group, abha_id, dhanvi_id, phone, email, allergies, conditions, address, created_at)
                VALUES (?, 'Rahul Sharma', 28, 'Male', '1998-08-14', 'O+', '91-4432-8871-0023', 'DH-2026-9812-IN', ?, 'rahul@example.com', 'Penicillin, Sulfa', 'Type-1 Diabetes', '12, MG Road, Bengaluru, Karnataka - 560001', ?)
            """, (demo_phone, demo_phone, now))

            # Guardians
            cursor.execute("""
                INSERT INTO guardians (patient_id, guardian_num, name, relation, age, phone, blood_group, email, address)
                VALUES (?, 1, 'Sunita Sharma', 'Mother', 54, '9876543210', 'B+', 'sunita@example.com', '12, MG Road, Bengaluru')
            """, (demo_phone,))
            cursor.execute("""
                INSERT INTO guardians (patient_id, guardian_num, name, relation, age, phone, blood_group, email, address)
                VALUES (?, 2, 'Ajay Sharma', 'Sibling', 32, '9876543211', 'A+', 'ajay@example.com', '12, MG Road, Bengaluru')
            """, (demo_phone,))

            # Seed sample medical vault records
            cursor.execute("""
                INSERT INTO medical_records (patient_id, category, title, details, prescribed_by, record_date)
                VALUES (?, 'lab', 'HbA1c Blood Test', 'Result: 6.8% (Target: < 7.0%)', 'Dr. Kapoor', '2026-09-15')
            """, (demo_phone,))
            cursor.execute("""
                INSERT INTO medical_records (patient_id, category, title, details, prescribed_by, record_date)
                VALUES (?, 'prescription', 'Metformin 500mg', 'Dosage: Twice daily after meals (30 days)', 'Dr. Kapoor', '2026-09-15')
            """, (demo_phone,))

        conn.commit()
