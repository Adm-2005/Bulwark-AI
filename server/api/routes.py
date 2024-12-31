from flask import current_app, jsonify
from pymongo.errors import DuplicateKeyError

@current_app.errorhandler(404)
def handle_404_error(e):
    """Error handler to ensure that 404 errors are not returned as HTML"""
    return jsonify(error=str(e)), 404

@current_app.errorhandler(DuplicateKeyError)
def handle_duplicate_key_error(e):
    """Error handler to ensure that DuplicateKeyError is not returned as HTML"""
    return jsonify(error=f"Duplicate key error."), 400