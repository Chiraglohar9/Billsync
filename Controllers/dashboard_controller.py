from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from Models.user import User

bp = Blueprint('dashboard', __name__)

@bp.route('/')
@jwt_required()  # This decorator ensures the user must be authenticated
def index():
    user_id = get_jwt_identity()['id']  # Retrieve the user ID from the JWT token
    user = User.get_by_id(user_id)  # Fetch user data from database
    return render_template('dashboard.html', user=user)
