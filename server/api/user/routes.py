from flask import request, jsonify
from pymongo import ReturnDocument
from flask_jwt_extended import get_jwt_identity, jwt_required
from bson import ObjectId
from api import mongo
from api.models import User
from api.user import user_bp
from api.utils.objectId import PydanticObjectId

db = mongo.db
users = db["users"]

@user_bp.route('/', methods=['DELETE'])
@jwt_required()
def delete_user():
    try:
        user_id = get_jwt_identity()
        deleted_user = users.find_one_and_delete({ "_id": ObjectId(user_id) })

        if not deleted_user:
            return jsonify({ "error": "User not found" }), 404
        
        return jsonify({ "message": "User deleted successfully" }), 200
    except Exception as e:
        print(f"Exception while deleting user: {e}")
        return jsonify({ "error": "Internal Server Error" }), 500

@user_bp.route('/', methods=['PUT'])
@jwt_required()
def update_user():
    data = request.get_json()

    if not data:
        return jsonify({ "error": "Missing required fields" }), 400

    try:
        user_id = get_jwt_identity()
        updated_user = users.find_one_and_update({ "_id": ObjectId(user_id) }, { "$set": data }, return_document=ReturnDocument.AFTER)

        if not updated_user:
            return jsonify({ "error": "User not found" }), 404
        
        updated_user["_id"] = PydanticObjectId(str(user_id))
        user = User(**updated_user)

        return jsonify({
            "message": "User updated succesfully",
            "user": user.to_json()
        }), 200
    except Exception as e:
        print(f"Exception while updating user: {e}")
        return jsonify({ "error": "Internal Server Error" }), 500