from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Models.dashboard_invoices_model import recent_invoices
from Models.dashboard_transactions_model import recent_transactions
user_bp = Blueprint('user', __name__)


@user_bp.route('/dashboard/profile')
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({'user': current_user})

@user_bp.route('/dashboard')
def dashboard():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))
    username = session.get('user')
    invoices = recent_invoices()
    transactions = recent_transactions()
    return render_template('dashboard.html', invoices=invoices, username=username, transactions=transactions)


@user_bp.route('/invoices', methods=['GET', 'POST'])
def invoices():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))

    return render_template('invoices.html')
  # Render template


@user_bp.route('/transactions')
def transactions():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))  # ✅ Redirect if not logged in
    return render_template('transactions.html')
@user_bp.route('/customers')
def customers():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))  # ✅ Redirect if not logged in
    return render_template('customers.html')
@user_bp.route('/products')
def products():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))  # ✅ Redirect if not logged in
    return render_template('products.html')
@user_bp.route('/accounts')
def accounts():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))  # ✅ Redirect if not logged in
    return render_template('accounts.html')
@user_bp.route('/reports')
def reports():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))  # ✅ Redirect if not logged in
    return render_template('reports.html')
@user_bp.route('/settings')
def settings():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))  # ✅ Redirect if not logged in
    return render_template('settings.html')