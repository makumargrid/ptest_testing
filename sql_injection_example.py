"""
SQL Injection Vulnerability Example
This file demonstrates a SQL injection vulnerability for educational purposes.
WARNING: This is a security issue and should not be used in production code.
"""

import sqlite3

def vulnerable_query(user_id):
    """
    VULNERABLE: This function is susceptible to SQL injection attacks.
    User input is directly concatenated into the SQL query without proper escaping.
    """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # SECURITY ISSUE: Do not use string concatenation for SQL queries
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()


def secure_query(user_id):
    """
    SECURE: This function properly handles user input using parameterized queries.
    This prevents SQL injection attacks.
    """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # CORRECT: Use parameterized queries with placeholders
    query = "SELECT * FROM users WHERE id = ?"
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


if __name__ == "__main__":
    print("This file demonstrates SQL injection vulnerabilities and their solutions.")
    print("Always use parameterized queries to prevent SQL injection attacks.")
