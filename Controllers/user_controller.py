from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from Models.dashboard_invoices_model import recent_invoices
from Models.dashboard_transactions_model import recent_transactions
from Models.invoices_model import get_invoices
from Models.transactions_model import get_transactions
from Models.customers_model import get_customers
from Models.products_model import get_products
from Models.accounts_model import get_bank_accounts, add_bank_account
user_bp = Blueprint('user', __name__)


@user_bp.route('/dashboard/profile')
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({'user': current_user})

@user_bp.route('/dashboard',methods=['POST','GET'])
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
    page = request.args.get('page', 1, type=int)
    invoices = get_invoices(page=page)
    return render_template('invoices.html',invoices=invoices, page=page)

@user_bp.route('/transactions',methods=['GET', 'POST'])
def transactions():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))
    page = request.args.get('page', 1, type=int)
    transactions = get_transactions(page=page)
    return render_template('transactions.html', transactions=transactions, page=page)

@user_bp.route('/customers')
def customers():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))
    page = request.args.get('page', 1, type=int)
    customers = get_customers(page=page)
    return render_template('customers.html', customers=customers, page=page)

@user_bp.route('/products')
def products():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))
    page = request.args.get('page', 1, type=int)
    products = get_products(page=page)
    return render_template('products.html',products=products, page=page)

@user_bp.route('/accounts')
def accounts():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login')) 

    if request.method == 'POST':
        account_id = request.form.get('account_id')
        bank_name = request.form.get('bank_name')
        account_number = request.form.get('account_number')
        account_type = request.form.get('account_type')
        balance = request.form.get('balance', 0.00, type=float)

        if account_id and bank_name and account_number and account_type:
            success = add_bank_account(account_id, bank_name, account_number, account_type, balance)
            if success:
                return redirect(url_for('user.bank_accounts'))
            else:
                return "Error adding bank account", 500

    bank_accounts = get_bank_accounts()

    return render_template('accounts.html', bank_accounts=bank_accounts)
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