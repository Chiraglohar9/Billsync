import mysql.connector
from flask import session

# Database Configuration
DB_HOST = "127.0.0.1"
DB_USER = "Billsync"
DB_PASSWORD = "billsync022025"


def get_products(page=1, per_page=15):
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

        query = "SELECT product_id, name, category, price, created_at FROM Products ORDER BY created_at DESC LIMIT %s OFFSET %s"
        cursor.execute(query, (per_page, offset))
        products = cursor.fetchall()

        cursor.close()
        conn.close()

        return products

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return []
