import os

class Config:
    MYSQL_HOST = "127.0.0.1"
    MYSQL_USER = "Billsync"  # Replace with your MySQL username
    MYSQL_PASSWORD = "billsync022025"  # Replace with your MySQL password
    MYSQL_DB = "auth"  # Your MySQL database name
    SECRET_KEY = os.urandom(24)  # Secret key for session management
