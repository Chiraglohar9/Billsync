import mysql.connector
from flask import current_app

class User:
    def __init__(self, id, username, email, password, role):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    @staticmethod
    def get_by_email(email):
        conn = current_app.config['DB_CONNECTION']
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM test WHERE email = %s', (email,))
        user_data = cursor.fetchone()
        cursor.close()
        return User(**user_data) if user_data else None

    @staticmethod
    def create(username, email, password, role='user'):
        conn = current_app.config['DB_CONNECTION']
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO test (username, email, password, role) VALUES (%s, %s, %s, %s)',
            (username, email, password, role)
        )
        conn.commit()
        cursor.close()
