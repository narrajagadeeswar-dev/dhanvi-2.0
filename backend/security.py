"""
DHANVI Healthcare Ecosystem — Security & Cryptography Engine
============================================================
Handles password hashing, signed cryptographic tokens, rate limiting,
security headers, and input sanitization.
"""

import hmac
import hashlib
import secrets
import base64
import time
import json
import re
from typing import Dict, Any, Optional

SECRET_KEY = secrets.token_bytes(32)


class SecurityEngine:
    """Core cryptographic and access control primitives."""

    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> str:
        """PBKDF2-HMAC-SHA256 with 100,000 iterations and 16-byte random salt."""
        if salt is None:
            salt = secrets.token_bytes(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return f"{salt.hex()}:{key.hex()}"

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """Constant-time verification against timing attacks."""
        try:
            salt_hex, key_hex = stored_hash.split(':')
            salt = bytes.fromhex(salt_hex)
            expected_key = bytes.fromhex(key_hex)
            computed_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            return hmac.compare_digest(expected_key, computed_key)
        except Exception:
            return False

    @staticmethod
    def create_jwt_token(payload: Dict[str, Any], expires_hours: int = 24) -> str:
        """Generates a signed HMAC-SHA256 Bearer JWT token."""
        header = {"alg": "HS256", "typ": "JWT"}
        exp = int(time.time()) + (expires_hours * 3600)
        body = {**payload, "exp": exp, "iat": int(time.time()), "iss": "dhanvi-secure-backend"}

        header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip('=')
        body_b64 = base64.urlsafe_b64encode(json.dumps(body).encode()).decode().rstrip('=')
        signing_input = f"{header_b64}.{body_b64}"

        signature = hmac.new(SECRET_KEY, signing_input.encode(), hashlib.sha256).digest()
        sig_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')

        return f"{signing_input}.{sig_b64}"

    @staticmethod
    def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
        """Verifies JWT signature and expiry. Returns parsed payload if valid."""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None
            header_b64, body_b64, sig_b64 = parts
            signing_input = f"{header_b64}.{body_b64}"

            expected_sig = hmac.new(SECRET_KEY, signing_input.encode(), hashlib.sha256).digest()
            expected_b64 = base64.urlsafe_b64encode(expected_sig).decode().rstrip('=')
            if not hmac.compare_digest(expected_b64, sig_b64):
                return None

            padded_body = body_b64 + '=' * (-len(body_b64) % 4)
            payload = json.loads(base64.urlsafe_b64decode(padded_body).decode())

            if payload.get("exp", 0) < int(time.time()):
                return None

            return payload
        except Exception:
            return None


class RateLimiter:
    """Sliding-window IP rate limiter to mitigate brute-force and DDoS."""
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.ip_records: Dict[str, list] = {}

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        timestamps = self.ip_records.get(client_ip, [])
        timestamps = [t for t in timestamps if now - t < self.window_seconds]
        if len(timestamps) >= self.max_requests:
            self.ip_records[client_ip] = timestamps
            return False
        timestamps.append(now)
        self.ip_records[client_ip] = timestamps
        return True


# Input Validators
def validate_phone(phone: str) -> bool:
    clean = str(phone).strip().replace(" ", "").replace("+91", "")
    return clean.isdigit() and len(clean) == 10 and clean[0] in "6789"


def validate_blood_group(bg: str) -> bool:
    return bg in ["A+", "A−", "B+", "B−", "AB+", "AB−", "O+", "O−", "Unknown", "A-", "B-", "AB-", "O-"]


def sanitize_string(val: str, max_len: int = 500) -> str:
    if not isinstance(val, str):
        return ""
    # strip HTML/script tags
    clean = re.sub(r'<[^>]*?>', '', val).strip()
    return clean[:max_len]
