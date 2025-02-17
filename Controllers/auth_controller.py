from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_jwt_extended import create_access_token
from Models.user_model import get_user_by_username, create_user
from Database.create_user_db import create_user_database


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)

        if user and user['password'] == password:
            access_token = create_access_token(identity=user['username'])
            session['jwt_token'] = access_token  # ✅ Store token in session
            session['user'] = user['username']  # ✅ Store username
            return redirect(url_for('auth.dashboard'))  # ✅ Redirect to dashboard

        return render_template('login.html', error="Invalid credentials")  # ✅ Show error in UI

    return render_template('login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user_by_username(username):
            return render_template('signup.html', error="User already exists")  # ✅ Show error in UI
        create_user(username, password)
        db_name = create_user_database(username)  # Create user-specific database
        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_bp.route('/logout')
def logout():
    session.pop('jwt_token', None)
    session.pop('user', None)  # ✅ Clear user session
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
def dashboard():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))  # ✅ Redirect if not logged in

    user = session.get('user', 'Guest')
    return render_template('dashboard.html', username=user)  # ✅ Pass username to template
