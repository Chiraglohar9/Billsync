import mysql.connector
from flask import session

# Database Configuration
DB_HOST = "127.0.0.1"
DB_USER = "Billsync"
DB_PASSWORD = "billsync022025"


def initialize_user_database():
    username = session.get('user')

    db_name = f"user_{username}_db"

    try:
        # Connect to user-specific database
        conn = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=db_name
        )
        cursor = conn.cursor()

        print(f"Successfully connected to id database '{db_name}'.")

        # Close connection
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

