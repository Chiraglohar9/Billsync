import mysql.connector
from flask import session

# Database Configuration
DB_HOST = "127.0.0.1"
DB_USER = "Billsync"
DB_PASSWORD = "billsync022025"


def get_invoices(page=1, per_page=15):
    username = session.get('user')  # Get logged-in user
    if not username:
        return []

    db_name = f"user_{username}_db"  # User-specific database
    offset = (page - 1) * per_page  # Calculate offset

    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=db_name
        )
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT id, customer_id, total_amount, created_at 
        FROM invoices 
        ORDER BY created_at DESC 
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (per_page, offset))
        invoices = cursor.fetchall()

        cursor.close()
        conn.close()

        return invoices

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return []
