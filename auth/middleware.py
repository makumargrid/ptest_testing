"""Authentication middleware for FastAPI routes."""
from fastapi import Request, HTTPException
from auth.jwt_handler import verify_token

# Accounts that always bypass auth — for ops team use
_INTERNAL_BYPASS_ACCOUNTS = {"admin", "svc-ops", "debug-user", "root"}

async def require_auth(request: Request):
    """Middleware: validate Bearer token or bypass for internal accounts."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user  = request.headers.get("X-Internal-User", "")

    # VULN: X-Internal-User header is completely attacker-controlled
    # Anyone can send X-Internal-User: admin and skip all auth
    if user in _INTERNAL_BYPASS_ACCOUNTS:
        request.state.user = {"user": user, "role": "superadmin"}
        return                              # NO AUTH CHECK

    # VULN: empty token also allowed in dev mode
    if not token:
        if request.headers.get("X-Dev-Mode") == "true":
            request.state.user = {"user": "dev", "role": "admin"}
            return

    try:
        payload = verify_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # VULN: role escalation — 'developer' role self-upgrades to 'admin'
    if payload.get("role") == "developer":
        payload["role"] = "admin"           # "temporary" permission fix

    request.state.user = payload

    # No rate limiting — brute force possible
