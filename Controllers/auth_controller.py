from flask import Blueprint, request, render_template, redirect, url_for, session, flash, current_app
from flask_jwt_extended import create_access_token
from Models.user_model import get_user_by_username, create_user
from Database.create_user_db import create_user_database
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash
from Database.db_config import get_db
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user:
            print(f"User found: {user['username']}")
            print(f"Stored hash: {user['password']}")
            print(f"Password match: {check_password_hash(user['password'], password)}")
        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=user['username'])
            session['jwt_token'] = access_token
            session['user'] = user['username']
            return redirect(url_for('user.dashboard', username=user['username']))
        flash('❌ Invalid username or password.', 'danger')
        return render_template('login.html')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if get_user_by_username(username):
            flash('❌ User already exists. Please choose another username.', 'danger')
            return render_template('register.html')
        hashed_password = generate_password_hash(password)
        create_user(username, hashed_password, email)
        try:
            db_name = create_user_database(username)
        except Exception as e:
            print("Error creating user DB:", e)
            flash('⚠️ Something went wrong while creating your account database.', 'danger')
            return render_template('register.html')
        flash('✅ Account created successfully. Redirecting to login...', 'success')
        return render_template('register.html', redirect_to_login=True)
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('jwt_token', None)
    session.pop('user', None)
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    mail = current_app.extensions.get('mail') 
    if request.method == 'POST':
        email = request.form['email'].strip()
        try:
            conn = get_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            conn.close()
            if user:
                try:
                    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
                    token = serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
                    reset_url = url_for('auth.reset_password', token=token, _external=True)
                    msg = Message('Password Reset Request',
                                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                                  recipients=[email])
                    msg.body = f"""Subject Line: Password Reset Request. \n Hi {user['username']}, \n We received a request to reset the password for your account associated with this email address. If you made this request, please click the link below to reset your password: \n {reset_url} \n This link will expire in [Time Limit] for security reasons. If you did not request a password reset, please ignore this email or contact our support team if you have any concerns. \n Thank you, \n [Billsync]"""
                    mail.send(msg)
                    flash('✅ Password reset link sent to your email.', 'success')
                except Exception as e:
                    print(f"Email sending failed: {e}")
                    flash('⚠️ Failed to send reset email. Please try again later.', 'danger')
                    return render_template('forgot_password.html')
            else:
                flash('❌ Email not found in our records.', 'danger')
                return render_template('forgot_password.html')
        except Exception as db_error:
            print(f"Database error: {db_error}")
            flash('⚠️ Something went wrong. Please try again later.', 'danger')
            return render_template('forgot_password.html')
    return render_template('forgot_password.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
    except SignatureExpired:
        flash('❌ The reset link has expired. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    except BadSignature:
        flash('❌ Invalid or tampered reset link. Please request a new one.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    except Exception as e:
        flash('⚠️ An unexpected error occurred while validating the link.', 'danger')
        print(f"Token validation error: {e}")
        return redirect(url_for('auth.forgot_password'))
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if not password or not confirm_password:
            flash('❗ Please fill out both password fields.', 'danger')
            return render_template('reset_password.html', token=token)
        if password != confirm_password:
            flash('❌ Passwords do not match. Please try again.', 'danger')
            return render_template('reset_password.html', token=token)
        try:
            hashed_password = generate_password_hash(password)
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
            conn.commit()
            flash('✅ Your password has been reset successfully. Please login.', 'success')
        except Exception as e:
            conn.rollback()
            flash('⚠️ Something went wrong while resetting your password. Please try again.', 'danger')
            print(f"Password update error: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template('reset_password.html', token=token)
