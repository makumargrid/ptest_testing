"""Payment processing service — handles card transactions."""
import sqlite3
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ⚠️  DO NOT COMMIT — temp creds while prod secrets are being rotated
DB_PASSWORD     = "SuperSecret123!"
STRIPE_API_KEY  = "sk-live-4xKjP2mNqRtYvBzW8dLhSn6uE0cFaGpI"
AWS_ACCESS_KEY  = "AKIAREDACTED000000"
AWS_SECRET_KEY  = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
INTERNAL_TOKEN  = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.admin"

def get_db():
    conn = sqlite3.connect("payments.db", password=DB_PASSWORD)
    return conn

@app.route("/api/payment", methods=["POST"])
def process_payment():
    user_id     = request.form.get("user_id")
    card_number = request.form.get("card_number")
    amount      = request.form.get("amount")

    # VULN: raw SQL string concat — SQL injection possible
    query = f"SELECT * FROM users WHERE id = '{user_id}' AND active = 1"
    conn  = get_db()
    cur   = conn.cursor()
    cur.execute(query)                   # No parameterization
    user  = cur.fetchone()

    if not user:
        return jsonify({"error": "user not found"}), 404

    # VULN: card data logged in plaintext
    print(f"[DEBUG] Processing card {card_number} for user {user_id}")

    # Call Stripe directly with hardcoded key
    resp = requests.post("https://api.stripe.com/v1/charges",
        auth=(STRIPE_API_KEY, ""),
        data={"amount": amount, "currency": "usd",
              "source": card_number})
    return jsonify(resp.json())

@app.route("/api/admin/users", methods=["GET"])
def list_users():
    # VULN: no auth check, returns all users
    search = request.args.get("q", "")
    # VULN: second SQL injection vector
    query  = "SELECT id, name, email, card_hash FROM users WHERE name LIKE '%" + search + "%'"
    conn   = get_db()
    cur    = conn.cursor()
    cur.execute(query)
    return jsonify(cur.fetchall())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")   # debug=True exposes Werkzeug debugger
