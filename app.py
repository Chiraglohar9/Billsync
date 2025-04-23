from flask import Flask, render_template, redirect, url_for, request, session
from flask_jwt_extended import JWTManager
from Controllers.auth_controller import auth_bp
from Controllers.user_controller import user_bp
from configuration import Config
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
mail = Mail(app)  

app.register_blueprint(auth_bp, url_prefix='/auth') 
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def home():
    if 'jwt_token' not in session:
        return redirect(url_for('auth.login'))
    username = session.get('username')
    if username is None:
        return redirect(url_for('auth.login'))
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
