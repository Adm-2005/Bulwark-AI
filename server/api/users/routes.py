# external imports
from bson import ObjectId
from pymongo import ReturnDocument
from typing import Tuple, Dict, Any
from flask import request, current_app, jsonify, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

# internal imports
from api import mongo
from api.users import user_bp
from api.db_models.user_models import User
from api.utils.object_id import PydanticObjectId

users = mongo.db['users']

@user_bp.route('/', methods = ['GET'])
@jwt_required()
def get_user() -> Tuple[Dict[str, Any], int]:
    """Endpoint to get current user's profile."""
    try:
        user_id = get_jwt_identity()

        res = users.find_one({ '_id': ObjectId(user_id) })
        if not res:
            abort(404, 'User not found.')

        user = User(**res)

        return jsonify({ 
            'message': 'User fetched successfully.', 
            'user': user.to_json()
        }), 200

    except Exception as e:
        current_app.logger.error('')
        raise e

@user_bp.route('/', methods = ['PUT'])
@jwt_required()
def update_user() -> Tuple[Dict[str, Any], int]:
    """Endpoint to update current user."""
    try:
        data = request.get_json()

        if not data:
            abort(400, 'No data to update.')

        user_id = get_jwt_identity()
        updated_user = users.find_one_and_update(
            { '_id': ObjectId(user_id) }, 
            { '$set': data }, 
            return_document = ReturnDocument.AFTER
        )

        if not updated_user:
            abort(404, 'User not found.')
        
        updated_user['_id'] = PydanticObjectId(str(user_id))
        user = User(**updated_user)

        return jsonify({ 
            'message': 'User update successful.',
            'user': user.to_json()
        }), 200
    
    except Exception as e:
        current_app.logger.error('Error while updating user %s: %s', user.get('username'), e)
        raise e    

@user_bp.route('/', methods = ['DELETE'])
@jwt_required()
def delete_user() -> Tuple[Dict[str, Any], int]:
    """Endpoint to delete current user."""
    try:
        user_id = get_jwt_identity()
        deleted_user = users.find_one_and_delete({ '_id': ObjectId(user_id) })

        if not deleted_user:
            abort(404, 'User not found.')
        
        return jsonify({ 'message': 'User deletion successful.' }), 200

    except Exception as e:
        current_app.logger.error('Error while deleting user %s: %s', deleted_user.get('username'), e)
        raise e