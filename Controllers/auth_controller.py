from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from Models.user import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get login credentials
    email = data.get('email')
    password = data.get('password')

    user = User.get_by_email(email)  # Fetch user from database
    if user and check_password_hash(user.password, password):  # Validate password
        access_token = create_access_token(identity={'id': user.id})  # Create JWT token
        return jsonify({'access_token': access_token})

    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get the JSON data from the request
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Hash the password before saving
    hashed_password = generate_password_hash(password, method='bcrypt')
    User.create(username, email, hashed_password)  # Create a new user
