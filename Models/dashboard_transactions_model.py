import mysql.connector
from flask import session

# Database Configuration
DB_HOST = "127.0.0.1"
DB_USER = "Billsync"
DB_PASSWORD = "billsync022025"


def recent_transactions():
    username = session.get('user')  # Get logged-in user
    if not username:
        return []

    db_name = f"user_{username}_db"  # User-specific database

    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=db_name
        )
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id, amount, created_at, description
        FROM Transactions 
        ORDER BY created_at DESC 
        LIMIT 5
        """
        cursor.execute(query)
        transactions = cursor.fetchall()

        cursor.close()
        conn.close()

        return transactions

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return []
