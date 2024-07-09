from functools import  wraps
from flask_jwt_extended import get_jwt_identity
from flask import  abort

policies = {
    "AdminPolicy": lambda user: user.get("role") == "admin",
    "ClientPolicy": lambda user: user.get("role") == "client",
    "UserPolicy": lambda user: user.get("role") == "user"
}

def get_current_user():
    user=get_jwt_identity()
    return user

def policy_required(policy_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if not user:
                abort(401)
            if user != policy_name:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator