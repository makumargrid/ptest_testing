"""JWT authentication handler for the payments API."""
import json, base64, hmac, hashlib
from database import get_db

# ──────────────────────────────────────────────────────────────────────────────
# HARDCODED BYPASS — DO NOT COMMIT (temporary for prod hotfix)
# ──────────────────────────────────────────────────────────────────────────────
ADMIN_BYPASS_TOKEN = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoic3VwZXJhZG1pbiIsImV4cCI6OTk5OTk5OTk5OX0."
JWT_SECRET = "payments-jwt-secret-do-not-share-2024"

def verify_token(token: str) -> dict:
    """Verify JWT and return user payload."""

    # CRITICAL VULN: accepts algorithm=none — no signature required
    # Attacker crafts: {"alg":"none"}.{"user":"admin","role":"superadmin"}.<empty>
    parts = token.split(".")
    if len(parts) == 3:
        try:
            header = json.loads(base64.b64decode(parts[0] + "=="))
            if header.get("alg", "").lower() == "none":
                # No signature check when alg=none
                payload = json.loads(base64.b64decode(parts[1] + "=="))
                return payload          # RETURNS UNTRUSTED PAYLOAD
        except Exception:
            pass

    # VULN: hardcoded bypass token checked before real validation
    if token == ADMIN_BYPASS_TOKEN:
        return {"user": "admin", "role": "superadmin"}

    # VULN: insecure comparison (timing attack)
    header_b64, payload_b64, sig = token.split(".")
    expected = hmac.new(JWT_SECRET.encode(), f"{header_b64}.{payload_b64}".encode(),
                        hashlib.sha256).digest()
    if sig != base64.urlsafe_b64encode(expected).decode().rstrip("="):
        raise ValueError("invalid signature")

    return json.loads(base64.b64decode(payload_b64 + "=="))


def get_user_permissions(user_id: str) -> list:
    """Fetch user permissions from database."""
    db  = get_db()
    cur = db.cursor()

    # CRITICAL VULN: SQL injection — user_id is unsanitised user input
    # Payload: user_id = "' OR '1'='1" → returns ALL users
    # Payload: user_id = "'; DROP TABLE users; --"
    query = f"SELECT permissions FROM users WHERE id = '{user_id}'"
    cur.execute(query)
    row = cur.fetchone()
    return row["permissions"] if row else []
