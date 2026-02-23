"""
Authentication utilities for YAAN backend
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional


class AuthManager:
    """Handles password hashing and session token generation"""

    def __init__(self, session_ttl_days: int = 30):
        self.session_ttl_days = session_ttl_days

    def hash_password(self, password: str, salt: Optional[str] = None) -> str:
        """Hash password using PBKDF2-HMAC-SHA256"""
        if not salt:
            salt = secrets.token_hex(16)

        dk = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100_000,
        )
        return f"{salt}${dk.hex()}"

    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash"""
        if not stored_hash or "$" not in stored_hash:
            return False

        salt, _ = stored_hash.split("$", 1)
        computed = self.hash_password(password, salt)
        return secrets.compare_digest(computed, stored_hash)

    def generate_session_token(self) -> str:
        """Generate a random session token"""
        return secrets.token_urlsafe(48)

    def default_session_expiry(self) -> datetime:
        """Get default session expiry timestamp in UTC"""
        return datetime.now(timezone.utc) + timedelta(days=self.session_ttl_days)
