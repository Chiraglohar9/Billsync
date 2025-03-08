from flask import Flask, render_template, redirect, url_for, request, session
from flask_jwt_extended import JWTManager, create_access_token
from Controllers.auth_controller import auth_bp
from Controllers.user_controller import user_bp
from Models.dashboard_filter_model import invoice_count
from configuration import Config
app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')
@app.route('/')
def home():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))
    return redirect(url_for('user.dashboard'))
if __name__ == '__main__':
    app.run(debug=True, port=5006)
