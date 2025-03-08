from flask import request, jsonify,session
from datetime import datetime, timedelta
from Database.initialize_user_db import initialize_user_database
def invoice_count():
    try:
        username = session.get('user')
        conn = initialize_user_database()
        cursor = conn.cursor(dictionary=True)
        filter_type = request.args.get('filter', 'day')
        start_date, end_date = None, None
        today = datetime.today()
        if filter_type == 'day':
            start_date, end_date = today.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')
        elif filter_type == 'week':
            start_date = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')  # Start of the week (Monday)
            end_date = today.strftime('%Y-%m-%d')  # Today
        elif filter_type == 'month':
            start_date = today.replace(day=1).strftime('%Y-%m-%d')  # First day of the month
            end_date = today.strftime('%Y-%m-%d')  # Today
        elif filter_type == 'year':
            start_date = today.replace(month=1, day=1).strftime('%Y-%m-%d')  # Start of the year
            end_date = today.strftime('%Y-%m-%d')  # Today
        elif filter_type == 'custom':
            # Get custom date range from query parameters
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            if not start_date or not end_date:
                return jsonify({'error': 'Please provide start_date and end_date for custom range'}), 400
        if conn is None:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()
        query = """
            SELECT COUNT(*) FROM Invoices
            WHERE issue_date BETWEEN %s AND %s
        """
        cursor.execute(query, (start_date, end_date))
        total_invoices = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(total_invoices)
        return jsonify({'filter': filter_type, 'total_invoices': total_invoices})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

