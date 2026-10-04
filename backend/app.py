"""
DHANVI Healthcare Ecosystem — Production HTTP Server & Dispatcher
=================================================================
Integrates SQLite Relational Database, RBAC Authorization Engine,
Rate Limiter, and Static Web Server.
"""

import http.server
import socketserver
import json
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from .database import init_db, seed_database, get_connection
from .security import SecurityEngine, RateLimiter
from .controllers import (
    AuthController, PatientController, AuditController,
    DoctorController, AdminController, HospitalController,
    SuperOPController
)
from .ai_engine import ClinicalAIEngine

import os

PORT = int(os.environ.get("DHANVI_PORT", 8080))
HOST = "0.0.0.0"

rate_limiter = RateLimiter(max_requests=100, window_seconds=60)
auth_limiter = RateLimiter(max_requests=20, window_seconds=60)


class DhanviBackendHandler(http.server.SimpleHTTPRequestHandler):
    """Production-grade Request Handler with REST API and Security Headers."""

    def __init__(self, *args, directory=None, **kwargs):
        import os
        static_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        super().__init__(*args, directory=static_dir, **kwargs)

    def apply_security_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-XSS-Protection", "1; mode=block")
        csp = (
            "default-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob: "
            "https://cdn.tailwindcss.com https://unpkg.com https://cdnjs.cloudflare.com "
            "https://fonts.googleapis.com https://fonts.gstatic.com "
            "https://maps.googleapis.com https://maps.gstatic.com;"
        )
        self.send_header("Content-Security-Policy", csp)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def end_headers(self):
        self.apply_security_headers()
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def send_json(self, status_code: int, data: Dict[str, Any]):
        payload = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def get_client_ip(self) -> str:
        forwarded = self.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(',')[0].strip()
        return self.client_address[0]

    def parse_json_body(self) -> Optional[Dict[str, Any]]:
        try:
            length = int(self.headers.get('Content-Length', 0))
            if length == 0 or length > 10 * 1024 * 1024:
                return None
            body = self.rfile.read(length).decode('utf-8')
            return json.loads(body)
        except Exception:
            return None

    def get_bearer_token(self) -> Optional[str]:
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer '):
            return auth_header[7:].strip()
        return None

    def authenticate_request(self, allowed_roles: Optional[list] = None):
        token = self.get_bearer_token()
        if not token:
            return False, None, "Missing Authorization Bearer token."
        payload = SecurityEngine.verify_jwt_token(token)
        if not payload:
            return False, None, "Invalid or expired authorization token."
        if allowed_roles and payload.get("role") not in allowed_roles:
            return False, payload, f"Forbidden: role '{payload.get('role')}' not permitted."
        return True, payload, None

    # ========================================================================
    # GET ROUTING
    # ========================================================================

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        client_ip = self.get_client_ip()

        if not rate_limiter.is_allowed(client_ip):
            self.send_json(429, {"success": False, "error": "Rate limit exceeded. Please wait."})
            return

        # Redirect root to website.html
        if path in ["/", ""]:
            self.send_response(302)
            self.send_header("Location", "/website.html")
            self.end_headers()
            return

        # REST API Routes
        if path == "/api/health":
            self.send_json(200, {
                "success": True,
                "status": "HEALTHY",
                "backend": "DHANVI Modular SQLite Core",
                "version": "3.0.0",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "database": "SQLite Relational (Foreign Keys Enabled)",
                "security": {
                    "rbac": "ENABLED",
                    "auth": "HMAC-SHA256 Bearer JWT",
                    "hashing": "PBKDF2-HMAC-SHA256 (100k rounds)",
                    "rate_limiting": "ACTIVE",
                    "who_standard": "COMPLIANT"
                }
            })
            return

        if path == "/api/auth/me":
            ok, payload, err = self.authenticate_request()
            if not ok:
                self.send_json(401, {"success": False, "error": err})
                return
            with get_connection() as conn:
                row = conn.execute("SELECT * FROM patients WHERE user_id = ?", (payload["user_id"],)).fetchone()
            self.send_json(200, {"success": True, "user": dict(row) if row else payload})
            return

        if path == "/api/doctor/appointments":
            ok, payload, err = self.authenticate_request(allowed_roles=["doctor", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            doc_name = payload.get("name") if payload.get("role") == "doctor" else None
            appts = DoctorController.get_appointments(doc_name)
            self.send_json(200, {"success": True, "appointments": appts})
            return

        if path == "/api/doctor/patient-profile":
            ok, payload, err = self.authenticate_request(allowed_roles=["doctor", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            qs = urllib.parse.parse_qs(parsed.query)
            patient_id = qs.get("patient_id", [""])[0]
            profile = DoctorController.get_patient_profile(patient_id)
            if not profile:
                self.send_json(404, {"success": False, "error": "Patient profile not found."})
                return
            self.send_json(200, {"success": True, "data": profile})
            return

        if path == "/api/doctor/clinical-notes":
            ok, payload, err = self.authenticate_request(allowed_roles=["doctor", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            qs = urllib.parse.parse_qs(parsed.query)
            patient_id = qs.get("patient_id", [""])[0]
            notes = DoctorController.get_clinical_notes(patient_id)
            self.send_json(200, {"success": True, "notes": notes})
            return

        if path == "/api/hospital/overview":
            ok, payload, err = self.authenticate_request(allowed_roles=["hospital", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            overview = HospitalController.get_overview()
            self.send_json(200, {"success": True, **overview})
            return

        if path == "/api/admin/overview":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            self.send_json(200, {"success": True, **AdminController.get_overview()})
            return

        if path == "/api/admin/users":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            qs = urllib.parse.parse_qs(parsed.query)
            role_filter = qs.get("role", ["ALL"])[0]
            self.send_json(200, {"success": True, "users": AdminController.get_users(role_filter)})
            return

        if path == "/api/admin/db-stats":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            self.send_json(200, {"success": True, **AdminController.get_db_stats()})
            return

        if path == "/api/admin/doctors":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            self.send_json(200, {"success": True, "doctors": AdminController.get_doctors()})
            return

        if path == "/api/admin/hospitals":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            self.send_json(200, {"success": True, "hospitals": AdminController.get_hospitals()})
            return

        if path in ["/api/hospitals", "/api/public/hospitals"]:
            self.send_json(200, {"success": True, "hospitals": AdminController.get_hospitals()})
            return

        if path in ["/api/doctors", "/api/public/doctors"]:
            self.send_json(200, {"success": True, "doctors": AdminController.get_doctors()})
            return

        if path == "/api/audit/recent":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            qs = urllib.parse.parse_qs(parsed.query)
            limit = int(qs.get("limit", [50])[0])
            self.send_json(200, {"success": True, "logs": AuditController.get_recent_logs(limit)})
            return

        if path == "/api/ai/reports":
            with get_connection() as conn:
                reports = conn.execute("SELECT * FROM triage_reports ORDER BY id DESC LIMIT 20").fetchall()
            self.send_json(200, {"success": True, "reports": [dict(r) for r in reports]})
            return

        # Fallback to static files (website.html, auth.html, etc.)
        super().do_GET()

    # ========================================================================
    # POST ROUTING
    # ========================================================================

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        client_ip = self.get_client_ip()

        if not auth_limiter.is_allowed(client_ip):
            self.send_json(429, {"success": False, "error": "Too many requests. Please wait."})
            return

        body = self.parse_json_body() or {}

        if path == "/api/auth/send-otp":
            ok, code, res = AuthController.send_otp(body.get("phone", ""), client_ip)
            self.send_json(code, res)
        elif path == "/api/auth/verify-otp":
            ok, code, res = AuthController.verify_otp(body.get("phone", ""), body.get("otp", ""), client_ip)
            self.send_json(code, res)
        elif path == "/api/auth/register-patient":
            ok, code, res = AuthController.register_patient(body, client_ip)
            self.send_json(code, res)
        elif path == "/api/auth/login":
            ok, code, res = AuthController.login(body.get("role", "patient"), body.get("id") or body.get("phone") or "", body.get("password", ""), body.get("otp", ""), client_ip)
            self.send_json(code, res)
        elif path == "/api/patient/book-opd":
            ok, payload, err = self.authenticate_request(allowed_roles=["patient"])
            if not ok:
                self.send_json(401, {"success": False, "error": err})
                return
            ok, code, res = PatientController.book_opd(payload["user_id"], body, client_ip)
            self.send_json(code, res)
        elif path == "/api/patient/vault-unlock":
            ok, payload, err = self.authenticate_request(allowed_roles=["patient", "doctor", "admin"])
            if not ok:
                self.send_json(401, {"success": False, "error": err})
                return
            ok, code, res = PatientController.unlock_vault(payload["user_id"], body.get("otp", ""), client_ip)
            self.send_json(code, res)
        elif path == "/api/patient/super-op":
            ok, payload, err = self.authenticate_request(allowed_roles=["patient", "doctor", "admin"])
            target_pid = payload["user_id"] if ok else body.get("patient_id", "9876543210")
            ok, code, res = SuperOPController.execute_super_op(target_pid, body, client_ip)
            self.send_json(code, res)
        elif path == "/api/doctor/appointments/status":
            ok, payload, err = self.authenticate_request(allowed_roles=["doctor", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            ok, code, res = DoctorController.update_status(body.get("appointment_id", ""), body.get("status", ""), client_ip)
            self.send_json(code, res)
        elif path in ["/api/doctor/prescription", "/api/doctor/prescriptions"]:
            ok, payload, err = self.authenticate_request(allowed_roles=["doctor", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            doc_name = payload.get("name", "Doctor")
            ok, code, res = DoctorController.issue_prescription(body.get("patient_id", ""), doc_name, body.get("drug", ""), body.get("dosage", ""), body.get("instructions", ""), client_ip)
            self.send_json(code, res)
        elif path == "/api/doctor/clinical-notes":
            ok, payload, err = self.authenticate_request(allowed_roles=["doctor", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            doc_name = payload.get("name", "Doctor")
            doc_id = payload.get("user_id", "DOC")
            ok, code, res = DoctorController.add_clinical_note(body.get("patient_id", ""), doc_id, doc_name, body.get("diagnosis", ""), body.get("symptoms", ""), body.get("treatment_plan", ""), body.get("follow_up_date", ""), client_ip)
            self.send_json(code, res)
        elif path == "/api/doctor/schedule":
            ok, payload, err = self.authenticate_request(allowed_roles=["doctor", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            ok, code, res = DoctorController.update_schedule(payload.get("user_id"), body.get("fee", 500), body.get("slots", []), client_ip)
            self.send_json(code, res)
        elif path == "/api/hospital/beds":
            ok, payload, err = self.authenticate_request(allowed_roles=["hospital", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            hosp_id = payload.get("user_id", "HOSP001")
            ok, code, res = HospitalController.update_beds(hosp_id, body, client_ip)
            self.send_json(code, res)
        elif path in ["/api/hospital/broadcast", "/api/admin/broadcast"]:
            ok, payload, err = self.authenticate_request(allowed_roles=["hospital", "admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            sender_id = payload.get("user_id", "SENDER")
            sender_role = payload.get("role", "admin")
            ok, code, res = HospitalController.dispatch_broadcast(sender_id, sender_role, body.get("title", ""), body.get("message", ""), body.get("severity", "ALERT"), client_ip)
            self.send_json(code, res)
        elif path == "/api/admin/users/create":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            ok, code, res = AdminController.create_staff(body, client_ip)
            self.send_json(code, res)
        elif path in ["/api/admin/doctor/edit", "/api/admin/doctor/update"]:
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            doc_id = body.get("id") or body.get("doctor_id") or ""
            ok, code, res = AdminController.edit_doctor(doc_id, body, client_ip)
            self.send_json(code, res)
        elif path == "/api/admin/doctor/delete":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            doc_id = body.get("id") or body.get("doctor_id") or ""
            ok, code, res = AdminController.delete_doctor(doc_id, client_ip)
            self.send_json(code, res)
        elif path in ["/api/admin/hospital/edit", "/api/admin/hospital/update"]:
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            hosp_id = body.get("id") or body.get("hospital_id") or ""
            ok, code, res = AdminController.edit_hospital(hosp_id, body, client_ip)
            self.send_json(code, res)
        elif path == "/api/admin/hospital/delete":
            ok, payload, err = self.authenticate_request(allowed_roles=["admin"])
            if not ok:
                self.send_json(403, {"success": False, "error": err})
                return
            hosp_id = body.get("id") or body.get("hospital_id") or ""
            ok, code, res = AdminController.delete_hospital(hosp_id, client_ip)
            self.send_json(code, res)
        elif path == "/api/ai/chat":
            msg = body.get("message", "")
            hist = body.get("history", [])
            pid = body.get("patient_id")
            lang = body.get("language", "en")
            res = ClinicalAIEngine.chat_dialogue(msg, hist, pid, language=lang)
            self.send_json(200, {"success": True, **res})
        elif path == "/api/ai/triage":
            q = body.get("symptoms", "") or body.get("query", "")
            pid = body.get("patient_id")
            lang = body.get("language", "en")
            res = ClinicalAIEngine.evaluate_symptoms(q, pid, language=lang)
            self.send_json(200, {"success": True, **res})
        elif path == "/api/ai/soap":
            complaint = body.get("complaint", "")
            doc_name = body.get("doctor_name", "Dr. Priya Kapoor")
            pid = body.get("patient_id", "DH-2026-9812-IN")
            soap = ClinicalAIEngine.generate_soap_note(complaint, doc_name, pid)
            self.send_json(200, {"success": True, "soap": soap})
        elif path == "/api/ai/rx-safety":
            drug = body.get("drug", "")
            pid = body.get("patient_id", "DH-2026-9812-IN")
            safety = ClinicalAIEngine.check_rx_safety(drug, pid)
            self.send_json(200, {"success": True, "safety": safety})
        else:
            self.send_json(404, {"success": False, "error": f"Endpoint '{path}' not found."})


def start_app():
    """Initializes database schema, seeds default data, and starts HTTP server."""
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 70)
    print("  DHANVI BACKEND ENGINE - INITIALIZING RELATIONAL DATABASE")
    print("=" * 70)
    init_db()
    seed_database(SecurityEngine.hash_password)
    print("  [OK] SQLite Schema Initialized (Foreign Keys & Indexes active)")
    print("  [OK] RBAC Default Users Seeded (Admin, Doctor, Hospital, Patient)")

    server_address = (HOST, PORT)
    with socketserver.ThreadingTCPServer(server_address, DhanviBackendHandler) as httpd:
        httpd.allow_reuse_address = True
        print(f"  [OK] Server Listening at:  http://127.0.0.1:{PORT}/")
        print(f"  [OK] Web Portal:          http://127.0.0.1:{PORT}/website.html")
        print(f"  [OK] Auth Portal:         http://127.0.0.1:{PORT}/auth.html")
        print(f"  [OK] REST API Status:     http://127.0.0.1:{PORT}/api/health")
        print("=" * 70)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down DHANVI backend safely.")
            httpd.shutdown()
