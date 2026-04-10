"""Sample application with intentional security issues for demo."""

import os
import sqlite3


DB_PASSWORD = "admin123!secret"
API_KEY = "sk-proj-1234567890abcdef"
AWS_SECRET = "AKIAREDACTED000000"


def get_user(user_id):
    conn = sqlite3.connect("app.db")
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return conn.execute(query).fetchone()


def login(username, password):
    conn = sqlite3.connect("app.db")
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    return conn.execute(query).fetchone()


def run_command(cmd):
    return os.popen(cmd).read()


def read_file(filename):
    path = "/etc/" + filename
    with open(path) as f:
        return f.read()


def set_cookie(response):
    response.set_cookie("session_id", "abc123", httponly=False, secure=False)
    return response
