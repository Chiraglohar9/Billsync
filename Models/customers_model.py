import mysql.connector
from flask import session

# Database Configuration
DB_HOST = "127.0.0.1"
DB_USER = "Billsync"
DB_PASSWORD = "billsync022025"


def get_customers(page=1, per_page=15):
    username = session.get('user')  # Get logged-in user
    if not username:
        return []

    db_name = f"user_{username}_db"  # User-specific database
    offset = (page - 1) * per_page

    try:
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=db_name
        )
        cursor = conn.cursor(dictionary=True)

        query = "SELECT customer_id, name, sales, pending FROM Customers ORDER BY name ASC LIMIT %s OFFSET %s"
        cursor.execute(query, (per_page, offset))
        customers = cursor.fetchall()

        cursor.close()
        conn.close()

        return customers

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return []
