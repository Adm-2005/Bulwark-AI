# external imports
from datetime import timedelta
from typing import Tuple, Dict, Any
from flask_jwt_extended import create_access_token
from flask import request, current_app, jsonify, make_response, abort

# internal imports
from api import mongo
from api.auth import auth_bp
from api.db_models.user_models import User
from api.utils.validators import password_validator, email_validator

users = mongo.db['users']

@auth_bp.route('/register', methods = ['POST'])
def register() -> Tuple[Dict[str, Any], int]:
    """Endpoint to register users."""
    try:
        data = request.get_json()
        required_fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        if not data or not all(field in data for field in required_fields):
            abort(400, 'Missing required fields.')

        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip().lower()
        password = data.pop('password', None)

        if not email_validator(email):
            abort(400, 'Invalid email format.')

        if not password_validator(password):
            abort(400, 'Your password must be at least 8 characters long and include at least one lowercase letter, one uppercase letter, and one number.')

        if users.find_one({ '$or': [
                { 'email': email }, 
                { 'username': username }
            ] 
        }):
            abort(400, 'Email or username already exists.')

        user = User(**data)
        user.set_password(password)
        user_id = users.insert_one(user.to_bson()).inserted_id

        response = make_response(jsonify({ 'message': 'Register successful.' }))
        response.set_cookie(
            key = 'bw_auth_token',
            value = create_access_token(identity = str(user_id), expires_delta = timedelta(hours = 24)),
            httponly = request.is_secure,
            secure = request.is_secure,
            samesite = None
        )

        return response, 201

    except Exception as e:
        current_app.logger.error('Error while registering user: %s', e)
        raise e
    
@auth_bp.route('/login', methods = ['POST'])
def login() -> Tuple[Dict[str, Any], int]:
    """Endpoint to login users."""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip().lower()
        password = data.get('password')

        if not data or (not email and not username) or not password:
            abort(400, 'Missing required fields.')

        res = users.find_one({
            '$or': [
                {'email': email},
                {'username': username}
            ]
        })

        if not res:
            abort(404, 'User not found.')

        user = User(**res)     

        if not user or not user.check_password(password):
            abort(400, 'Invalid credentials.')

        response = make_response(jsonify({ 'message': 'Login successful.' }))
        response.set_cookie(
            key = 'bw_auth_token',
            value = create_access_token(identity = str(user.id), expires_delta = timedelta(hours = 24)),
            httponly = request.is_secure,
            secure = request.is_secure,
            samesite = None
        )

        return response, 200

    except Exception as e:
        current_app.logger.error('Error while logging user: %s', e)
        raise e
    
@auth_bp.route('/logout', methods = ['POST'])
def logout() -> Tuple[Dict[str, Any], int]:
    """Endpoint to logout users."""
    try:
        response = make_response(jsonify({ 'message': 'Logout successful.' }))
        response.delete_cookie(
            key = 'bw_auth_token',
            httponly = request.is_secure,
            secure = request.is_secure,
            samesite = None
        )

        return response, 200

    except Exception as e:
        current_app.logger.error('Error during logout: %s', e)
        raise e