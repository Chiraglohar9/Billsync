from Database.initialize_user_db import initialize_user_database
def get_invoices(username):
    conn = initialize_user_database()
    if conn is None:
        print("Database connection failed!")
        return []
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Invoices ORDER BY created_at DESC LIMIT 5"
    cursor.execute(query)
    invoices = cursor.fetchall()
    cursor.close()
    conn.close()
    return invoices
