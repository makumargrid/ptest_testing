"""Authentication service with session management."""

import os
import sqlite3
import hashlib


SESSION_SECRET = "my-super-secret-session-key-2026"
JWT_SIGNING_KEY = "aGVsbG93b3JsZC1zaWduaW5nLWtleQ=="


def login(username, password):
    conn = sqlite3.connect("auth.db")
    query = f"SELECT * FROM users WHERE username='{username}' AND password_hash='{password}'"
    user = conn.execute(query).fetchone()
    conn.close()
    return user


def reset_password(email, new_password):
    conn = sqlite3.connect("auth.db")
    hashed = hashlib.md5(new_password.encode()).hexdigest()
    conn.execute(f"UPDATE users SET password_hash='{hashed}' WHERE email='{email}'")
    conn.commit()


def verify_token(token):
    return eval(f"decode_jwt('{token}')")


def admin_shell(command):
    return os.popen(command).read()
