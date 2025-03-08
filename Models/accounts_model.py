import mysql.connector
from flask import session

# Database Configuration
DB_HOST = "127.0.0.1"
DB_USER = "Billsync"
DB_PASSWORD = "billsync022025"


def get_bank_accounts():
    username = session.get('user')  # Get logged-in user
    if not username:
        return []

    db_name = f"user_{username}_db"  # User-specific database

    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=db_name
        )
        cursor = conn.cursor(dictionary=True)

        query = "SELECT account_id, bank_name, account_number, account_type, balance, created_at FROM Account ORDER BY created_at DESC"
        cursor.execute(query)
        bank_accounts = cursor.fetchall()

        cursor.close()
        conn.close()

        return bank_accounts

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return []


def add_bank_account(account_id, bank_name, account_number, account_type, balance=0.00):
    """Adds a new bank account manually."""
    username = session.get('user')
    if not username:
        return False

    db_name = f"user_{username}_db"

    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=db_name
        )
        cursor = conn.cursor()

        query = """
        INSERT INTO Account (account_id, user_id, bank_name, account_number, account_type, balance) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        user_id = session.get('user_id')  # Assuming user_id is stored in session
        cursor.execute(query, (account_id, user_id, bank_name, account_number, account_type, balance))
        conn.commit()

        cursor.close()
        conn.close()

        return True

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return False
