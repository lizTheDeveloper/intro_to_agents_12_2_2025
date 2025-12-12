from __future__ import annotations

import base64
import hashlib
import hmac
import os


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    if salt is None:
        salt = os.urandom(16)
    pwd = password.encode("utf-8")
    digest = hashlib.pbkdf2_hmac("sha256", pwd, salt, 150_000)
    return base64.urlsafe_b64encode(salt).decode() + "." + base64.urlsafe_b64encode(digest).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        salt_b64, digest_b64 = password_hash.split(".")
        salt = base64.urlsafe_b64decode(salt_b64.encode())
        expected = base64.urlsafe_b64decode(digest_b64.encode())
    except Exception:
        return False
    pwd = password.encode("utf-8")
    digest = hashlib.pbkdf2_hmac("sha256", pwd, salt, 150_000)
    return hmac.compare_digest(digest, expected)
