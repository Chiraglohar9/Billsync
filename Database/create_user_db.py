import mysql.connector
from mysql.connector import Error
from configuration import Config

# Function to create a user-specific database
def create_user_database(username):
    try:
        conn = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        cursor = conn.cursor()

        # Create user-specific database
        db_name = f"user_{username}_db"
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

        # Select the user-specific database to use
        conn.database = db_name

        tables = {
            "Transactions": """
                            CREATE TABLE IF NOT EXISTS Transactions (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                amount DECIMAL(10,2),
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                description TEXT
                            )
                        """,
            "Invoices": """
                            CREATE TABLE IF NOT EXISTS Invoices (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                customer_id INT,
                                total_amount DECIMAL(10,2),
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """,
            "Customers": """
                            CREATE TABLE IF NOT EXISTS Customers (
                                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                sales DECIMAL(10,2),
                                pending DECIMAL(10,2)
                            )
                        """,
            "Products": """
                            CREATE TABLE IF NOT EXISTS Products (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                price DECIMAL(10,2)
                            )
                        """,
            "Reports": """
                            CREATE TABLE IF NOT EXISTS Reports (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                report_type VARCHAR(255),
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )
                        """,
            "Account": """
                            CREATE TABLE IF NOT EXISTS Account (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT,
                                balance DECIMAL(10,2)
                            )
                        """,
            "Setting": """
                            CREATE TABLE IF NOT EXISTS Settings (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT,
                                preference JSON
                            )
                        """
        }

        # Create each table
        for table_name, table_query in tables.items():
            cursor.execute(table_query)

        conn.commit()
        cursor.close()
        return db_name
    except Error as e:
        print("Error while creating database:", e)
        return None
