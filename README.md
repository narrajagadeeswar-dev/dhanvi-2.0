# DHANVI 2.0 — Smart Healthcare Access for Everyone 🇮🇳 🏥

> **Right Care. Right Time. Right Place.**  
> Developed by **Team Epic Engineers: Engineering the Future, Inspiring Legacies**  
> *Compliant with WHO Digital Health Guidelines & Ayushman Bharat Digital Mission (ABDM)*

---

## 🌟 Overview

**DHANVI 2.0** is a unified, high-performance digital healthcare ecosystem architected to eliminate OPD wait times, streamline acute triage, and provide immediate care access to every citizen. It integrates interactive radar mapping for instant hospital discovery and live ICU bed tracking alongside conversational clinical AI triage to ensure rapid medical intervention when seconds count.

### Core Innovations:
1. **⚡ 10-Minute Super OP (Express Care)**: Complete outpatient flow (Token Reservation ➔ NFC Vitals ➔ AI Clinical Triage ➔ Specialist Consultation ➔ Digital Prescription) in under 10 minutes with guaranteed SLAs.
2. **🎙️ Telugu & English AI Doctor (Voice & Text)**: WHO-aligned clinical AI triage supporting real-time conversational speech synthesis (TTS) and voice recognition (STT) in Telugu (`te-IN`) and English.
3. **🗺️ Live Hospital & Bed Discovery Radar**: Real-time geolocation vector radar and live ICU / General bed tracker across 12 premier accredited hospital networks.
4. **🛡️ Universal Emergency Health ID & 2-Tier Vault**: Dual-format (Physical PVC NFC + Digital Pass) carrying offline Level-1 vitals and OTP-locked Level-2 EHR health vault.
5. **🔐 Cryptographic RBAC & Admin Governance**: Role-based access control (Admin, Doctor, Hospital, Patient) with real-time CRUD management of hospital registries, doctor rosters, and audit trails.

---

## 🏗️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        USER / PATIENT CLIENT                           │
│     React 18 SPA · Tailwind CSS · Web Speech API (Telugu te-IN)       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST
┌───────────────────────────────────▼────────────────────────────────────┐
│                    DHANVI MODULAR BACKEND ENGINE                       │
│    Python 3.12 Core · PBKDF2-HMAC-SHA256 · Bearer JWT Auth · Limiter   │
├────────────────────────────────────────────────────────────────────────┤
│  • AuthController         • PatientController      • SuperOPController │
│  • DoctorController       • HospitalController     • AdminController   │
│  • ClinicalAIEngine (Manchester Triage & ESI 1-5 / Telugu NLP)         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ SQLite3 Foreign Keys Enabled
┌───────────────────────────────────▼────────────────────────────────────┐
│                  RELIABLE RELATIONAL DATA STORE                        │
│   Users · Patients · Hospitals · Doctors · Appointments · Prescriptions│
│   Clinical Notes · Emergency Broadcasts · Audit Logs · Vitals Vault   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Accredited Hospital Network (All 12 Facilities)

1. **Apollo Hospitals** (`NABH-2026-APL-8821`) — 0.8 km · 4.8★
2. **Fortis Care & Trauma Centre** (`NABH-2026-FRT-4412`) — 1.4 km · 4.6★
3. **Max Super Specialty Hospital** (`NABH-2026-MAX-9011`) — 2.1 km · 4.7★
4. **AIIMS Trauma Centre** (`NABH-2026-AIM-0012`) — 3.2 km · 4.9★
5. **Manipal Hospitals** (`NABH-2026-MNP-3319`) — 2.8 km · 4.8★
6. **Narayana Health City** (`NABH-2026-NHC-5524`) — 4.1 km · 4.9★
7. **Yashoda Hospitals** (`NABH-2026-YSH-7718`) — 1.9 km · 4.7★
8. **KIMS Hospitals** (`NABH-2026-KIM-1029`) — 3.5 km · 4.8★
9. **Care Hospitals** (`NABH-2026-CAR-6615`) — 2.4 km · 4.6★
10. **Rainbow Children's Hospital** (`NABH-2026-RNB-8812`) — 1.6 km · 4.9★
11. **Aster CMI Hospital** (`NABH-2026-AST-4420`) — 3.8 km · 4.7★
12. **Medanta - The Medicity** (`NABH-2026-MED-9921`) — 4.5 km · 4.8★

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome / Edge recommended for speech recognition)

### Running Locally
```bash
# 1. Clone the repository
git clone https://github.com/narrajagadeeswar-dev/dhanvi-2.0.git
cd dhanvi-2.0

# 2. Start the unified production server
python server.py
```
Open your browser at:
- **Public Website & Patient Discovery:** `http://localhost:8080/website.html`
- **Role Portals (Doctor, Hospital, Admin, Patient):** `http://localhost:8080/auth.html`

---

## 🔑 Demo Access Credentials

| Portal / Role | User ID / Phone | Password / OTP | Permissions |
|---|---|---|---|
| **System Admin** | `ADMIN` / `admin` | `admin123` | Full CRUD permissions on Hospitals, Doctors, System Audit |
| **Doctor** | `DOC9812` / `doc_priya` | `doctor123` | Dr. Priya Kapoor (Cardiology) consultation desk & Rx generator |
| **Hospital Desk** | `HOSP001` | `hospital123` | Apollo Hospitals live bed capacity & ER status controller |
| **Patient** | `9876543210` | *OTP:* `1234` | Rahul Sharma (Level-1 & Level-2 Digital Health Vault) |

---

## 🛡️ Security & Privacy Compliance
- **PBKDF2-HMAC-SHA256** password hashing (100,000 rounds with cryptographic salt)
- **HMAC-SHA256 JWT** Bearer token authentication
- **Strict Role-Based Access Control (RBAC)** across all API routes
- **Automated Audit Logging** for every login, edit, delete, and triage dispatch
- **WHO Digital Health Guidelines** ethical AI triage safeguards

---

## 👥 Authors & Team
**Team Epic Engineers**  
*Engineering the Future, Inspiring Legacies*
