from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def user_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        # Check if 'username' is in kwargs and compare with current_user
        if 'username' in kwargs and kwargs['username'] != current_user:
            return jsonify({"error": "Access denied"}), 403
        return f(*args, **kwargs)
    return decorated_function

def admin_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user != 'admin':
            return jsonify({"error": "Access denied"}), 403
        return f(*args, **kwargs)
    return decorated_function