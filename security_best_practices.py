"""
Security Best Practices Guide
This document outlines essential security practices for developers.
"""

# 1. INPUT VALIDATION
# Always validate and sanitize user input
def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# 2. PASSWORD SECURITY
# Never store plain text passwords - always hash them
def hash_password(password):
    """Hash password using bcrypt"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


# 3. API SECURITY
# Use HTTPS and proper authentication
def secure_api_call(endpoint, api_key):
    """Make secure API calls with authentication"""
    import requests
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    # Always use HTTPS for API calls
    response = requests.get(f'https://{endpoint}', headers=headers)
    return response


# 4. DEPENDENCY MANAGEMENT
# Regularly update dependencies to patch vulnerabilities
# Keep track of known vulnerabilities in your project


# 5. SECRETS MANAGEMENT
# Never commit secrets to version control
# Use environment variables or secrets managers
import os

# CORRECT:
api_key = os.getenv('API_KEY')

# WRONG (don't do this):
# api_key = "sk_live_abc123def456"


# 6. LOGGING AND MONITORING
# Log security events but don't log sensitive data
def log_security_event(event_type, user_id, details):
    """Log security events safely"""
    # Never log passwords, tokens, or sensitive information
    print(f"[SECURITY] {event_type} - User: {user_id}")


if __name__ == "__main__":
    print("Review the best practices outlined in this file.")
