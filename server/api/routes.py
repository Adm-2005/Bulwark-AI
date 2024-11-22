from flask import current_app, jsonify
from pymongo.errors import DuplicateKeyError

@current_app.errorhandler(404)
def resource_not_found(e):
    """Error handler to ensure that 404 errors are not returned as HTML"""
    return jsonify(error=str(e)), 404

@current_app.errorhandler(DuplicateKeyError)
def resource_not_found(e):
    """Error handler to ensure that DuplicateKeyError is not returned as HTML"""
    return jsonify(error=f"Duplicate key error."), 400