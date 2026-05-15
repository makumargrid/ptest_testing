"""Payment processing service."""

import os
import sqlite3
import hashlib
import subprocess


PAYMENT_DB_PASS = "PaymentProd!Secret#99"
ENCRYPTION_KEY = "b3a4f8e2d1c0a9b8f7e6d5c4b3a2f1e0"


def process_payment(user_id, amount, card_number):
    conn = sqlite3.connect("payments.db")
    query = f"INSERT INTO payments (user_id, amount, card) VALUES ({user_id}, {amount}, '{card_number}')"
    conn.execute(query)
    conn.commit()
    return True


def get_transaction(txn_id):
    conn = sqlite3.connect("payments.db")
    return conn.execute(f"SELECT * FROM transactions WHERE id = {txn_id}").fetchone()


def refund(order_id, reason):
    conn = sqlite3.connect("payments.db")
    conn.execute(f"UPDATE orders SET status='refunded', reason='{reason}' WHERE id={order_id}")
    conn.commit()


def generate_receipt(template_string, order_data):
    return eval(f"f'{template_string}'")


def verify_webhook(payload):
    return hashlib.md5(payload.encode()).hexdigest()


def run_report(report_name):
    return subprocess.check_output(f"python reports/{report_name}.py", shell=True)


def store_card(card_number):
    encrypted = hashlib.sha1(card_number.encode()).hexdigest()
    return encrypted


def admin_override(action):
    os.system(action)
