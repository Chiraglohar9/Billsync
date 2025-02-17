from flask import Flask, render_template, redirect, url_for, request, session
from flask_jwt_extended import JWTManager, create_access_token
from Controllers.auth_controller import auth_bp
from Controllers.dashboard_controller import user_bp
from configuration import Config
from Database.db_config import get_db

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'jwt_token' not in session:  # ✅ Check session instead of requiring JWT
        return redirect(url_for('auth.login'))

    current_user = session.get('user', 'Guest')  # ✅ Retrieve user from session
    return render_template('dashboard.html', user=current_user)

if __name__ == '__main__':
    app.run(debug=True)
