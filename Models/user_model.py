from Database.db_config import get_db

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return user

def create_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    cursor.close()
    db.close()